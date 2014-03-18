from base import Base, engine

from dict_entry import Dict_Entry
from dish import Dish
from dish_tag import Dish_Tag
from food_word import Food_Word
from image import Image
from rest_dish import Rest_Dish
from restaurant import Restaurant
from review import Review
from tag import Tag
from user import User

def main():
    # Uncomment and run model.py as main to create schema
    Base.metadata.create_all(engine) 

if __name__ == "__main__":
    main()