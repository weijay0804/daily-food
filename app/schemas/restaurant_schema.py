'''
Author: weijay
Date: 2023-04-24 17:08:09
LastEditors: weijay
LastEditTime: 2023-05-22 19:03:08
Description: 定義 restaurant router 的數據模型
'''

import datetime
from typing import Union, List

from pydantic import BaseModel


class __BaseModel(BaseModel):
    """餐廳基本 schemas model"""

    name: str
    address: str
    phone: Union[str, None] = None


class RestaurantModel(__BaseModel):
    """對應 restaurant table 的 schemas model"""

    id: int
    lat: float
    lng: float

    class Config:
        orm_mode = True


class WithIsOpenModel(RestaurantModel):
    """餐廳基本 schemas 但新增了 `is_open` 欄位，用於回傳多個 restaurant 時"""

    is_open: bool = True


class ReadsModel(BaseModel):
    """取得多個餐廳資料時的 schemas model"""

    items: List[WithIsOpenModel]


class ReadModel(RestaurantModel):
    """取得特定一筆餐廳時的 schemas model"""

    pass


class CreateOrUpdateModel(__BaseModel):
    """新增一筆簪聽資料時的 schemas model"""

    pass


class UpdateModel(BaseModel):
    name: Union[str, None] = None
    address: Union[str, None] = None
    phone: Union[str, None] = None


class OpenTimeBaseModel(BaseModel):
    """餐廳營業時間基本 schemas model"""

    day_of_week: int
    open_time: datetime.time
    close_time: datetime.time


class OpenTimeModel(OpenTimeBaseModel):
    """對應 restaurant_open_time table 的 schemas model"""

    id: int

    class Config:
        orm_model = True


class ReadsOpenTimeModel(BaseModel):
    """取得餐廳營業時間時的 schemas model"""

    items: List[OpenTimeModel]


class CreateOpenTimeModel(BaseModel):
    """新增餐廳營業時間時的 schemas model (為了方便，設計成一次可以建立多個營業時間)"""

    items: List[OpenTimeBaseModel]


class UpdateOpenTimeModel(BaseModel):
    """更新餐廳營業時間時的 schemas model"""

    day_of_week: Union[int, None] = None
    open_time: Union[datetime.time, None] = None
    close_time: Union[datetime.time, None] = None
