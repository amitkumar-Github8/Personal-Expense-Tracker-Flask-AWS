#!/usr/bin/env python3
"""
Personal Expense Tracker - Setup Script
Automated installation and configuration
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime

def print_step(step, message):
    print(f"[{step}] {message}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def check_python_version():
    print_step("1/5", "Checking Python version...")

    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required. Current: {sys.version}")
        return False

    print_success(f"Python {sys.version.split()[0]} detected")
    return True

def setup_virtual_environment():
    print_step("2/5", "Setting up virtual environment...")

    if not os.path.exists("venv"):
        result = subprocess.run([sys.executable, "-m", "venv", "venv"])
        if result.returncode != 0:
            print_error("Failed to create virtual environment")
            return False

    print_success("Virtual environment ready")
    return True

def install_dependencies():
    print_step("3/5", "Installing dependencies...")

    pip_path = "pip"
    if os.name == "nt":  # Windows
        pip_path = "venv\\Scripts\\pip.exe"
    else:  # Unix
        pip_path = "venv/bin/pip"

    if not os.path.exists(pip_path):
        pip_path = "pip"

    result = subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    if result.returncode != 0:
        print_error("Failed to install dependencies")
        return False

    print_success("Dependencies installed")
    return True

def initialize_database():
    print_step("4/5", "Initializing database...")

    try:
        from app import create_app, db
        from app.models.category import Category

        app = create_app('development')
        with app.app_context():
            db.create_all()

            if Category.query.count() == 0:
                Category.create_default_categories()
                print_success("Database initialized with default categories")
            else:
                print_success("Database already initialized")

        return True

    except Exception as e:
        print_error(f"Database initialization failed: {e}")
        return False

def create_env_file():
    print_step("5/5", "Creating environment file...")

    if os.path.exists('.env'):
        print_success(".env file already exists")
        return True

    env_content = f'''# Flask Configuration - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
FLASK_CONFIG=development
SECRET_KEY=dev-secret-key-{datetime.now().strftime('%Y%m%d')}
DATABASE_URL=sqlite:///expense_tracker.db
DEBUG=True
'''

    with open('.env', 'w') as f:
        f.write(env_content)

    print_success("Environment file created")
    return True

def main():
    print("🚀 Personal Expense Tracker Setup")
    print("=" * 40)

    steps = [
        check_python_version,
        setup_virtual_environment, 
        install_dependencies,
        initialize_database,
        create_env_file
    ]

    for step_func in steps:
        if not step_func():
            print_error("Setup failed!")
            sys.exit(1)
        print()

    print("🎉 Setup Complete!")
    print()
    print("Next steps:")
    print("1. Activate virtual environment:")
    if os.name == "nt":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Start the application:")
    print("   python run.py")
    print("3. Open browser:")
    print("   http://localhost:5000")

if __name__ == "__main__":
    main()
