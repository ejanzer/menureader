from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from base import Base

import os
import config
import base64

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    filename = Column(Integer, nullable=False)

    dish = relationship("Dish", backref=backref("images", order_by=id))

    @staticmethod
    def get_json(filename):
        path = os.path.join(config.DISH_IMAGE_PATH, filename)
        print path
        with open(path) as im:
            image_data = im.read()
        print len(image_data)
        if image_data:
            return {'filename': filename, 'data': base64.b64encode(image_data)}
        
        return {}

