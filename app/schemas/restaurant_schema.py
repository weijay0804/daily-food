'''
Author: weijay
Date: 2023-04-24 17:08:09
LastEditors: weijay
LastEditTime: 2023-04-27 01:24:05
Description: 定義 restaurant router 的數據模型
'''

from datetime import datetime
from typing import Union, List

from pydantic import BaseModel


class ResBase(BaseModel):
    """基本的 restaurant 資料架構"""

    name: str
    address: str
    phone: Union[str, None] = None


class ResModel(ResBase):
    """對應到在資料庫中的 restaurant 資料架構"""

    id: int
    is_enable: Union[bool, None] = True
    create_at: datetime
    update_at: datetime = None

    class Config:
        orm_mode = True


class ResCreateModel(ResBase):
    """新增餐廳時的資料架構"""

    pass


class ResFullCreateModel(ResBase):
    """新增餐廳到資料庫中的架構，就是多了 lat 和 lng 資料"""

    lat: float
    lng: float


class ResReadModel(BaseModel):
    """取得聽餐廳時的資料架構"""

    items: List[ResModel]
