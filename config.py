import os

# Config file
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///menureader.db")
SECRET_KEY = os.environ.get("SECRET_KEY", "shhhhhhhhh")
DISH_IMAGE_PATH = os.environ.get("DISH_IMAGE_PATH", './dish_images/')
UPLOAD_FOLDER = os.environ.get("IMAGE_UPLOAD_PATH", './image_uploads/')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
LANG = os.environ.get("lang", "chi_sim")
PORT = int(os.environ.get("PORT", 5000))
