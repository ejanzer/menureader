from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base, db_session

class Dict_Entry(Base):
    __tablename__ = "dict_entries"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(64), nullable=False)
    traditional = Column(String(64), nullable=True)
    pinyin = Column(String(64), nullable=True)
    definition = Column(String(64), nullable=False)

    def get_json(self):
        d = {
            'char': self.simplified,
            'pinyin': self.pinyin,
            'english': self.definition
        }
        return d

    @staticmethod
    def find_matches(word):
        return db_session.query(Dict_Entry).filter_by(simplified=word).all()
