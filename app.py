# Import necessary modules
import sqlite3
from flask import Flask, render_template, abort

# Create a Flask application instance
app = Flask(__name__)

# Define a view function for the main route '/'
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    #user clicks and saves value in 'post' var
    post = get_post(post_id)
    # render the post page in the html
    return render_template('post.html', post=post)

# Database Connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    # open the connection to database
    conn = get_db_connection()
    # select the post based on its ID. ? holds the id variable
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    # Do we have the post?
    if post is None:
        abort(404)
    return post