from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    rest_dish_id = Column(Integer, ForeignKey('rest_dishes.id'))
    review_id = Column(Integer, ForeignKey('reviews.id'))
    path = Column(Integer, nullable=False)

    rest_dish = relationship("Rest_Dish", backref=backref("images", order_by=id))
    review = relationship("Review", backref=backref("images", order_by=id))

