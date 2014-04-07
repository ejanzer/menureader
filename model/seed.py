import sqlalchemy
import os
import datetime

import csv
from base import Base, engine, db_session
from dict_entry import Dict_Entry
from dish import Dish
from food_word import Food_Word
from user import User
from review import Review 
from dish_tag import Dish_Tag 
from rest_dish import Rest_Dish 
from restaurant import Restaurant
from image import Image
from tag import Tag

def seed_cedict():
    """Seed the Chinese/English dictionary with data from CEDICT."""
    with open('seeds/cedict3.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            if row[0] == '#':
                continue
            else:
                for i in range(len(row)):
                    row[i] = row[i].decode('utf-8')

                trad, simp, pinyin = row[0], row[1], row[2]
                definition = ''.join(row[3:])
                pinyin = pinyin.strip('"')
                definition = definition.strip('"')

                entry = Dict_Entry(simplified=simp, traditional=trad, pinyin=pinyin, definition=definition)
                db_session.add(entry)
        try: 
            db_session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            db_session.rollback()

def seed_dishes():
    """Seed dishes table with common dish names from Dianping and others."""
    with open('seeds/dishes_seed.txt', 'rb') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].decode('utf-8')
                row[i] = row[i].strip()

            chin_name = row[0]
            eng_name = row[1].lower()
            if len(row) > 2:
                desc = row[2]
                dish = Dish(chin_name=chin_name, eng_name=eng_name, desc=desc)                                            
            else:
                dish = Dish(chin_name=chin_name, eng_name=eng_name)
            db_session.add(dish)

        try: 
            db_session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            db_session.rollback()


def seed_food_words():
    """Seed food_words table with common food words."""
    with open('seeds/food_words_seed.txt', 'rb') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].decode('utf-8')
                row[i] = row[i].strip()

            simplified = row[0]
            english = row[1].lower()

            food_word = Food_Word(simplified=simplified, english=english)
            db_session.add(food_word)

        try: 
            db_session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            db_session.rollback()

def seed_users():
    """Seed users with test users."""

    emilypass = os.environ.get("EMILYPASS")
    emily = User(username='emily')
    emily.set_password(emilypass)

    nickpass = os.environ.get("NICKPASS")
    nick = User(username="nick")
    nick.set_password(nickpass)

    db_session.add(emily)
    db_session.add(nick)
    db_session.commit()

def seed_restaurants():
    """Seed restaurants with test data."""
    r1 = Restaurant(name="Chef Zhao's")
    r2 = Restaurant(name="Fu Lam Mum")
    r3 = Restaurant(name="Chef Chu's")
    r4 = Restaurant(name="Queen House")
    r5 = Restaurant(name="Cafe Macs")
    db_session.add(r1)
    db_session.add(r2)
    db_session.add(r3)
    db_session.add(r4)
    db_session.commit()

def seed_reviews():
    """Seed reviews with test data."""

    ##### Add a review for Hot and Sour Soup at Fu Lam Mum from Emily. #####
    add_review(1, 199, 2, 1, "too spicy!")

    ##### Add a review for Hot and Sour Soup at Fu Lam Mum from Emily. #####
    add_review(1, 199, 2, 1, "too spicy!")

    ##### Add a review for Kung Pao Chicken at Cafe Macs from Nick. #####
    add_review(2, 3, 5, 2, "Very peanut\nMuch tasty\nWow")

    ##### Add a review for Chongqing Chicken at Chef Zhao's from Emily. #####
    add_review(1, 83, 1, 1, "Yum! Spicy AND numbing. Best fried chicken ever.")

    ##### Add a review for beef noodles at Queen House from Emily. #####
    add_review(1, 1, 4, 4, "Really good. Beef is a little fatty, but homemade noodles are delicious. Huge portions!")

    ##### Add a review for Hot and Sour Soup at Queen House from Nick. #####
    add_review(2, 199, 4, 5, "Delicious!")

    ##### Add a review for mapo tofu at Chef Zhao's from Emily. #####
    add_review(1, 2, 1, 1, "Tastes just like Chen's mapo tofu in Chengdu!")

def add_review(user_id, dish_id, rest_id, tag_id, text):
    now = datetime.datetime.now()

    rest_dish = Rest_Dish(dish_id=dish_id, rest_id=rest_id)
    db_session.add(rest_dish)
    db_session.commit()

    dish_tag = Dish_Tag(dish_id=dish_id, tag_id=tag_id, rest_dish_id=rest_dish.id)
    db_session.add(dish_tag)
    db_session.commit()

    review = Review(user_id=user_id, rest_dish_id=rest_dish.id, dish_id=dish_id, text=text, date=now)
    db_session.add(review)
    db_session.commit()


def seed_tags():
    """Seed tags with test data."""
    tags = [
        Tag(name="spicy"),
        Tag(name="chicken"),
        Tag(name="pork"),
        Tag(name="beef"),
        Tag(name="vegetarian"),
        Tag(name="fish")
    ]

    for tag in tags:
        db_session.add(tag)

    db_session.commit()

def create_new_tag(dish_id, rest_id, tag_id):
    """Add more tags"""
    rest_dish = Rest_Dish(dish_id=dish_id, rest_id=rest_id)
    db_session.add(rest_dish)
    db_session.commit()

    dish_tag = Dish_Tag(dish_id=dish_id, tag_id=tag_id, rest_dish_id=rest_dish.id)
    db_session.add(dish_tag)
    db_session.commit()

def seed_additional_tags():
    """Add some more tags"""

    # Tag yuxiang eggplant as vegetarian
    create_new_tag(dish_id=327, rest_id=1, tag_id=5)

    # Tag Mapo tofu as having beef
    create_new_tag(2, 1, 4)

    # Tag maoxuewang as having pork
    create_new_tag(6, 1, 3)

    # Tag kung pao chicken has being spicy, again
    create_new_tag(3, 1, 1)

    # Tag kung pao chicken as having chicken
    create_new_tag(3, 1, 2)

    # Tag chongqing chicken as being spicy
    create_new_tag(83, 1, 1)

    # Tag chongqing chicken has having chicken
    create_new_tag(83, 1, 2)


def seed_images():
    with open("seeds/images_seed.txt") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            dish_id = row[0]
            filename = row[1].strip()

            image = Image(dish_id=dish_id, filename=filename)
            db_session.add(image)

    try: 
        db_session.commit()
    except sqlalchemy.exc.IntegrityError, e:
        db_session.rollback()

if __name__ == "__main__":
    # Uncomment and run as main to seed entire database.
    # Or, run in interactive mode and call the function for the table you want to seed.
    # seed_cedict()
    # seed_dishes()
    # seed_food_words()
    # seed_users()
    # seed_tags()
    # seed_restaurants()
    # seed_reviews()
    # seed_additional_tags()
    # seed_images()
    pass


