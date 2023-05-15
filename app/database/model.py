'''
Author: weijay
Date: 2023-04-24 20:34:28
LastEditors: weijay
LastEditTime: 2023-05-15 22:38:47
Description: 定義  DataBase ORM 模型
'''

from typing import Union
from datetime import datetime, time

from sqlalchemy import (
    Index,
    String,
    Integer,
    Column,
    Text,
    Float,
    DateTime,
    Boolean,
    Time,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), server_default=None)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    is_enable = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, server_default=None)

    open_times = relationship(
        "RestaurantOpenTime", back_populates="restaurant", cascade="all, delete"
    )

    __table_args__ = (Index("idx_lat_lng", "lat", "lng"),)

    def __init__(
        self,
        name: str,
        address: str,
        lat: float,
        lng: float,
        phone: Union[str, None] = None,
    ):
        self.name = name
        self.address = address
        self.phone = phone
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return f"Data in restaurant table, name = {self.name}"


class RestaurantOpenTime(Base):
    __tablename__ = "restaurant_open_time"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, server_default=None)

    restaurant = relationship("Restaurant", back_populates="open_times")

    __table_args__ = (
        Index('idx_restaurant_id_day_of_week', 'restaurant_id', 'day_of_week'),
        Index('idx_restaurant_id', 'restaurant_id'),
    )

    def __init__(self, restaurant_id: int, day_of_week: int, open_time: time, close_time: time):
        self.restaurant_id = restaurant_id
        self.day_of_week = day_of_week
        self.open_time = time(hour=open_time.hour, minute=open_time.minute)
        self.close_time = time(hour=close_time.hour, minute=close_time.minute)

    def to_dict(self):
        """把 ORM object 轉換成 dict"""

        return {
            "id": self.id,
            "day_of_week": self.day_of_week,
            "open_time": self.open_time,
            "close_time": self.close_time,
        }
