# Personal Expense Tracker

This is a simple web application to track your personal expenses. You can add, edit, and delete expenses, organize them by category, and view summaries.


## Features

- ✅ Add, edit, and delete your expenses easily
- ✅ Organize expenses by custom categories
- ✅ View a dashboard with monthly and yearly totals
- ✅ See recent expenses and category breakdowns
- ✅ Search and filter expenses by description or category
- ✅ Responsive design for desktop and mobile


## Getting Started

Follow these steps to set up and run the Expense Tracker app:

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ExpenseTrackerApp
   ```

2. **Create and activate a virtual environment**
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open your browser**
   Go to [http://localhost:5000](http://localhost:5000)


## Project Structure

```
ExpenseTrackerApp/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   └── expense.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── add_expense.html
│       ├── edit_expense.html
│       ├── expenses.html
│       └── errors/
│           ├── 404.html
│           └── 500.html
├── config.py
├── requirements.txt
├── run.py
├── manage.py
└── README.md
```


## Requirements

- Python 3.8 or higher
- pip (Python package installer)


>>>>>>> 07a556a (Initial commit: Flask Expense Tracker ready for AWS deployment)
