category_model_content = """\"\"\"
Category Model for Expense Tracker

This model manages expense categories with icons, colors, and descriptions.
Each category can have multiple expenses associated with it.
\"\"\"

from datetime import datetime
from app import db

class Category(db.Model):
    \"\"\"
    Category model for organizing expenses.
    
    Attributes:
        id (int): Primary key
        name (str): Category name (unique)
        description (str): Category description
        color (str): Hex color code for UI
        icon (str): Emoji icon for category
        is_active (bool): Whether category is active
        created_at (datetime): Creation timestamp
    \"\"\"
    
    __tablename__ = 'categories'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Category information
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#007bff')
    icon = db.Column(db.String(50), default='💰')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    expenses = db.relationship(
        'Expense',
        backref='category',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='desc(Expense.date)'
    )
    
    def __init__(self, name, description=None, color='#007bff', icon='💰'):
        \"\"\"Initialize a new Category.\"\"\"
        self.name = name
        self.description = description
        self.color = color
        self.icon = icon
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def __str__(self):
        return f'{self.icon} {self.name}'
    
    @property
    def total_expenses(self):
        \"\"\"Calculate total amount spent in this category.\"\"\"
        return sum(float(expense.amount) for expense in self.expenses)
    
    @property
    def expense_count(self):
        \"\"\"Count number of expenses in this category.\"\"\"
        return len(self.expenses)
    
    def to_dict(self):
        \"\"\"Convert category to dictionary for JSON serialization.\"\"\"
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'icon': self.icon,
            'is_active': self.is_active,
            'total_expenses': self.total_expenses,
            'expense_count': self.expense_count,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def create_default_categories():
        \"\"\"Create default expense categories.\"\"\"
        default_categories = [
            {
                'name': 'Food & Dining',
                'description': 'Restaurants, groceries, and food-related expenses',
                'icon': '🍽️',
                'color': '#FF6B6B'
            },
            {
                'name': 'Transportation',
                'description': 'Gas, parking, public transport, and travel costs',
                'icon': '🚗',
                'color': '#4ECDC4'
            },
            {
                'name': 'Entertainment',
                'description': 'Movies, games, hobbies, and recreational activities',
                'icon': '🎬',
                'color': '#45B7D1'
            },
            {
                'name': 'Shopping',
                'description': 'Clothing, accessories, and personal items',
                'icon': '🛍️',
                'color': '#96CEB4'
            },
            {
                'name': 'Bills & Utilities',
                'description': 'Electricity, water, internet, and monthly bills',
                'icon': '💡',
                'color': '#FECA57'
            },
            {
                'name': 'Healthcare',
                'description': 'Medical expenses, pharmacy, and health-related costs',
                'icon': '🏥',
                'color': '#FF9FF3'
            },
            {
                'name': 'Education',
                'description': 'Books, courses, and educational materials',
                'icon': '📚',
                'color': '#54A0FF'
            },
            {
                'name': 'Travel',
                'description': 'Flights, hotels, and vacation expenses',
                'icon': '✈️',
                'color': '#5F27CD'
            },
            {
                'name': 'Others',
                'description': 'Miscellaneous expenses that don\\'t fit other categories',
                'icon': '📝',
                'color': '#747D8C'
            }
        ]
        
        categories_created = 0
        for cat_data in default_categories:
            existing = Category.query.filter_by(name=cat_data['name']).first()
            if not existing:
                category = Category(**cat_data)
                db.session.add(category)
                categories_created += 1
        
        try:
            db.session.commit()
            if categories_created > 0:
                print(f"✅ Created {categories_created} default categories")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating categories: {e}")
    
    @classmethod
    def get_active_categories(cls):
        \"\"\"Get all active categories ordered by name.\"\"\"
        return cls.query.filter_by(is_active=True).order_by(cls.name).all()
"""

"""
Category Model for Expense Tracker

This model manages expense categories with icons, colors, and descriptions.
Each category can have multiple expenses associated with it.
"""

from datetime import datetime
from app import db

class Category(db.Model):
    """
    Category model for organizing expenses.

    Attributes:
        id (int): Primary key
        name (str): Category name (unique)
        description (str): Category description
        color (str): Hex color code for UI
        icon (str): Emoji icon for category
        is_active (bool): Whether category is active
        created_at (datetime): Creation timestamp
    """

    __tablename__ = 'categories'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Category information
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#007bff')
    icon = db.Column(db.String(50), default='💰')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    expenses = db.relationship(
        'Expense',
        backref='category',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='desc(Expense.date)'
    )

    def __init__(self, name, description=None, color='#007bff', icon='💰'):
        """Initialize a new Category."""
        self.name = name
        self.description = description
        self.color = color
        self.icon = icon

    def __repr__(self):
        return f'<Category {self.name}>'

    def __str__(self):
        return f'{self.icon} {self.name}'

    @property
    def total_expenses(self):
        """Calculate total amount spent in this category."""
        return sum(float(expense.amount) for expense in self.expenses)

    @property
    def expense_count(self):
        """Count number of expenses in this category."""
        return len(self.expenses)

    def to_dict(self):
        """Convert category to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'icon': self.icon,
            'is_active': self.is_active,
            'total_expenses': self.total_expenses,
            'expense_count': self.expense_count,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def create_default_categories():
        """Create default expense categories."""
        default_categories = [
            {
                'name': 'Food & Dining',
                'description': 'Restaurants, groceries, and food-related expenses',
                'icon': '🍽️',
                'color': '#FF6B6B'
            },
            {
                'name': 'Transportation',
                'description': 'Gas, parking, public transport, and travel costs',
                'icon': '🚗',
                'color': '#4ECDC4'
            },
            {
                'name': 'Entertainment',
                'description': 'Movies, games, hobbies, and recreational activities',
                'icon': '🎬',
                'color': '#45B7D1'
            },
            {
                'name': 'Shopping',
                'description': 'Clothing, accessories, and personal items',
                'icon': '🛍️',
                'color': '#96CEB4'
            },
            {
                'name': 'Bills & Utilities',
                'description': 'Electricity, water, internet, and monthly bills',
                'icon': '💡',
                'color': '#FECA57'
            },
            {
                'name': 'Healthcare',
                'description': 'Medical expenses, pharmacy, and health-related costs',
                'icon': '🏥',
                'color': '#FF9FF3'
            },
            {
                'name': 'Education',
                'description': 'Books, courses, and educational materials',
                'icon': '📚',
                'color': '#54A0FF'
            },
            {
                'name': 'Travel',
                'description': 'Flights, hotels, and vacation expenses',
                'icon': '✈️',
                'color': '#5F27CD'
            },
            {
                'name': 'Others',
                'description': 'Miscellaneous expenses that don\'t fit other categories',
                'icon': '📝',
                'color': '#747D8C'
            }
        ]

        categories_created = 0
        for cat_data in default_categories:
            existing = Category.query.filter_by(name=cat_data['name']).first()
            if not existing:
                category = Category(**cat_data)
                db.session.add(category)
                categories_created += 1

        try:
            db.session.commit()
            if categories_created > 0:
                print(f"✅ Created {categories_created} default categories")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating categories: {e}")

    @classmethod
    def get_active_categories(cls):
        """Get all active categories ordered by name."""
        return cls.query.filter_by(is_active=True).order_by(cls.name).all()
