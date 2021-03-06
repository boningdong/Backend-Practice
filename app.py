import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DATABASE_URL = None
db = None
# Config the database link
if os.environ.get('DATABASE_URL') != None:
    # The reason we use get here is environ['var'] will cause an exception, while get reutrn None for non-existing value.
    DATABASE_URL = os.environ['DATABASE_URL']   # Get the URL of database from Heroku

# Database configuration
if DATABASE_URL != None:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    db = SQLAlchemy(app)

# Flask Practice
@app.route('/')
def index():
    return "DATABASE_URL: " + DATABASE_URL  # Display the URL if found

@app.route('/profile/<username>')
def profile(username):
    return "Hi there " + username

@app.route('/post/<int:postId>') # Restrict data type
def show_post(postId):  # Name not necessary to be same
    return "Post ID is: " + str(postId)

@app.route('/bacon/', methods = ['GET', 'POST'])  # Set the allowed HTTP method
def bacon():
    return "Method used: " + request.method  # Return Method used

# APIs practice
# Model
class Info(db.Model):
    __tablename__ = "StringTable"
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(100), nullable=False)

    def __init__ (self, id, info):
        self.id = id
        self.info = info

    def toString(self):
        return "Info id: {} str: {}".format(self.id, self.info)

# Create all tables
db.create_all()

@app.route('/getstring/<string:str>', methods = ['POST'])
def get_string(str):
    return "The received string is: " + str

@app.route('/savestring/<string:str>', methods = ['POST'])
def save_string(str):
    max = db.session.query(db.func.max(Info.id)).scalar() # Get the max id
    info = Info(max + 1, str) # This will save the data into database with id = max + 1.
    db.session.add(info)
    db.session.commit()

    # Print out what is left in DB
    strBuilder = ""
    entries = Info.query.order_by(Info.info).all() # Essentially, Info tells which database to query.
    for entry in entries:
        strBuilder += entry.toString() + '\n'
    return strBuilder

@app.route('/removestring/<string:str>', methods = ['POST'])
def remove_string(str):
    deleteItem = Info.query.filter_by(info=str).first()
    if deleteItem != None:
        db.session.delete(deleteItem)
        db.session.commit()

    # Print out what is left in DB
    strBuilder = ""
    entries = Info.query.order_by(Info.info).all() # Essentially, Info tells which database to query.
    for entry in entries:
        strBuilder += entry.toString() + '\n'
    return strBuilder

@app.route('/getstring/<string:name>', methods = ['GET'])
def get_info(name):
    getItem = Info.query.filter_by(info=name).first()
    if getItem != None:
        return "The item found is: " + getItem.toString()
    else:
        return "Cannot find the match item"


if __name__ == "__main__":
    app.run(debug=True)
