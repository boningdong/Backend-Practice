# request in flask can check used method
from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def index():
    return "Method used: " + request.method # Return Method used

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