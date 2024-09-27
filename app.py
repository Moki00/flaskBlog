# Import modules
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

# Create a Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY']='your secret key'

# Main page
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# See a post
@app.route('/<int:post_id>')
def post(post_id):
    #user clicks and saves value in 'post' var
    post = get_post(post_id)
    # render the post page in the html
    return render_template('post.html', post=post)

# create posts
@app.route('/create', methods=('GET', 'POST'))
def create():
    # if user clicks Submit
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

# Edit Posts
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    # get the post by id
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            # UPDATE has to be like below
            conn.execute('UPDATE posts SET title = ?, content = ?' 'WHERE id = ?' , (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)

# connect to Database
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
    # Do we have the post or 404?
    if post is None:
        abort(404)
    return post