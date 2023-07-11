'''
Author: weijay
Date: 2023-04-25 17:19:24
LastEditors: weijay
LastEditTime: 2023-07-07 20:36:29
Description: 放一些測試時會用到的通用函示
'''

import datetime
import random
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.model import Base

from . import _fake_data


class FakeData:
    """用來建立隨機測試資料"""

    def fake_restaurant(is_lat_lng: bool = True, number: int = 1):
        """生成假餐廳資料，比較近的

        這裡的比較近是指使用 `fake_current_location()` 生成目標位置
        使用 `fake_restaurant()` 生成的餐廳資料，會座落在目標位置附近

        簡而言之，如果使用 `fake_restaurant()` 生成餐廳位置，如果要測試在目標範圍內的餐廳，就使用 `fake_current_location()` ( 5KM 內 )
        """

        result = []

        name_list = random.sample(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME, number)
        address_list = random.sample(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_ADDRESS, number)

        for i in range(number):
            tmp = {"name": name_list[i], "address": address_list[i]}

            result.append(tmp)

        if is_lat_lng:
            lat_lng_list = random.sample(
                _fake_data.FakeRestaurantData.FAKE_RESTAURANT_LAT_LNG, number
            )

            for i in range(number):
                lat, lng = lat_lng_list[i]

                result[i].update({"lat": lat, "lng": lng})

        if number <= 1:
            return result[0]

        return result

    def fake_restaurant_far(is_lat_lng: bool = True, number: int = 1):
        """生成假餐廳資料，比較遠的

        這裡的比較遠是指使用 `fake_cureent_location()` 生成的目標位置
        使用 `fake_restaurant_far()` 生成的餐廳資料，會座落在目標位置很遠的地方

        簡而言之，如果使用 `fake_restaurant_far()` 生成餐廳位置，如果要測試不在目標範圍內的餐廳，就用 `fake_current_location_far()`
        """

        result = []

        name_list = random.sample(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME_FAR, number)
        address_list = random.sample(
            _fake_data.FakeRestaurantData.FAKE_RESTAURANT_ADDRESS_FAR, number
        )

        for i in range(number):
            tmp = {"name": name_list[i], "address": address_list[i]}

            result.append(tmp)

        if is_lat_lng:
            lat_lng_list = random.sample(
                _fake_data.FakeRestaurantData.FAKE_RESTAURANT_LAT_LNG_FAR, number
            )

            for i in range(number):
                lat, lng = lat_lng_list[i]

                result[i].update({"lat": lat, "lng": lng})

        if number <= 1:
            return result[0]

        return result

    def fake_current_location(number: int = 1):
        """生成目標位置

        如果要測試在附近的餐廳，使用 `fake_restaurant()` ( 5KM 內 )
        """

        fake_location = [(24.94409, 121.22538), (24.94442, 121.22347), (24.94135, 121.22447)]

        if number <= 1:
            return random.choice(fake_location)

        else:
            return random.sample(fake_location, number)

    def fake_current_location_far(number: int = 1):
        """生成目標位置

        如果要測試在附近的餐廳，使用 `fake_restaurant_far()` ( 5KM 內 )
        """

        fake_location = [(22.98856, 120.23490), (22.98892, 120.23356), (22.98796, 120.23541)]

        if number <= 1:
            return random.choice(fake_location)

        else:
            return random.sample(fake_location, number)

    def fake_restaurant_open_time(to_str: bool = False, number: int = 1):
        """生成假餐廳營業時間

        ( 不會包括 restaurant_id 欄位，需要自己增加，因為考慮之後會要根據 restaurant 的資料來關聯)

        """

        result = []

        day_of_week_list = random.sample(_fake_data.FakeRestaurantOpenTimeData.DAY_OF_WEEK, number)
        open_time_list = random.sample(_fake_data.FakeRestaurantOpenTimeData.OPEN_TIME, number)
        close_time_list = random.sample(_fake_data.FakeRestaurantOpenTimeData.CLOSE_TIME, number)

        for i in range(number):
            open_time = open_time_list[i]
            close_time = close_time_list[i]

            if to_str:
                open_time = open_time.strftime("%H:%M")
                close_time = close_time.strftime("%H:%M")

            tmp = {
                "day_of_week": day_of_week_list[i],
                "open_time": open_time,
                "close_time": close_time,
            }

            result.append(tmp)

        if number <= 1:
            return result[0]

        return result

    def fake_restaurant_type(number: int = 1):
        """生成假餐廳種類資料"""

        name_list = random.sample(_fake_data.FakeRestaurantType.NAME, number)
        desc_list = random.sample(_fake_data.FakeRestaurantType.DESC, number)

        result = []

        for i in range(number):
            tmp = {"name": name_list[i], "desc": desc_list[i]}

            result.append(tmp)

        if number <= 1:
            return result[0]

        return result

    def fake_user(is_oauth: bool = False, number: int = 1):
        result = []

        username_list = random.sample(_fake_data.FakeUser.USERNAME, number)
        email_list = random.sample(_fake_data.FakeUser.USERNAME, number)

        if not is_oauth:
            password_list = random.sample(_fake_data.FakeUser.PASSWORD, number)

        for i in range(number):
            tmp = {"username": username_list[i], "email": email_list[i]}

            if not is_oauth:
                tmp.update({"password": password_list[i]})

            else:
                tmp.update({"is_oauth": True})

            result.append(tmp)

        if number <= 1:
            return result[0]

        return result

    def fake_oauth(number: int = 1):
        result = []

        provider_list = random.sample(_fake_data.FakeOAuth.PROVIDER, number)
        access_token_list = random.sample(_fake_data.FakeOAuth.ACCESS_TOKEN, number)

        for i in range(number):
            tmp = {"provider": provider_list[i], "access_token": access_token_list[i]}

            result.append(tmp)

        if number <= 1:
            return result[0]

        return result


