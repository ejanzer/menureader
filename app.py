from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
import json
import os
from urllib import urlopen
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./image_uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "secret"

# Specify the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    # Login form should be handled by view controller.
    # This handler will accept post data and confirm if the user is authenticated.
    pass

@app.route("/logout")
def logout():
    # Destroy the current session.
    pass

@app.route("/signup")
def signup():
    # Signup form should be handled by view controller.
    # This handler will accept post data, create a new user and confirm.
    pass

@app.route("/upload/file", methods=["POST"])
def upload_file():
    # Accept a File object in form data and send to tesseract for processing.
    # Return the text, dish object, translation and/or relevant dishes
    pass

@app.route("/upload/webcam", methods=["POST"])
def upload_webcam():
    # Accept a base64-encoded bytestream and send to tesseract for processing.
    # Return the text, dish object, translation and/or relevant classes.
    # TODO: Do security checks on image.
    pass

@app.route("/dish/<int:id>")
def view_dish(id):
    # Will return dish object from database.
    pass

@app.route("/dish/new", methods=["POST"])
def add_dish():
    # Takes post data and creates a new dish in the database.
    pass

@app.route("/restaurant/<int:id>")
def view_restaurant(id):
    # Returns restaurant object.
    pass

@app.route("/user/<int:id>")
def view_user(id):
    # Returns user data (not the password)
    pass

@app.route("/search/<string:text>")
def search(text):
    # Returns search data for a particular query.
    # Step 1: Check the dishes table for an exact match.
    # Step 2: Check dishes for a partial match.
    # Step 3: Check food_words for an exact/partial match.
    # Step 4: Look up remaining characters in CEDICT.
    # If no exact matches, return best translation (*) and top 5 results from dishes.
    pass

@app.route("/review/new", methods=["POST"])
def add_review():
    # Accepts post data and creates a review object.
    pass

if __name__ == "__main__":
    # Change debug to False when deploying, probably.
    app.run(debug = True)

