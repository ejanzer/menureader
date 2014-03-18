import sqlalchemy

import csv
from base import Base, engine, db_session
from dict_entry import Dict_Entry
from dish import Dish
from food_word import Food_Word

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
    pass

def seed_reviews():
    """Seed reviews with test data."""
    pass

def seed_tags():
    """Seed tags with test data."""
    pass

def seed_restaurants():
    """Seed restaurants with test data."""
    pass

if __name__ == "__main__":
    # Uncomment and run as main to seed entire database.
    # Or, run in interactive mode and call the function for the table you want to seed.
    # seed_cedict()
    # seed_dishes()
    seed_food_words()
    # seed_users()
    # seed_reviews()
    # seed_tags()
    # seed_restaurants()


