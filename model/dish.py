from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    eng_name = Column(String(64), nullable=False)
    chin_name = Column(String(64), nullable=False)
    pinyin = Column(String(64), nullable=True)
    desc = Column(String(64), nullable=True)