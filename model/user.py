import bcrypt

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base, db_session
from date import format_date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password


    @staticmethod
    def create_user(username, password, password_verify):
        if password != password_verify:
            return "Error: Passwords do not match."

        user = db_session.query(User).filter_by(username=username)

        if user:
            return "Error: User already exists."

        user = User(username=username)
        user.set_password(password)
        db_session.add(user)
        db_session.commit()

        return "User created."

    @staticmethod
    def get_user_by_id(user_id):
        return db_session.query(User).get(user_id)

    @staticmethod
    def jsonify(user):
        reviews = []
        if user.reviews != []:
            reviews = [{'restaurant': review.rest_dish.restaurant.name, 'dish': review.dish.eng_name, 'date': format_date(review.date), 'text': review.text} for review in user.reviews]

        data = {
            'username': user.username,
            'reviews': reviews
        }
        return data
