'''
Author: weijay
Date: 2023-04-24 17:08:09
LastEditors: weijay
LastEditTime: 2023-07-03 23:38:53
Description: 定義 restaurant router 的數據模型
'''

from typing import Optional, List
from pydantic import BaseModel


class _OpenTimeBaseModel(BaseModel):
    """餐廳營業時間基本 schemas model"""

    day_of_week: int
    open_time: str
    close_time: str


class _OpenTimeInDBModel(_OpenTimeBaseModel):
    """對應 restaurant_open_time table 的 schemas model"""

    id: int

    class Config:
        orm_model = True


class OnCreateOpenTimeModel(BaseModel):
    """建立餐廳營業時間的 schemas model"""

    items: List[_OpenTimeBaseModel]


class OnUpadteOpenTimeModel(BaseModel):
    """更新餐廳營業時間時的 schemas model"""

    day_of_week: Optional[int] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None


class _BaseModel(BaseModel):
    """餐廳基本 schemas model"""

    name: str
    address: str
    phone: Optional[str] = None
    desc: Optional[str] = None
    price: Optional[int] = None


class RestaurantInDBModel(_BaseModel):
    """對應 restaurant table 的 schemas model"""

    id: int
    lat: float
    lng: float

    class Config:
        orm_mode = True


class _OnReadsModel(RestaurantInDBModel):
    """餐廳基本 schemas 但新增了 `is_open` 欄位，用於回傳多個 restaurant 時"""

    is_open: bool = True


class OnReadsModel(BaseModel):
    """取得多個餐廳時的 schemas model"""

    items: List[_OnReadsModel]


class OnReadModel(RestaurantInDBModel):
    """取得特定一筆餐廳時的 schemas model"""

    open_times: List[_OpenTimeInDBModel]


class OnCreateModel(_BaseModel):
    """新增一筆簪聽資料時的 schemas model"""

    open_times: Optional[List[_OpenTimeBaseModel]] = None


class OnUpdateModel(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    desc: Optional[str] = None
    price: Optional[int] = None
