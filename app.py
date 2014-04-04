from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session, send_file
import json
import datetime
import os
from urllib import urlopen
from werkzeug.utils import secure_filename

from config import SECRET_KEY, DISH_IMAGE_PATH, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from model.model import Dish, User, Tag
from tesseract.pytesser import image_file_to_string
from normalize import preprocess_image, smooth_and_thin_image
from translate import search_dish_name
from timing import time_elapsed

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Specify the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    # Login form should be handled by view controller.
    # This handler will accept post data and confirm if the user is authenticated.
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.find_user(username)
    if user:
        auth = user.authenticate(password)
        if auth:
            return "Logged in."
        else:
            return "Username and password don't match."

    return "Username and password don't match."

@app.route("/logout")
def logout():
    # Destroy the current session.
    session.clear()
    
    return "Logged out."

@app.route("/signup", methods=["POST"])
def signup():
    # Signup form should be handled by view controller.
    # This handler will accept post data, create a new user and confirm.
    username = request.form.get('username')
    password = request.form.get('password')
    password_verify = request.form.get('password_verify')

    response = User.create_user(username, password, password_verify)

    return response

@app.route("/upload", methods=["POST"])
def upload():
    if request.data:
        file = request.data
        now = datetime.datetime.utcnow()
        filename = now.strftime('%Y%m%d%M%S') + '.png'
        print filename

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print image_path

        with open(image_path, 'wb') as f:
            f.write(file)

        start = datetime.datetime.now()
        start = time_elapsed("Writing file", start)

        # do some preprocessing on the image to optimize it for Tesseract
        preprocess_image(image_path)
        start = time_elapsed("Preprocessing", start)

        # run the image through tesseract and extract text
        text = image_file_to_string(image_path, lang="chi_sim", graceful_errors=True)
        text = text.strip()
        start = time_elapsed("Tesseract", start)

        if not text:
            # try thinning the image to see if it improves results from Tesseract
            smooth_and_thin_image(image_path)

            # try running through tesseract again
            text = image_file_to_string(image_path, lang="chi_sim", graceful_errors=True)
            text = text.strip()
            start = time_elapsed("Tesseract", start)

            if not text:
                print "No text received from Tesseract!"
                error_data = {"error": "No results found. Please try again."}
                return json.dumps(error_data)

        print "Received text from Tesseract: ", text
        return redirect(url_for("search", text=text))

@app.route("/dish/<int:id>")
def view_dish(id):
    # Will return dish object from database.
    dish = Dish.get_dish_by_id(id)
    data = dish.get_json()
    return json.dumps(data)

@app.route("/dish/new", methods=["POST"])
def add_dish():
    # Takes post data and creates a new dish in the database.
    user_id = session.get("user_id")
    pass

@app.route("/restaurant/<int:id>")
def view_restaurant(id):
    # Returns restaurant object.
    pass

@app.route("/user/<int:id>")
def view_user(id):
    # Returns user data (not the password)
    user = User.get_user_by_id(id)
    data = User.get_json(user)
    return json.dumps(data)

@app.route("/search/<string:text>")
def search(text):
    start = datetime.datetime.now()
    print "Searching for text:", text

    # Returns search data for a particular query.
    results = search_dish_name(text)
    time_elapsed("Search and translate", start)
    return json.dumps(results)

@app.route("/review/new", methods=["POST"])
def add_review():
    # Accepts post data and creates a review object.
    pass

@app.route("/tag/<tag_id>")
def view_tag(tag_id):
    # View all dishes for a certain tag.
    tag = Tag.get_tag_by_id(tag_id)
    data = {}
    data['similar'] = tag.get_dishes()
    return json.dumps(data)

@app.route("/get_image/<string:filename>")
def send_image(filename):
    path = os.path.join(DISH_IMAGE_PATH, filename)
    return send_file(path)

if __name__ == "__main__":
    # Change debug to False when deploying, probably.
    app.run(debug = True)

