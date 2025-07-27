import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )
    return conn

# Function to initialize the database table
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create the table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            category VARCHAR(100) NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Main page route
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY date DESC;")
    expenses = cur.fetchall()
    cur.execute("SELECT SUM(amount) FROM expenses;")
    total_result = cur.fetchone()[0]
    total = total_result if total_result is not None else 0
    cur.close()
    conn.close()

    # Convert fetched data to a list of dictionaries for easier template rendering
    expenses_list = []
    for row in expenses:
        expenses_list.append({
            "date": row[1].strftime('%Y-%m-%d'),
            "category": row[2],
            "amount": row[3],
            "description": row[4]
        })

    return render_template('index.html', expenses=expenses_list, total_expenses=total)

# Route to add an expense
@app.route('/add', methods=['POST'])
def add_expense():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)",
        (request.form['date'], request.form['category'], float(request.form['amount']), request.form['description'])
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

# Run the database setup when the app starts
with app.app_context():
    init_db()

if __name__ == '__main__':
    # This part is only for local testing, not for production
    app.run(debug=True)