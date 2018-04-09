import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config the database link
DATABASE_URL = None
if os.environ.get('DATABASE_URL') != None:
    # The reason we use get here is environ['var'] will cause an exception, while get reutrn None for non-existing value.
    DATABASE_URL = os.environ['DATABASE_URL']   # Get the URL of database from Heroku

# Database configuration
if DATABASE_URL != None:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    db = SQLAlchemy(app)


@app.route('/')
def index():
    return "DATABASE_URL: " + DATABASE_URL

@app.route('/profile/<username>')
def profile(username):
    return "Hi there " + username

@app.route('/post/<int:postId>') # Restrict data type
def show_post(postId):  # Name not necessary to be same
    return "Post ID is: " + str(postId)

@app.route('/bacon/', methods = ['GET', 'POST'])  # Set the allowed HTTP method
def bacon():
    return "Method used: " + request.method  # Return Method used

if __name__ == "__main__":
    app.run(debug=True)
