import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base, db_session

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    eng_name = Column(String(64), nullable=False)
    chin_name = Column(String(64), nullable=False)
    pinyin = Column(String(64), nullable=True)
    desc = Column(String(64), nullable=True)

    @staticmethod
    def get_dish_by_id(id):
        dish = db_session.query(Dish).get(id)
        data = {
            'dish': {
                'id': dish.id,
                'chin_name': dish.chin_name,
                'eng_name': dish.eng_name,
            }
        }
        if dish.reviews:
            reviews = [{'username': review.user.username, 'date': datetime.datetime.strftime(review.date, '%D'), 'text': review.text} for review in dish.reviews]
            data['dish']['reviews'] = reviews

        if dish.dish_tags:
            tags = [dish_tag.tag.name for dish_tag in dish.dish_tags]
            data['dish']['tags'] = tags

        return data