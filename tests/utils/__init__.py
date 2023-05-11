'''
Author: weijay
Date: 2023-04-25 17:19:24
LastEditors: weijay
LastEditTime: 2023-05-11 21:47:38
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
        """生成假餐廳資料，比較近的

        這裡的比較近是指使用 `fake_current_location()` 生成目標位置
        使用 `fake_restaurant()` 生成的餐廳資料，會座落在目標位置附近

        簡而言之，如果使用 `fake_restaurant()` 生成餐廳位置，如果要測試在目標範圍內的餐廳，就使用 `fake_current_location()` ( 5KM 內 )
        """
        result = {}

        name = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME)
        address = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_ADDRESS)

        if is_lat_lng:
            lat, lng = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_LAT_LNG)
            result.update({"lat": lat, "lng": lng})

        result.update({"name": name, "address": address})

        return result

    def fake_restaurant_far(is_lat_lng: bool = True):
        """生成假餐廳資料，比較遠的

        這裡的比較遠是指使用 `fake_cureent_location()` 生成的目標位置
        使用 `fake_restaurant_far()` 生成的餐廳資料，會座落在目標位置很遠的地方

        簡而言之，如果使用 `fake_restaurant_far()` 生成餐廳位置，如果要測試不在目標範圍內的餐廳，就用 `fake_current_location_far()`
        """
        result = {}

        name = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME_FAR)
        address = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_ADDRESS_FAR)

        if is_lat_lng:
            lat, lng = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_LAT_LNG_FAR)
            result.update({"lat": lat, "lng": lng})

        result.update({"name": name, "address": address})

        return result

    def fake_current_location():
        """生成目標位置

        如果要測試在附近的餐廳，使用 `fake_restaurant()` ( 5KM 內 )
        """

        fake_location = [(24.94409, 121.22538), (24.94442, 121.22347), (24.94135, 121.22447)]

        return random.choice(fake_location)

    def fake_current_location_far():
        """生成目標位置

        如果要測試在附近的餐廳，使用 `fake_restaurant_far()` ( 5KM 內 )
        """

        fake_location = [(22.98856, 120.23490), (22.98892, 120.23356), (22.98796, 120.23541)]

        return random.choice(fake_location)

    def fake_restaurant_open_time():
        """生成假餐廳營業時間

        ( 不會包括 restaurant_id 欄位，需要自己增加，因為考慮之後會要根據 restaurant 的資料來關聯)

        """

        day_of_week = random.choice(_fake_data.FakeRestaurantOpenTimeData.DAY_OF_WEEK)
        open_time = random.choice(_fake_data.FakeRestaurantOpenTimeData.OPEN_TIME)
        close_time = random.choice(_fake_data.FakeRestaurantOpenTimeData.CLOSE_TIME)

        return {"day_of_week": day_of_week, "open_time": open_time, "close_time": close_time}


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
