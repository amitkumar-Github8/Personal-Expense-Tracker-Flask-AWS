
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from app import db

class Expense(db.Model):
    """Expense model for tracking individual expenses."""

    __tablename__ = 'expenses'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Expense details
    description = db.Column(db.String(255), nullable=False, index=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    notes = db.Column(db.Text)

    # Foreign key
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, description, amount, category_id, date=None, notes=None):
        """Initialize a new Expense."""
        self.description = description.strip()
        self.amount = self._validate_amount(amount)
        self.category_id = category_id
        self.date = date or datetime.now().date()
        self.notes = notes.strip() if notes else None

    def __repr__(self):
        return f'<Expense {self.description}: ${self.amount}>'

    def _validate_amount(self, amount):
        """Validate and convert amount to proper Decimal."""
        try:
            decimal_amount = Decimal(str(amount))
            if decimal_amount <= 0:
                raise ValueError("Amount must be positive")
            return decimal_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid amount: {amount}")

    @property
    def formatted_amount(self):
        """Return formatted amount as currency string."""
        return f"${self.amount:.2f}"

    @property
    def formatted_date(self):
        """Return formatted date string (YYYY-MM-DD)."""
        return self.date.strftime('%Y-%m-%d')

    @property
    def display_date(self):
        """Return user-friendly date string."""
        return self.date.strftime('%B %d, %Y')

    @property
    def is_recent(self):
        """Check if expense was created in the last 7 days."""
        return (datetime.now().date() - self.date).days <= 7

    def to_dict(self):
        """Convert expense to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'description': self.description,
            'amount': float(self.amount),
            'formatted_amount': self.formatted_amount,
            'date': self.formatted_date,
            'display_date': self.display_date,
            'notes': self.notes,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'category_icon': self.category.icon if self.category else None,
            'category_color': self.category.color if self.category else '#747D8C',
            'is_recent': self.is_recent,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def get_monthly_total(year=None, month=None):
        """Get total expenses for a specific month."""
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month

        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        total = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.date >= start_date,
            Expense.date < end_date
        ).scalar()

        return float(total) if total else 0.0

    @staticmethod
    def get_yearly_total(year=None):
        """Get total expenses for a specific year."""
        if not year:
            year = datetime.now().year

        start_date = date(year, 1, 1)
        end_date = date(year + 1, 1, 1)

        total = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.date >= start_date,
            Expense.date < end_date
        ).scalar()

        return float(total) if total else 0.0

    @staticmethod
    def get_category_totals(year=None, month=None):
        """Get expense totals grouped by category."""
        from app.models.category import Category

        query = db.session.query(
            Category.name,
            Category.icon,
            Category.color,
            db.func.sum(Expense.amount).label('total')
        ).join(Expense).group_by(Category.id)

        if year and month:
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month + 1, 1)

            query = query.filter(
                Expense.date >= start_date,
                Expense.date < end_date
            )

        results = query.all()
        return [
            {
                'category': result.name,
                'icon': result.icon,
                'color': result.color,
                'total': float(result.total)
            }
            for result in results
        ]

    @staticmethod
    def get_recent_expenses(limit=10):
        """Get most recent expenses."""
        return Expense.query.order_by(
            Expense.date.desc(),
            Expense.created_at.desc()
        ).limit(limit).all()
