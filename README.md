# Personal Expense Tracker

A web application to track personal expenses, built with Flask and designed for cloud deployment and monitoring.  
**Stack:** Flask (Python) • AWS EC2 • AWS RDS • AWS CloudWatch

---

## Project Overview

This project helps users manage and analyze their personal expenses. It supports adding, editing, and deleting expenses, organizing them by category, and viewing summaries.  
The app is designed for real-world deployment on AWS, using EC2 for hosting, RDS for the database, and CloudWatch for monitoring and alerts.

---

## Features

- Add, edit, and delete expenses
- Categorize expenses for better organization
- Dashboard with monthly and yearly summaries
- Search and filter expenses
- Responsive design for desktop and mobile
- Cloud-ready: easily deployable to AWS EC2 with RDS
- Monitoring and alerting with AWS CloudWatch

---

## Tech Stack

- Python 3.8+
- Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF
- MySQL (via AWS RDS) or SQLite (for local/dev)
- Gunicorn (for production WSGI server)
- AWS EC2 (hosting), AWS RDS (database), AWS CloudWatch (monitoring)

---

## Getting Started (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/amitkumar-Github8/Personal-Expense-Tracker-Flask-AWS.git
   cd ExpenseTrackerApp
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```
   Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deployment on AWS

- Launch an EC2 instance (Ubuntu recommended)
- Install Python, pip, and git
- Clone this repo and set up your virtual environment
- Set up an RDS instance (MySQL recommended) and update your `.env` with the RDS connection string
- Use Gunicorn to run the app in production
- (Recommended) Use Nginx as a reverse proxy
- Set up CloudWatch for EC2 and RDS monitoring and alerts

See `Instructions.md` for a detailed AWS deployment guide.

---

## Project Structure

```
ExpenseTrackerApp/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── config.py
├── requirements.txt
├── run.py
├── manage.py
└── README.md
```

---

## Requirements

- Python 3.8 or higher
- pip

---

## License

MIT License

---

**This project demonstrates full-stack development, cloud deployment, and infrastructure monitoring in one practical application.**
