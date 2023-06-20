'''
Author: weijay
Date: 2023-04-24 23:09:47
LastEditors: andy
LastEditTime: 2023-06-21 01:04:41
Description: DataBase ORM 模型單元測試
'''

import os
import unittest
from datetime import datetime, time

from sqlalchemy import text

from app.database.model import Restaurant, RestaurantOpenTime, RestaurantType, User, OAuth
from tests.utils import FakeData, FakeDataBase


# TODO 這邊應該獨立出來
class InitialDataBaseTest(unittest.TestCase):
    """建立測試資料庫環境"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.fake_database = FakeDataBase()
        cls.fake_database.Base.metadata.create_all(bind=cls.fake_database.engine)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fake_database.engine.clear_compiled_cache()
        cls.fake_database.engine.dispose()
        cls.fake_database.Base.metadata.drop_all(bind=cls.fake_database.engine)
        os.remove("test.db")


class TestRestaurantModel(InitialDataBaseTest):
    """Restaraunt Table ORM 模型單元測試"""

    def _get_restaurant_obj(self, db) -> "Restaurant":
        """取得資料庫中的 restaurant 物件"""

        r_obj = (
            db.query(Restaurant)
            .filter(Restaurant.name == self._fake_restaurant_data["name"])
            .first()
        )

        return r_obj

    def setUp(self) -> None:
        """在每個測試前先新增資料至資料庫"""

        # TODO 這邊不要這樣，應該統一生成
        # NOTE 如果之後 Restaurant 有做更改的話，要檢查一下這邊

        self._fake_restaurant_data = {
            "name": "test_restaurant",
            "address": "test_address",
            "lat": 23.001,
            "lng": 120.001,
        }

        fake_restaurant = Restaurant(**self._fake_restaurant_data)

        with self.fake_database.get_db() as db:
            db.add(fake_restaurant)
            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant"))
            db.commit()

    def test_create_restaurant(self):
        """新增餐廳測試"""

        fake_data = FakeData.fake_restaurant()

        restaurant = Restaurant(**fake_data)

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

            self.assertEqual(restaurant.name, fake_data["name"])
            self.assertEqual(restaurant.address, fake_data["address"])
            self.assertEqual(restaurant.lat, fake_data["lat"])
            self.assertEqual(restaurant.lng, fake_data["lng"])
            self.assertIsNone(restaurant.phone)
            self.assertIsNone(restaurant.desc)
            self.assertIsNone(restaurant.price)
            self.assertEqual(restaurant.is_enable, True)
            self.assertIsInstance(restaurant.create_at, datetime)
            self.assertIsNotNone(restaurant.create_at)
            self.assertIsNone(restaurant.update_at)

    def test_read_restaurant(self):
        """取得餐廳測試"""

        with self.fake_database.get_db() as db:
            restaurant = self._get_restaurant_obj(db)

        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.name, self._fake_restaurant_data["name"])
        self.assertEqual(restaurant.address, self._fake_restaurant_data["address"])
        self.assertEqual(restaurant.lat, self._fake_restaurant_data["lat"])
        self.assertEqual(restaurant.lng, self._fake_restaurant_data["lng"])

    def test_update_restaurant(self):
        """更新餐廳測試"""

        with self.fake_database.get_db() as db:
            restaurant = self._get_restaurant_obj(db)

            self.assertEqual(restaurant.name, self._fake_restaurant_data["name"])
            self.assertEqual(restaurant.address, self._fake_restaurant_data["address"])
            self.assertEqual(restaurant.update_at, None)

            restaurant.name = "update_test_restaurant"
            db.commit()

            updated_restaurant = db.get(Restaurant, restaurant.id)

            self.assertIsNotNone(updated_restaurant)
            self.assertEqual(restaurant.name, "update_test_restaurant")
            self.assertIsNotNone(restaurant.update_at)
            self.assertIsInstance(restaurant.update_at, datetime)

    def test_delete_restaurant(self):
        """刪除餐測試"""

        with self.fake_database.get_db() as db:
            restaurant = self._get_restaurant_obj(db)

            self.assertIsNotNone(restaurant)

            db.delete(restaurant)
            db.commit()

            deleted_restaurant = db.get(Restaurant, restaurant.id)

            self.assertIsNone(deleted_restaurant)


class TestRestaurantOpenTimeModel(InitialDataBaseTest):
    """RestaurantOpenTime ORM 模型單元測試"""

    def _get_restaurant_obj(self, db) -> "Restaurant":
        """取得資料庫中的 restaurant 物件"""

        r_obj = (
            db.query(Restaurant)
            .filter(Restaurant.name == self.fake_restaurant_data["name"])
            .first()
        )

        return r_obj

    def _get_open_time_obj(self, db) -> "RestaurantOpenTime":
        """取得資料庫中的 open time 物件"""

        ot_obj = (
            db.query(RestaurantOpenTime)
            .filter(RestaurantOpenTime.day_of_week == self._fake_open_time_data["day_of_week"])
            .first()
        )

        return ot_obj

    @classmethod
    def setUpClass(cls) -> None:
        """在這個 class 執行前先塞資料到資料庫"""

        super().setUpClass()

        cls.fake_restaurant_data = FakeData.fake_restaurant()
        fake_restaurant = Restaurant(**cls.fake_restaurant_data)

        with cls.fake_database.get_db() as db:
            db.add(fake_restaurant)
            db.commit()

    def setUp(self) -> None:
        """在每個測試執行前，先新增資料到資料庫"""

        # TODO 這邊不要這樣，應該統一生成
        # NOTE 如果 restaurant_open_time table 有更改的話，要檢查一下這邊

        self._fake_open_time_data = {
            "day_of_week": 2,
            "open_time": time(hour=12, minute=0),
            "close_time": time(hour=20, minute=0),
        }

        with self.fake_database.get_db() as db:
            r_obj = self._get_restaurant_obj(db)

            fake_restaurant_open_time = RestaurantOpenTime(**self._fake_open_time_data)
            r_obj.open_times.append(fake_restaurant_open_time)

            db.add(fake_restaurant_open_time)
            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant_open_time"))
            db.commit()

    def test_create_restaurant_open_time(self):
        """新增餐廳營業時間測試"""

        fake_restaurant_open_time = FakeData.fake_restaurant_open_time()

        while self._fake_open_time_data["day_of_week"] == fake_restaurant_open_time["day_of_week"]:
            fake_restaurant_open_time = FakeData.fake_restaurant_open_time()

        with self.fake_database.get_db() as db:
            r_obj = self._get_restaurant_obj(db)
            ot_obj = RestaurantOpenTime(**fake_restaurant_open_time)

            r_obj.open_times.append(ot_obj)

            db.add(ot_obj)
            db.commit()

            data = (
                db.query(RestaurantOpenTime)
                .filter(RestaurantOpenTime.day_of_week == fake_restaurant_open_time["day_of_week"])
                .first()
            )

            self.assertEqual(data.day_of_week, fake_restaurant_open_time["day_of_week"])
            self.assertIsInstance(data.open_time, time)
            self.assertEqual(data.open_time, fake_restaurant_open_time["open_time"])
            self.assertIsInstance(data.close_time, time)
            self.assertEqual(data.close_time, fake_restaurant_open_time["close_time"])
            self.assertIsInstance(data.create_at, datetime)
            self.assertIsNotNone(data.create_at)
            self.assertIsNone(data.update_at)

    def test_read_restaurant_open_time(self):
        """取得餐廳營業時間測試"""

        with self.fake_database.get_db() as db:
            data = self._get_open_time_obj(db)

        self.assertIsNotNone(data)
        self.assertEqual(data.open_time, self._fake_open_time_data["open_time"])
        self.assertEqual(data.close_time, self._fake_open_time_data["close_time"])

    def test_update_restaurant_open_time(self):
        """更新餐廳營業時間測試"""

        with self.fake_database.get_db() as db:
            open_time = self._get_open_time_obj(db)

            self.assertIsNone(open_time.update_at)

            open_time.day_of_week = 5

            db.commit()

            updated_data = db.get(RestaurantOpenTime, open_time.id)

            self.assertIsNotNone(updated_data)
            self.assertEqual(updated_data.day_of_week, 5)
            self.assertIsNotNone(updated_data.update_at)
            self.assertIsInstance(updated_data.update_at, datetime)

    def test_delete_restaurant_open_time(self):
        """刪除餐廳營業時間測試"""

        with self.fake_database.get_db() as db:
            open_time = self._get_open_time_obj(db)

            self.assertIsNotNone(open_time)

            db.delete(open_time)
            db.commit()

            deleted_data = db.get(RestaurantOpenTime, open_time.id)

            self.assertIsNone(deleted_data)


class TestRestaurantTypeModel(InitialDataBaseTest):
    """RestaurantType Model 單元測試"""

    def setUp(self) -> None:
        """在每個測試前，先新增資料"""

        # TODO 這邊不要這樣，應該統一生成
        # NOTE 如果 RestaurantType 有變動，要檢查一下這邊

        self._fake_type_data = {"name": "test_type", "desc": "This is test type"}

        fake_restaurant_type = RestaurantType(**self._fake_type_data)

        with self.fake_database.get_db() as db:
            db.add(fake_restaurant_type)
            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant_type"))
            db.commit()

    def test_create_restaurant_type(self):
        """新增餐廳種類測試"""

        fake_restaurant_type = FakeData.fake_restaurant_type()

        with self.fake_database.get_db() as db:
            db.add(RestaurantType(**fake_restaurant_type))
            db.commit()

            r_type = (
                db.query(RestaurantType)
                .filter(RestaurantType.name == fake_restaurant_type["name"])
                .first()
            )

        self.assertIsNotNone(r_type)
        self.assertIsNotNone(r_type.id)
        self.assertEqual(r_type.name, fake_restaurant_type["name"])
        self.assertEqual(r_type.desc, fake_restaurant_type["desc"])
        self.assertIsNotNone(r_type.create_at)
        self.assertIsInstance(r_type.create_at, datetime)
        self.assertIsNone(r_type.update_at)

    def test_read_restaurant_type(self):
        """取得餐廳種類測試"""

        with self.fake_database.get_db() as db:
            r_type = (
                db.query(RestaurantType)
                .filter(RestaurantType.name == self._fake_type_data["name"])
                .first()
            )

        self.assertIsNotNone(r_type)
        self.assertEqual(r_type.name, self._fake_type_data["name"])
        self.assertEqual(r_type.desc, self._fake_type_data["desc"])

    def test_update_restaurant_type(self):
        """更新餐廳種類測試"""

        with self.fake_database.get_db() as db:
            r_type = (
                db.query(RestaurantType)
                .filter(RestaurantType.name == self._fake_type_data["name"])
                .first()
            )

            self.assertIsNotNone(r_type)
            self.assertEqual(r_type.name, self._fake_type_data["name"])
            self.assertIsNone(r_type.update_at)

            r_type.name = "update_test_type"
            db.commit()

            updated_r_type = db.get(RestaurantType, r_type.id)

            self.assertEqual(updated_r_type.name, "update_test_type")
            self.assertIsNotNone(updated_r_type.update_at)
            self.assertIsInstance(updated_r_type.update_at, datetime)

    def test_delete_restaurant_type(self):
        """刪除餐廳種類測試"""

        with self.fake_database.get_db() as db:
            r_type = (
                db.query(RestaurantType)
                .filter(RestaurantType.name == self._fake_type_data["name"])
                .first()
            )

            self.assertIsNotNone(r_type)

            db.delete(r_type)
            db.commit()

            deleted_r_type = (
                db.query(RestaurantType)
                .filter(RestaurantType.name == self._fake_type_data["name"])
                .first()
            )

            self.assertIsNone(deleted_r_type)


class TestUserModel(InitialDataBaseTest):
    """User Model 單元測試"""

    def setUp(self) -> None:
        """在每個測試前，先新增資料到資料庫"""

        # TODO 這邊不要這樣，應該統一生成
        # NOTE 如果 User model 有變更的話，要檢查一下這邊
        self._fake_uesr_data = {
            "username": "test_user",
            "email": "test_user@test.com",
            "password_hash": "This is hashed password",
        }

        with self.fake_database.get_db() as db:
            db.add(User(**self._fake_uesr_data))
            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM user"))
            db.commit()

    def test_create_user(self):
        """新增使用者測試"""

        fake_user = FakeData.fake_user()

        with self.fake_database.get_db() as db:
            db.add(User(**fake_user))
            db.commit()

            data = db.query(User).filter(User.username == fake_user["username"]).first()

            self.assertEqual(data.username, fake_user["username"])
            self.assertEqual(data.email, fake_user["email"])
            self.assertEqual(data.password_hash, fake_user["password_hash"])
            self.assertEqual(data.is_oauth, False)
            self.assertEqual(data.is_enable, True)
            self.assertIsNotNone(data.create_at)
            self.assertIsInstance(data.create_at, datetime)
            self.assertIsNone(data.update_at)

    def test_read_user(self):
        """取得使用者測試"""

        with self.fake_database.get_db() as db:
            user = db.query(User).filter(User.username == self._fake_uesr_data["username"]).first()

            self.assertIsNotNone(user)
            self.assertEqual(user.username, self._fake_uesr_data["username"])
            self.assertEqual(user.email, self._fake_uesr_data["email"])
            self.assertEqual(user.password_hash, self._fake_uesr_data["password_hash"])

    def test_update_user(self):
        """更新使用者測試"""

        with self.fake_database.get_db() as db:
            user = db.query(User).filter(User.username == self._fake_uesr_data["username"]).first()

            self.assertIsNotNone(user)

            user.username = "update_user"

            db.commit()

            updated_user = db.get(User, user.id)

            self.assertIsNotNone(updated_user)
            self.assertEqual(updated_user.username, "update_user")
            self.assertIsNotNone(updated_user.update_at)
            self.assertIsInstance(updated_user.update_at, datetime)

    def test_delete_uesr(self):
        """刪除使用者測試"""

        with self.fake_database.get_db() as db:
            user = db.query(User).filter(User.username == self._fake_uesr_data["username"]).first()

            self.assertIsNotNone(user)

            db.delete(user)
            db.commit()

            deleted_user = (
                db.query(User).filter(User.username == self._fake_uesr_data["username"]).first()
            )

            self.assertIsNone(deleted_user)


class TestOAuthModel(InitialDataBaseTest):
    """OAuth model 單元測試"""

    @classmethod
    def setUpClass(cls) -> None:
        """在這個 class 執行前，先新增 user 資料"""
        super().setUpClass()

        fake_user_data = FakeData.fake_user(is_oauth=True)

        with cls.fake_database.get_db() as db:
            db.add(User(**fake_user_data))
            db.commit()

            cls.fake_user = (
                db.query(User).filter(User.username == fake_user_data["username"]).first()
            )

    def setUp(self) -> None:
        """在每個測試前，先新增資料的資料庫"""

        # TODO 這邊不要這樣，應該統一生成
        # NOTE 如果 OAuth model 有變更的話，要檢查一下這邊
        self._fake_oauth_data = {"provider": "test_provider", "access_token": "test_token"}

        with self.fake_database.get_db() as db:
            db.add(OAuth(**self._fake_oauth_data, user=self.fake_user))
            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM oauth"))
            db.commit()

    def test_create_oauth(self):
        """新增 oauth 測試"""

        fake_oauth = FakeData.fake_oauth()

        with self.fake_database.get_db() as db:
            db.add(OAuth(**fake_oauth, user=self.fake_user))
            db.commit()

            oauth = db.query(OAuth).filter(OAuth.access_token == fake_oauth["access_token"]).first()

            self.assertEqual(oauth.provider, fake_oauth["provider"])
            self.assertEqual(oauth.access_token, fake_oauth["access_token"])
            self.assertIsNotNone(oauth.create_at)
            self.assertIsInstance(oauth.create_at, datetime)
            self.assertIsNone(oauth.update_at)

    def test_read_oauth(self):
        """取得 oauth 測試"""

        with self.fake_database.get_db() as db:
            oauth = (
                db.query(OAuth)
                .filter(OAuth.access_token == self._fake_oauth_data["access_token"])
                .first()
            )

            self.assertIsNotNone(oauth)
            self.assertEqual(oauth.provider, self._fake_oauth_data["provider"])
            self.assertEqual(oauth.access_token, self._fake_oauth_data["access_token"])

    def test_update_oauth(self):
        """更新 oauth 測試"""

        with self.fake_database.get_db() as db:
            oauth = (
                db.query(OAuth)
                .filter(OAuth.access_token == self._fake_oauth_data["access_token"])
                .first()
            )

            self.assertIsNotNone(oauth)

            oauth.access_token = "update_access_token"

            db.commit()

            updated_oauth = db.get(OAuth, oauth.id)

            self.assertIsNotNone(updated_oauth)
            self.assertEqual(updated_oauth.access_token, "update_access_token")
            self.assertIsNotNone(updated_oauth.update_at)
            self.assertIsInstance(updated_oauth.update_at, datetime)

    def test_delete_oauth(self):
        """刪除 oauth 測試"""

        with self.fake_database.get_db() as db:
            oauth = (
                db.query(OAuth)
                .filter(OAuth.access_token == self._fake_oauth_data["access_token"])
                .first()
            )

            self.assertIsNotNone(oauth)

            db.delete(oauth)
            db.commit()

            deleted_oauth = (
                db.query(OAuth)
                .filter(OAuth.access_token == self._fake_oauth_data["access_token"])
                .first()
            )

            self.assertIsNone(deleted_oauth)
