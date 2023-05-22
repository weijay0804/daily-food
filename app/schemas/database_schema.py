'''
Author: weijay
Date: 2023-05-15 20:03:52
LastEditors: weijay
LastEditTime: 2023-05-22 18:58:20
Description: 針對 database 中的 table 定義的 schemas
'''

import datetime
from pydantic import BaseModel
from typing import Union


class RestaurantDBModel(BaseModel):
    """要建立 restaurant table 的資料時的 schemas model"""

    name: str
    address: str
    phone: Union[str, None] = None
    lat: float
    lng: float


class RestaurantUpdateDBModel(BaseModel):
    """要更新 restaurant table 的資料時的 schames model"""

    name: Union[str, None] = None
    address: Union[str, None] = None
    phone: Union[str, None] = None
    lat: Union[float, None] = None
    lng: Union[float, None] = None


class RestaurantOpenTimeDBModel(BaseModel):
    """要建立 restaurant_open_time table 的資料時的 schemas model"""

    day_of_week: int
    open_time: datetime.time
    close_time: datetime.time


class RestaurantOpenTimeUpdateDBModel(BaseModel):
    """要更新 restaurant_open_time table 的資料時的 schames model"""

    day_of_week: Union[int, None] = None
    open_time: Union[datetime.time, None] = None
    close_time: Union[datetime.time, None] = None
