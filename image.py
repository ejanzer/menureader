from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

# class Image(Base):
#     __tablename__ = "images"

#     id = Column(Integer, primary_key=True)
#     rest_dish_id = Column(Integer, ForeignKey('rest_dishes.id'))

#     rest_dish = relationship("Rest_Dish", backref=backref("images", order_by=id))

