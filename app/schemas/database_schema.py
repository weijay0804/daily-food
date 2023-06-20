'''
Author: weijay
Date: 2023-05-15 20:03:52
LastEditors: andy
LastEditTime: 2023-06-20 02:45:52
Description: 針對 database 中的 table 定義的 schemas
'''

import datetime
from pydantic import BaseModel
from typing import Optional


class RestaurantDBModel(BaseModel):
    """要建立 restaurant table 的資料時的 schemas model"""

    name: str
    address: str
    phone: Optional[str] = None
    lat: float
    lng: float
    desc: Optional[str] = None
    price: Optional[int] = None


class RestaurantUpdateDBModel(BaseModel):
    """要更新 restaurant table 的資料時的 schames model"""

    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    desc: Optional[str] = None
    price: Optional[int] = None


class RestaurantOpenTimeDBModel(BaseModel):
    """要建立 restaurant_open_time table 的資料時的 schemas model"""

    day_of_week: int
    open_time: datetime.time
    close_time: datetime.time


class RestaurantOpenTimeUpdateDBModel(BaseModel):
    """要更新 restaurant_open_time table 的資料時的 schames model"""

    day_of_week: Optional[int] = None
    open_time: Optional[datetime.time] = None
    close_time: Optional[datetime.time] = None


class UserNotOAuthDBModel(BaseModel):
    """要建立不是使用 OAuth 註冊時的 user"""

    username: str
    email: str
    password: str
    is_oauth: int = 0
