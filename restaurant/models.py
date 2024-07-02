from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

from config.db import Model
from core.utils import TimestampMixin


class Restaurant(Model, TimestampMixin):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))
    phone = Column(String, nullable=True)

    owner = relationship('User')
    addresses = relationship('Address', back_populates='restaurant', cascade='all, delete-orphan')
    menus = relationship('Menu', back_populates='restaurant', cascade='all, delete-orphan')


class Address(Model, TimestampMixin):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    phone = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    restaurant = relationship('Restaurant', back_populates='addresses')


class Menu(Model, TimestampMixin):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    todaysmenu = Column(Boolean, default=False)

    restaurant = relationship('Restaurant', back_populates='menus')
    items = relationship('MenuItem', back_populates='menu', cascade='all, delete-orphan')


class MenuItem(Model, TimestampMixin):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    menu_id = Column(Integer, ForeignKey('menus.id'))

    menu = relationship('Menu', back_populates='items')
    images = relationship('MenuItemImage', back_populates='menu_item', cascade='all, delete-orphan')


class MenuItemImage(Model):
    __tablename__ = 'menu_item_images'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))

    menu_item = relationship('MenuItem', back_populates='images')
