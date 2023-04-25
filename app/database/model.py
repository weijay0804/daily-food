'''
Author: weijay
Date: 2023-04-24 20:34:28
LastEditors: weijay
LastEditTime: 2023-04-26 01:21:10
Description: 定義  DataBase ORM 模型
'''

from typing import Union
from datetime import datetime

from sqlalchemy import Index, String, Integer, Column, Text, Float, DateTime, Boolean

from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), server_default=None)
    lat = Column(Float, nullable=False, index=True)
    lng = Column(Float, nullable=False)
    is_enable = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, server_default=None)

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
