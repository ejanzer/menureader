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
            tags_dict = {}
            for dish_tag in self.dish_tags:
                name = dish_tag.tag.name
                if tags_dict.get(name):
                    tags_dict[name] += 1
                else:
                    tags_dict[name] = 1

            tags = {name: count for name, count in tags_dict.iteritems()}
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
        word_list = []
        for char in word:
            word_list.append(char)

        for i in range(len(word)):
            temp = word_list[i]
            word_list[i] = '%'
            new_word = ''.join(word_list)

            similar = db_session.query(Dish).filter(Dish.chin_name.like(new_word)).all()
            results.extend(similar)
            word_list[i] = temp

        return results


