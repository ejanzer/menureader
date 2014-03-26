from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base, db_session

class Food_Word(Base):
    __tablename__ = "food_words"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(64), nullable=False)
    pinyin = Column(String(64), nullable=True)
    english = Column(String(64), nullable=False)

    def get_json(self):
        d = {
            "char": self.simplified,
            "pinyin": self.pinyin,
            "english": self.english
        }
        return d

    @staticmethod
    def find_match(word):
        return db_session.query(Food_Word).filter_by(simplified=word).first()

    @staticmethod
    def get_all_words():
        words = []
        food_words = db_session.query(Food_Word).all()
        for word in food_words:
            words.append(word.simplified)
        return words
