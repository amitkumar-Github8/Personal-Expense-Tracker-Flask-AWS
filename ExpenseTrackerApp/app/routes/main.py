"""
Main Routes for Flask Expense Tracker

Handles all core functionality including dashboard, CRUD operations,
form processing, and API endpoints.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.expense import Expense
from app.models.category import Category

# Create Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Dashboard - Display recent expenses and summary statistics."""
    try:
        # Get recent expenses
        recent_expenses = Expense.get_recent_expenses(limit=10)

        # Get current date statistics
        current_date = datetime.now()
        monthly_total = Expense.get_monthly_total(current_date.year, current_date.month)
        yearly_total = Expense.get_yearly_total(current_date.year)

        # Get category breakdown
        category_totals = Expense.get_category_totals(current_date.year, current_date.month)

        # Get categories for quick add
        categories = Category.get_active_categories()

        # Count total expenses
        total_expenses_count = Expense.query.count()

        return render_template(
            'index.html',
            recent_expenses=recent_expenses,
            monthly_total=monthly_total,
            yearly_total=yearly_total,
            category_totals=category_totals,
            categories=categories,
            total_expenses_count=total_expenses_count,
            current_month=current_date.strftime('%B %Y'),
            current_year=current_date.year
        )

    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('index.html', 
                             recent_expenses=[], 
                             categories=[],
                             monthly_total=0,
                             category_totals=[])

@main_bp.route('/expenses')
def expenses():
    """View all expenses with pagination and filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        category_id = request.args.get('category', type=int)
        search_term = request.args.get('search', '').strip()

        # Base query
        query = Expense.query

        # Apply search filter
        if search_term:
            query = query.filter(Expense.description.contains(search_term))

        # Apply category filter
        if category_id:
            query = query.filter_by(category_id=category_id)

        # Paginate results
        expenses_paginated = query.order_by(
            Expense.date.desc(), 
            Expense.created_at.desc()
        ).paginate(
            page=page, 
            per_page=20, 
            error_out=False
        )

        # Get categories for filter
        categories = Category.get_active_categories()

        return render_template(
            'expenses.html',
            expenses=expenses_paginated.items,
            pagination=expenses_paginated,
            categories=categories,
            selected_category=category_id,
            search_term=search_term
        )

    except Exception as e:
        flash(f'Error loading expenses: {str(e)}', 'error')
        return render_template('expenses.html', expenses=[], categories=[])

@main_bp.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Add a new expense."""
    if request.method == 'POST':
        return _process_expense_form()

    # GET request - show form
    categories = Category.get_active_categories()

    if not categories:
        Category.create_default_categories()
        categories = Category.get_active_categories()

    return render_template('add_expense.html', categories=categories)

@main_bp.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    """Edit an existing expense."""
    expense = Expense.query.get_or_404(expense_id)

    if request.method == 'POST':
        return _process_expense_form(expense)

    categories = Category.get_active_categories()
    return render_template('edit_expense.html', expense=expense, categories=categories)

@main_bp.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    """Delete an expense."""
    try:
        expense = Expense.query.get_or_404(expense_id)
        description = expense.description

        db.session.delete(expense)
        db.session.commit()

        flash(f'Expense "{description}" deleted successfully!', 'success')

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting expense: {str(e)}', 'error')

    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/api/expenses/summary')
def api_expenses_summary():
    """API endpoint for expense summary data."""
    try:
        current_date = datetime.now()
        monthly_total = Expense.get_monthly_total(current_date.year, current_date.month)
        yearly_total = Expense.get_yearly_total(current_date.year)
        category_totals = Expense.get_category_totals(current_date.year, current_date.month)

        return jsonify({
            'status': 'success',
            'data': {
                'monthly_total': monthly_total,
                'yearly_total': yearly_total,
                'category_totals': category_totals,
                'month': current_date.strftime('%B %Y'),
                'year': current_date.year
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def _process_expense_form(expense=None):
    """Process expense form submission (shared by add and edit)."""
    try:
        # Get form data
        description = request.form.get('description', '').strip()
        amount_str = request.form.get('amount', '').strip()
        category_id = request.form.get('category_id', type=int)
        date_str = request.form.get('date', '').strip()
        notes = request.form.get('notes', '').strip()

        # Validation
        errors = []

        if not description:
            errors.append('Description is required')
        elif len(description) > 255:
            errors.append('Description must be less than 255 characters')

        if not amount_str:
            errors.append('Amount is required')
        else:
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    errors.append('Amount must be positive')
                elif amount > 999999.99:
                    errors.append('Amount is too large')
            except (InvalidOperation, ValueError):
                errors.append('Invalid amount format')

        if not category_id:
            errors.append('Category is required')
        else:
            category = Category.query.get(category_id)
            if not category or not category.is_active:
                errors.append('Invalid category selected')

        # Validate date
        expense_date = date.today()
        if date_str:
            try:
                expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Invalid date format')

        # Show errors if any
        if errors:
            for error in errors:
                flash(error, 'error')

            redirect_route = 'main.edit_expense' if expense else 'main.add_expense'
            redirect_args = {'expense_id': expense.id} if expense else {}
            return redirect(url_for(redirect_route, **redirect_args))

        # Create or update expense
        if expense:
            expense.description = description
            expense.amount = amount
            expense.category_id = category_id
            expense.date = expense_date
            expense.notes = notes or None
            expense.updated_at = datetime.utcnow()
            action = 'updated'
        else:
            expense = Expense(
                description=description,
                amount=amount,
                category_id=category_id,
                date=expense_date,
                notes=notes or None
            )
            db.session.add(expense)
            action = 'added'

        db.session.commit()
        flash(f'Expense "{description}" {action} successfully!', 'success')
        return redirect(url_for('main.index'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error processing expense: {str(e)}', 'error')
        redirect_route = 'main.edit_expense' if expense else 'main.add_expense'
        redirect_args = {'expense_id': expense.id} if expense else {}
        return redirect(url_for(redirect_route, **redirect_args))

# Error handlers
@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