class FakeInitData:
    """生成測試資料
    與 :class:`FakeData` 不同的是， :class:`FakeInitData` 是生成在測試初始化時要新增進資料庫的資料。

    :class:`FakeInitData` 生成的資料不會跟 :class:`FakeData` 重複。
    """

    def fake_restaurant() -> dict:
        """生成餐廳測試資料

        測試資料的欄位有:
        - `name` (str)
        - `address` (str)
        - `lat` (float)
        - `lng` (float)
        """

        fake_data = {
            "name": "test_restaurant_name",
            "address": "test_restaurant_address",
            "lat": 23.001,
            "lng": 120.001,
        }

        return fake_data

    def fake_restaurant_open_time() -> dict:
        """生成餐廳營業時間測試資料

        測試資料的欄位有:
        - `day_of_week` (int)
        - `open_time` (datetime.time)
        - `close_time` (datetime.time)
        """

        fake_data = {
            "day_of_week": 100,
            "open_time": datetime.time(hour=8, minute=0),
            "close_time": datetime.time(hour=22, minute=0),
        }

        return fake_data

    def fake_restaurant_type() -> dict:
        """生成餐廳種類測試資料

        測試資料的欄位有:
        - `name` (str)
        - `desc` (str)
        """

        fake_data = {"name": "restaurant_test_type", "desc": "This_is_a_restaurant_test_type"}

        return fake_data

    def fake_user() -> dict:
        """生成使用者測試資料

        測試資料的欄位有:
        - `username` (str)
        - `email` (str)
        - `password` (str)
        """

        fake_data = {
            "username": "test_user",
            "email": "test_user@test.com",
            "password": "this_is_test_user_password",
        }

        return fake_data

    def fake_user_oauth() -> dict:
        """生成使用者 OAuth 測試資料

        測試資料的欄位有:
        - `provider` (str)
        - `access_token` (str)
        """

        fake_data = {"provider": "test_oauth_provider", "access_token": "test_oauth_access_token"}

        return fake_data


class FakeDataBase:
    """產生測試資料庫"""

    SQLALCHEMY_DATABASE_URL = "sqlite://"

    def __init__(self):
        # 使用 `StaticPool` 來確保只會有一個連接對資料庫進行操作
        # 確保每次使用 `SessionLocal` 時都是建立一個新連接，不會被其他測試影響
        self.engine = create_engine(
            self.SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
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
