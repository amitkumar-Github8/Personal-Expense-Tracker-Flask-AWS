#!/usr/bin/env python3



import os
from flask.cli import FlaskGroup
from app import create_app, db
from app.models import Category, Expense

# Create Flask application
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Create CLI group
cli = FlaskGroup(app)

@app.cli.command()
def init_db():
    """Initialize the database."""
    print("Creating database tables...")
    db.create_all()
    print("✅ Database tables created")

    print("Creating default categories...")
    Category.create_default_categories()
    print("✅ Default categories created")

    print("🎉 Database initialization complete!")

@app.cli.command()
def reset_db():
    """Reset the database."""
    print("Dropping all tables...")
    db.drop_all()
    print("Creating fresh tables...")
    db.create_all()
    print("Creating default categories...")
    Category.create_default_categories()
    print("🎉 Database reset complete!")

@app.shell_context_processor
def make_shell_context():
    """Make database models available in shell."""
    return {
        'db': db,
        'Category': Category,
        'Expense': Expense
    }

if __name__ == '__main__':
    print("Starting Flask Expense Tracker...")
    print("Access your app at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)

    # Initialize database on first run
    with app.app_context():
        db.create_all()
        if Category.query.count() == 0:
            print("First run detected - creating default categories...")
            Category.create_default_categories()

    # Use debug from app config for flexibility
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
