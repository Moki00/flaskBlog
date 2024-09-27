# Import necessary modules
import sqlite3
from flask import Flask, render_template

# Create a Flask application instance
app = Flask(__name__)

# Define a view function for the main route '/'
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Database Connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn