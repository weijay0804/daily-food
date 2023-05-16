'''
Author: weijay
Date: 2023-05-15 20:03:52
LastEditors: weijay
LastEditTime: 2023-05-15 22:03:49
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


class RestaurantOpenTimeDBModel(BaseModel):
    """要建立 restaurant_open_time table 的資料時的 schemas model"""

    day_of_week: int
    open_time: datetime.time
    close_time: datetime.time
