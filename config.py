import os

# Config file
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///menureader.db")
SECRET_KEY = "shhhhitsasecret"