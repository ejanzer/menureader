import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base, db_session
from date import format_date

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    eng_name = Column(String(64), nullable=False)
    chin_name = Column(String(64), nullable=False)
    pinyin = Column(String(64), nullable=True)
    desc = Column(String(64), nullable=True)

    def get_json(self):
        data = {
            'dish': {
                'id': self.id,
                'chin_name': self.chin_name,
                'eng_name': self.eng_name,
            }
        }
        if self.reviews:
            reviews = [{'username': review.user.username, 'date': format_date(review.date), 'text': review.text} for review in self.reviews]
            data['dish']['reviews'] = reviews

        if self.dish_tags:
            tags = [dish_tag.tag.name for dish_tag in self.dish_tags]
            data['dish']['tags'] = tags

        return data

    @staticmethod
    def get_dish_by_id(id):
        dish = db_session.query(Dish).get(id)
        return dish

    @staticmethod
    def find_match(word):
        return db_session.query(Dish).filter_by(chin_name=word).first()

    @staticmethod
    def find_similar(word):
        results = []
        # TODO
        return results


