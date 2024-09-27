# Import necessary modules
from flask import Flask, render_template

# Create a Flask application instance
app = Flask(__name__)

# Define a view function for the main route '/'
@app.route('/')
def index():
    return render_template('index.html')