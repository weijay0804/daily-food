'''
Author: weijay
Date: 2023-04-25 17:19:24
LastEditors: andy
LastEditTime: 2023-06-21 01:08:58
Description: 放一些測試時會用到的通用函示
'''

import random
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.model import Base

from . import _fake_data


# TODO 重構這邊，不要寫那麼複雜，不管 number 是不是 1 一律用 `random.sample`
class FakeData:
    """用來建立隨機測試資料"""

    def fake_restaurant(is_lat_lng: bool = True, number: int = 1):
        """生成假餐廳資料，比較近的

        這裡的比較近是指使用 `fake_current_location()` 生成目標位置
        使用 `fake_restaurant()` 生成的餐廳資料，會座落在目標位置附近

        簡而言之，如果使用 `fake_restaurant()` 生成餐廳位置，如果要測試在目標範圍內的餐廳，就使用 `fake_current_location()` ( 5KM 內 )
        """

        if number <= 1:
            result = {}

            name = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME)
            address = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_ADDRESS)

            if is_lat_lng:
                lat, lng = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_LAT_LNG)
                result.update({"lat": lat, "lng": lng})

            result.update({"name": name, "address": address})

        else:
            result = []

            name_list = random.sample(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME, number)
            address_list = random.sample(
                _fake_data.FakeRestaurantData.FAKE_RESTAURANT_ADDRESS, number
            )

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

        return result

    def fake_restaurant_far(is_lat_lng: bool = True, number: int = 1):
        """生成假餐廳資料，比較遠的

        這裡的比較遠是指使用 `fake_cureent_location()` 生成的目標位置
        使用 `fake_restaurant_far()` 生成的餐廳資料，會座落在目標位置很遠的地方

        簡而言之，如果使用 `fake_restaurant_far()` 生成餐廳位置，如果要測試不在目標範圍內的餐廳，就用 `fake_current_location_far()`
        """

        if number <= 1:
            result = {}

            name = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME_FAR)
            address = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_ADDRESS_FAR)

            if is_lat_lng:
                lat, lng = random.choice(_fake_data.FakeRestaurantData.FAKE_RESTAURANT_LAT_LNG_FAR)
                result.update({"lat": lat, "lng": lng})

            result.update({"name": name, "address": address})

        else:
            result = []

            name_list = random.sample(
                _fake_data.FakeRestaurantData.FAKE_RESTAURANT_NAME_FAR, number
            )
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

        if number <= 1:
            day_of_week = random.choice(_fake_data.FakeRestaurantOpenTimeData.DAY_OF_WEEK)
            open_time = random.choice(_fake_data.FakeRestaurantOpenTimeData.OPEN_TIME)
            close_time = random.choice(_fake_data.FakeRestaurantOpenTimeData.CLOSE_TIME)

            if to_str:
                open_time = open_time.strftime("%H:%M")
                close_time = close_time.strftime("%H:%M")

            result = {"day_of_week": day_of_week, "open_time": open_time, "close_time": close_time}

        else:
            result = []

            day_of_week_list = random.sample(
                _fake_data.FakeRestaurantOpenTimeData.DAY_OF_WEEK, number
            )
            open_time_list = random.sample(_fake_data.FakeRestaurantOpenTimeData.OPEN_TIME, number)
            close_time_list = random.sample(
                _fake_data.FakeRestaurantOpenTimeData.CLOSE_TIME, number
            )

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

        return result

    def fake_restaurant_type(number: int = 1):
        """生成假餐廳種類資料"""

        if number <= 1:
            name = random.choice(_fake_data.FakeRestaurantType.NAME)
            desc = random.choice(_fake_data.FakeRestaurantType.DESC)

            result = {"name": name, "desc": desc}

        else:
            name_list = random.sample(_fake_data.FakeRestaurantType.NAME, number)
            desc_list = random.sample(_fake_data.FakeRestaurantType.DESC, number)

            result = []

            for i in range(number):
                tmp = {"name": name_list[i], "desc": desc_list[i]}

                result.append(tmp)

        return result

    # TODO 把 password_hash 更改成 password
    def fake_user(is_oauth: bool = False, number: int = 1):
        if number <= 1:
            username = random.choice(_fake_data.FakeUser.USERNAME)
            email = random.choice(_fake_data.FakeUser.EMAIL)

            result = {"username": username, "email": email}

            if not is_oauth:
                password_hash = random.choice(_fake_data.FakeUser.PASSWORD_HASH)

                result.update({"password_hash": password_hash})

            else:
                result.update({"is_oauth": True})

        else:
            result = []

            username_list = random.sample(_fake_data.FakeUser.USERNAME, number)
            email_list = random.sample(_fake_data.FakeUser.USERNAME, number)

            if not is_oauth:
                password_hash_list = random.sample(_fake_data.FakeUser.PASSWORD_HASH, number)

            for i in range(number):
                tmp = {"username": username_list[i], "email": email_list[i]}

                if not is_oauth:
                    tmp.update({"password_hash": password_hash_list[i]})

                else:
                    tmp.update({"is_oauth": True})

                result.append(tmp)

        return result

    def fake_oauth(number: int = 1):
        if number <= 1:
            provider = random.choice(_fake_data.FakeOAuth.PROVIDER)
            access_token = random.choice(_fake_data.FakeOAuth.ACCESS_TOKEN)

            result = {"provider": provider, "access_token": access_token}

        else:
            result = []

            provider_list = random.sample(_fake_data.FakeOAuth.PROVIDER, number)
            access_token_list = random.sample(_fake_data.FakeOAuth.ACCESS_TOKEN, number)

            for i in range(number):
                tmp = {"provider": provider_list[i], "access_token": access_token_list[i]}

                result.append(tmp)

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
