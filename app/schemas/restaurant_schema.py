'''
Author: weijay
Date: 2023-04-24 17:08:09
LastEditors: weijay
LastEditTime: 2023-05-15 20:30:14
Description: 定義 restaurant router 的數據模型
'''

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
