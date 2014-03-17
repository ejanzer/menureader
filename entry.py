from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Entry(Base):
    __tablename__ = "cedict"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(64))
    traditional = Column(String(64))
    pinyin = Column(String(64))
    definition = Column(String(64))