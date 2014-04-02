import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base, db_session
from date import format_date
from image import Image

import config

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    eng_name = Column(String(64), nullable=False)
    chin_name = Column(String(64), nullable=False)
    pinyin = Column(String(64), nullable=True)
    desc = Column(String(64), nullable=True)

    def get_json(self):
        data = {}
            
        dish = [
                {'title':'Chinese', 'data': self.chin_name},
                {'title': 'English', 'data': self.eng_name},
                ]

        if self.desc:
            dish.append({'title': 'description', 'data': self.desc})

        if self.pinyin:
            dish.append({'title': 'pinyin', 'data': self.pinyin})

        data['dish'] = dish

        if self.reviews:
            reviews = []
            for review in self.reviews:
                print review
                print "Rest dish id: ", review.rest_dish.id
                print review.rest_dish.restaurant
                print review.rest_dish.rest_id
                print review.rest_dish.dish_id
                print review.rest_dish.dish.eng_name
                review_data = {
                    'username': review.user.username,
                    'date': format_date(review.date),
                    'text': review.text,
                    'restaurant': review.rest_dish.restaurant.name
                }

                reviews.append(review_data)

            # reviews = [{"username": review.user.username, "date": format_date(review.date), "text": review.text, "restaurant": review.rest_dish.restaurant.name} for review in self.reviews]
            data['reviews'] = reviews

        if self.images:
            images = [Image.get_json(image.filename) for image in self.images]
            data['images'] = images

        if self.dish_tags:
            tags_dict = {}
            for dish_tag in self.dish_tags:
                name = dish_tag.tag.name
                tag_id = dish_tag.tag.id
                if tags_dict.get(name):
                    tags_dict[name] += 1
                else:
                    tags_dict[name] = 1

            tags = [{'tag': name, 'count': str(count)} for name, count in tags_dict.iteritems()]
            data['tags'] = tags

        print data.keys()
        return data

    def get_json_min(self):
        similar = {'title': self.chin_name, 'data': self.eng_name }
        return similar

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

    @staticmethod
    def get_all_dishes():
        dish_names = []
        dishes = db_session.query(Dish).all()
        for dish in dishes:
            dish_names.append(dish.chin_name)
        return dish_names



