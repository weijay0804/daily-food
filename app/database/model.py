'''
Author: weijay
Date: 2023-04-24 20:34:28
LastEditors: andy
LastEditTime: 2023-06-10 13:54:20
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
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# restaurant 與 restaurant_type 多對多中間表
restaurant_type_intermediary_table = Table(
    "restaurant_type_intermediay",
    Base.metadata,
    Column("restaurant_id", Integer, ForeignKey("restaurant.id"), primary_key=True),
    Column("restaurant_type_id", Integer, ForeignKey("restaurant_type.id"), primary_key=True),
)

# user 與 restaurant 多對多中間表
user_restaurant_intermediary_table = Table(
    "user_restaurant_intermediary",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("restaurant_id", Integer, ForeignKey("restaurant.id"), primary_key=True),
)


class Restaurant(Base):
    """餐廳表"""

    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    address = Column(Text, nullable=False)
    phone = Column(String(20), server_default=None)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    desc = Column(Text, server_default=None)
    price = Column(Integer, server_default=None)
    is_enable = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, server_default=None, onupdate=datetime.utcnow)

    # 與 restaurant_open_time table 建立一對多關係
    open_times = relationship(
        "RestaurantOpenTime",
        back_populates="restaurant",
        cascade="delete, delete-orphan",
        lazy="joined",
    )

    # 與 restaurant_type table 建立多對多關係
    types = relationship(
        "RestaurantType",
        secondary=restaurant_type_intermediary_table,
        back_populates="restaurants",
        lazy="joined",
    )

    # 與 user table 建立多對多關係
    users = relationship(
        "User",
        secondary=user_restaurant_intermediary_table,
        back_populates="restaurants",
    )

    __table_args__ = (Index("idx_lat_lng", "lat", "lng"),)

    def __init__(
        self,
        name: str,
        address: str,
        lat: float,
        lng: float,
        phone: Union[str, None] = None,
        desc: Union[str, None] = None,
        price: Union[int, None] = None,
    ):
        self.name = name
        self.address = address
        self.phone = phone
        self.lat = lat
        self.lng = lng
        self.desc = desc
        self.price = price

    def __repr__(self):
        return f"Data in restaurant table, name = {self.name}"


class RestaurantOpenTime(Base):
    """餐廳營業時間表"""

    __tablename__ = "restaurant_open_time"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, server_default=None, onupdate=datetime.utcnow)

    # 與 restaurant talbe 建立多對一關係
    restaurant = relationship("Restaurant", back_populates="open_times")

    __table_args__ = (
        Index('idx_restaurant_id_day_of_week', 'restaurant_id', 'day_of_week'),
        Index('idx_restaurant_id', 'restaurant_id'),
    )

    def __init__(self, day_of_week: int, open_time: time, close_time: time):
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


class RestaurantType(Base):
    """餐廳種類表"""

    __tablename__ = "restaurant_type"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    desc = Column(Text, server_default=None)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, server_default=None, onupdate=datetime.utcnow)

    # 與 restaurant 建立多對多關係
    restaurants = relationship(
        "Restaurant",
        secondary=restaurant_type_intermediary_table,
        back_populates="types",
        lazy="dynamic",
    )

    def __init__(self, name: str, desc: str):
        self.name = name
        self.desc = desc


class User(Base):
    """使用者表"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, index=True, unique=True)
    email = Column(String(128), nullable=False, index=True, unique=True)
    password_hash = Column(String(128), server_default=None)
    is_oauth = Column(Boolean, default=False)
    is_enable = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, server_default=None, onupdate=datetime.utcnow)

    # 與 restaurant table 建立多對多關係
    restaurants = relationship(
        "Restaurant",
        secondary=user_restaurant_intermediary_table,
        back_populates="users",
        lazy="dynamic",
    )

    # 與 oauth table 建立一對一關係 ( 只有在 is_oauth = true 時會建立關係 )
    oauth = relationship("OAuth", uselist=False, back_populates="user", cascade="delete, delete")

    def __init__(
        self,
        username: str,
        email: str,
        password_hash: Union[str, None] = None,
        is_oauth: Union[bool, None] = False,
    ):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_oauth = is_oauth


class OAuth(Base):
    """使用者 OAuth 表 (只有在使用者用 OAuth 登入時才會有資料)"""

    __tablename__ = "oauth"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    provider = Column(String(30), nullable=False)
    access_token = Column(String(128), nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, server_default=None, onupdate=datetime.utcnow)

    # 與 user table 建立一對一關係 ( 只有在 user.is_oauth = true 會建立關係 )
    user = relationship("User", back_populates="oauth")
