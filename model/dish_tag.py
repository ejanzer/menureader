from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base

class Dish_Tag(Base):
    __tablename__ = "dish_tags"

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    rest_dish_id = Column(Integer, ForeignKey('rest_dishes.id')) 

    tag = relationship("Tag", backref=backref("dish_tags", order_by=id))
    dish = relationship("Dish", backref=backref("dish_tags", order_by=id))
    rest_dish = relationship("Rest_Dish", backref=backref("dish_tags", order_by=id))