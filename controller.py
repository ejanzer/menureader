from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
import os
from werkzeug.utils import secure_filename
from urllib import urlopen

UPLOAD_FOLDER = "./image_uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "lkfejowiefmoiewgmwogi"

# Specify the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    pass

@app.route("/login")
def login():
    pass

@app.route("/logout")
def logout():
    pass

@app.route("/signup")
def signup():
    pass

@app.route("/upload/file", methods=["POST"])
def upload_file():
    pass

@app.route("/upload/webcam", methods=["POST"])
def upload_webcam():
    pass

@app.route("/dish/<int:id>")
def view_dish(id):
    pass

@app.route("/dish/new", methods=["POST"])
def add_dish():
    pass

@app.route("/restaurant/<int:id>")
def view_restaurant(id):
    pass

@app.route("/user/<int:id>")
def view_user(id):
    pass

@app.route("/user/new", methods=["POST"])
def add_user():
    pass

@app.route("/search/<string:text>")
def search(text):
    pass

@app.route("/review/new", methods=["POST"])
def add_review():
    pass

if __name__ == "__main__":
    # Change debug to False when deploying, probably.
    app.run(debug = True)

