'''
Author: weijay
Date: 2023-04-24 17:08:09
LastEditors: weijay
LastEditTime: 2023-04-24 19:32:28
Description: 定義 restaurant router 的數據模型
'''

from typing import Union, List

from pydantic import BaseModel


class ResBase(BaseModel):
    name: str
    address: str
    phone: Union[str, None] = None


class ResModel(ResBase):
    id: int
    lat: float
    lng: float
    is_enable: Union[bool, None] = True


class ResCreateModel(BaseModel):
    items: List[ResBase]


class ResReadModel(BaseModel):
    items: List[ResModel]
