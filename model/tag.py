from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base, db_session

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    def get_dishes(self):
        if self.dish_tags:
            dishes = [dish_tag.dish.get_json_min() for dish_tag in self.dish_tags]  
            return dishes        
        return None

    @staticmethod
    def get_tag_by_name(name):
        return db_session.query(Tag).filter_by(name=name).first()

    @staticmethod
    def get_tag_by_id(id):
        return db_session.query(Tag).get(id)
