'''
Author: weijay
Date: 2023-04-25 17:19:24
LastEditors: weijay
LastEditTime: 2023-04-27 16:10:15
Description: 放一些測試時會用到的通用函示
'''

import random
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.model import Base

from . import _fake_data


class FakeData:
    """用來建立隨機測試資料"""

    def fake_restaurant(is_lat_lng: bool = True):
        result = {}

        name = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME)
        address = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_ADDRESS)

        if is_lat_lng:
            lat, lng = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_LAT_LNG)
            result.update({"lat": lat, "lng": lng})

        result.update({"name": name, "address": address})

        return result


class FakeDataBase:
    """產生測試資料庫"""

    SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

    def __init__(self):
        self.engine = create_engine(
            self.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )

        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        self.Base = Base

    def override_get_db(self):
        try:
            db = self.SessionLocal()
            yield db

        finally:
            db.close()

    @contextmanager
    def get_db(self):
        try:
            db = self.SessionLocal()
            yield db

        finally:
            db.close()
