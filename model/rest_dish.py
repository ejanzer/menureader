from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base

class Rest_Dish(Base):
    __tablename__ = "rest_dishes"

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    rest_id = Column(Integer, ForeignKey('restaurants.id'))

    dish = relationship("Dish", backref=backref("rest_dishes", order_by=id))
    restaurant = relationship("Restaurant", backref=backref("rest_dishes", order_by=id))