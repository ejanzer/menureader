from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base

class Dict_Entry(Base):
    __tablename__ = "dict_entries"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(64), nullable=False)
    traditional = Column(String(64), nullable=True)
    pinyin = Column(String(64), nullable=True)
    definition = Column(String(64), nullable=False)