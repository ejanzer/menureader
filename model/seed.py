import model
from base import Base, engine, db_session

def seed_cedict():
    """Seed the Chinese/English dictionary with data from CEDICT."""
    pass

def seed_dishes():
    """Seed dishes table with common dish names from Dianping and others."""
    pass

def seed_food_words():
    """Seed food_words table with common food words."""
    pass

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
    seed_cedict()
    seed_dishes()
    seed_food_words()
    seed_users()
    seed_reviews()
    seed_tags()
    seed_restaurants()