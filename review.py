from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    rest_dish_id = Column(Integer, ForeignKey('rest_dishes.id'))
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    text = Column(String(64), nullable=True)
    date = Column(Date, nullable=False)

    user = relationship("User", backref=backref("reviews", order_by=id))
    dish = relationship("Dish", backref=backref("reviews", order_by=id))
    rest_dish = relationship("Rest_Dish", backref=backref("reviews", order_by=id))