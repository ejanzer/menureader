from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base

class Food_Word(Base):
    __tablename__ = "food_words"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(64), nullable=False)
    pinyin = Column(String(64), nullable=True)
    english = Column(String(64), nullable=False)