'''
Author: weijay
Date: 2023-06-04 15:24:07
LastEditors: andy
LastEditTime: 2023-06-11 23:11:51
Description: DataBase ORM 模型關聯性單元測試
'''

import os
import unittest
from typing import Tuple

from sqlalchemy import text

from app.database.model import Restaurant, RestaurantOpenTime, RestaurantType, User, OAuth
from tests.utils import FakeDataBase, FakeData


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


class TestRestaurantAndOpneTimeRealtion(InitialDataBaseTest):
    """Restaurant model 與 RestaurantOpenTime model 一對多關聯性測試"""

    def _get_restaurant_obj(self, db) -> "Restaurant":
        """取得資料庫中的 restaurant 資料"""

        restaurant_obj = (
            db.query(Restaurant)
            .filter(Restaurant.name == self.fake_reataurant_data["name"])
            .first()
        )

        return restaurant_obj

    def _get_open_time_objs(self, db) -> Tuple["RestaurantOpenTime"]:
        """取得資料庫中的 open_time 資料"""

        open_time_obj1 = (
            db.query(RestaurantOpenTime)
            .filter(RestaurantOpenTime.day_of_week == self.fake_open_time_data1["day_of_week"])
            .first()
        )

        open_time_obj2 = (
            db.query(RestaurantOpenTime)
            .filter(RestaurantOpenTime.day_of_week == self.fake_open_time_data2["day_of_week"])
            .first()
        )

        return open_time_obj1, open_time_obj2

    def setUp(self) -> None:
        """在每個測試前，先新增資料"""

        self.fake_reataurant_data = FakeData.fake_restaurant()

        open_time_datas = FakeData.fake_restaurant_open_time(number=2)
        self.fake_open_time_data1 = open_time_datas[0]
        self.fake_open_time_data2 = open_time_datas[1]

        with self.fake_database.get_db() as db:
            db_restaurant = Restaurant(**self.fake_reataurant_data)
            db_open_time1 = RestaurantOpenTime(**self.fake_open_time_data1)
            db_open_time2 = RestaurantOpenTime(**self.fake_open_time_data2)

            db_restaurant.open_times.append(db_open_time1)
            db_restaurant.open_times.append(db_open_time2)
            db.add_all([db_restaurant, db_open_time1, db_open_time2])
            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant_open_time"))
            db.execute(text("DELETE FROM restaurant"))

            db.commit()

    def test_read(self):
        """餐廳與餐廳營業時間關聯測試"""

        with self.fake_database.get_db() as db:
            restaurant_obj = self._get_restaurant_obj(db)
            open_time_obj1, open_time_obj2 = self._get_open_time_objs(db)

            open_times = restaurant_obj.open_times

            self.assertEqual(len(open_times), 2)
            self.assertIn(open_time_obj1, open_times)
            self.assertIn(open_time_obj2, open_times)

    def test_on_remove(self):
        """移除餐廳與營業時間關聯測試"""

        with self.fake_database.get_db() as db:
            restaurant_obj = self._get_restaurant_obj(db)
            open_time_obj1, open_time_obj2 = self._get_open_time_objs(db)

            restaurant_obj.open_times.remove(open_time_obj1)
            db.commit()

            new_resaurant_obj = db.get(Restaurant, restaurant_obj.id)
            new_open_time_obj1 = db.get(RestaurantType, open_time_obj1.id)

            open_times = new_resaurant_obj.open_times

            self.assertEqual(len(open_times), 1)
            self.assertIsNone(new_open_time_obj1)
            self.assertIn(open_time_obj2, open_times)
            self.assertNotIn(open_time_obj1, open_times)

    def test_on_delete_restaurant(self):
        """刪除餐廳物件後測試"""

        with self.fake_database.get_db() as db:
            restaurant_obj = self._get_restaurant_obj(db)
            open_time_obj1, open_time_obj2 = self._get_open_time_objs(db)

            self.assertIsNotNone(restaurant_obj)
            self.assertIsNotNone(open_time_obj1)
            self.assertIsNotNone(open_time_obj2)

            db.delete(restaurant_obj)
            db.commit()

            new_restaurant_obj = db.get(Restaurant, restaurant_obj.id)
            new_open_time_obj1 = db.get(RestaurantOpenTime, open_time_obj1.id)
            new_open_time_obj2 = db.get(RestaurantOpenTime, open_time_obj2.id)

            self.assertIsNone(new_restaurant_obj)
            self.assertIsNone(new_open_time_obj1)
            self.assertIsNone(new_open_time_obj2)

    def test_on_delete_open_time(self):
        """移除餐廳營業時間物件後測試"""

        with self.fake_database.get_db() as db:
            restaurant_obj = self._get_restaurant_obj(db)
            open_time_obj1, open_time_obj2 = self._get_open_time_objs(db)

            self.assertIsNotNone(restaurant_obj)
            self.assertIsNotNone(open_time_obj1)
            self.assertIsNotNone(open_time_obj2)

            db.delete(open_time_obj1)
            db.commit()

            new_restaurant_obj = db.get(Restaurant, restaurant_obj.id)
            new_open_time_obj1 = db.get(RestaurantOpenTime, open_time_obj1.id)
            new_open_time_obj2 = db.get(RestaurantOpenTime, open_time_obj2.id)

            self.assertIsNotNone(new_restaurant_obj)
            self.assertIsNotNone(new_open_time_obj2)
            self.assertIsNone(new_open_time_obj1)

            self.assertIn(new_open_time_obj2, new_restaurant_obj.open_times)


class TestRestaurantAndRestaurantTypeRelation(InitialDataBaseTest):
    """Restaurant model 與 RestaurantType model 多對多關聯性測試"""

    def _get_restaurant_objs(self, db) -> Tuple["Restaurant"]:
        """取得資料庫中的餐廳物件"""

        r_obj1 = (
            db.query(Restaurant)
            .filter(Restaurant.name == self.fake_restaurant_data1["name"])
            .first()
        )
        r_obj2 = (
            db.query(Restaurant)
            .filter(Restaurant.name == self.fake_restaurant_data2["name"])
            .first()
        )

        return r_obj1, r_obj2

    def _get_restaurant_type_objs(self, db) -> Tuple["RestaurantType"]:
        """取得資料庫中的餐廳種類物件"""

        r_type_obj1 = (
            db.query(RestaurantType)
            .filter(RestaurantType.name == self.fake_r_type_data1["name"])
            .first()
        )
        r_type_obj2 = (
            db.query(RestaurantType)
            .filter(RestaurantType.name == self.fake_r_type_data2["name"])
            .first()
        )

        return r_type_obj1, r_type_obj2

    def setUp(self) -> None:
        """在每個測試前，先新增資料"""

        restaurant_datas = FakeData.fake_restaurant(number=2)
        self.fake_restaurant_data1 = restaurant_datas[0]
        self.fake_restaurant_data2 = restaurant_datas[1]

        type_datas = FakeData.fake_restaurant_type(number=2)
        self.fake_r_type_data1 = type_datas[0]
        self.fake_r_type_data2 = type_datas[1]

        with self.fake_database.get_db() as db:
            db_r_obj1 = Restaurant(**self.fake_restaurant_data1)
            db_r_obj2 = Restaurant(**self.fake_restaurant_data2)
            db_r_type_obj1 = RestaurantType(**self.fake_r_type_data1)
            db_r_type_obj2 = RestaurantType(**self.fake_r_type_data2)

            db_r_obj1.types.append(db_r_type_obj1)
            db_r_obj1.types.append(db_r_type_obj2)

            db_r_obj2.types.append(db_r_type_obj1)
            db_r_obj2.types.append(db_r_type_obj2)

            db.add_all([db_r_obj1, db_r_obj2, db_r_type_obj1, db_r_type_obj2])

            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant_type_intermediay"))
            db.execute(text("DELETE FROM restaurant"))
            db.execute(text("DELETE FROM restaurant_type"))
            db.commit()

    def test_read(self):
        """餐廳和餐廳種類關聯測試"""

        with self.fake_database.get_db() as db:
            restaurant_obj1, restaurant_obj2 = self._get_restaurant_objs(db)
            r_type_obj1, r_type_obj2 = self._get_restaurant_type_objs(db)

            r_obj1_types = restaurant_obj1.types
            r_obj2_types = restaurant_obj2.types

            self.assertIn(r_type_obj1, r_obj1_types)
            self.assertIn(r_type_obj2, r_obj1_types)
            self.assertIn(r_type_obj1, r_obj2_types)
            self.assertIn(r_type_obj2, r_obj2_types)

            self.assertIn(restaurant_obj1, r_type_obj1.restaurants)
            self.assertIn(restaurant_obj2, r_type_obj1.restaurants)
            self.assertIn(restaurant_obj1, r_type_obj2.restaurants)
            self.assertIn(restaurant_obj2, r_type_obj2.restaurants)

    def test_on_remove_restaurant(self):
        """移除餐廳與餐廳種類關聯測試"""

        with self.fake_database.get_db() as db:
            restaurant_obj1, restaurant_obj2 = self._get_restaurant_objs(db)
            r_type_obj1, r_type_obj2 = self._get_restaurant_type_objs(db)

            restaurant_obj1.types.remove(r_type_obj1)
            restaurant_obj2.types.remove(r_type_obj2)

            db.commit()

            new_restaurant_obj1 = db.get(Restaurant, restaurant_obj1.id)
            new_restaurant_obj2 = db.get(Restaurant, restaurant_obj2.id)
            new_r_type_obj1 = db.get(RestaurantType, r_type_obj1.id)
            new_r_type_obj2 = db.get(RestaurantType, r_type_obj2.id)

            self.assertIn(new_r_type_obj2, new_restaurant_obj1.types)
            self.assertNotIn(new_r_type_obj1, new_restaurant_obj1.types)
            self.assertIn(new_r_type_obj1, new_restaurant_obj2.types)
            self.assertNotIn(new_r_type_obj2, new_restaurant_obj2.types)

            self.assertIn(new_restaurant_obj1, new_r_type_obj2.restaurants)
            self.assertIn(new_restaurant_obj2, new_r_type_obj1.restaurants)
            self.assertNotIn(new_restaurant_obj1, new_r_type_obj1.restaurants)
            self.assertNotIn(new_restaurant_obj2, new_r_type_obj2.restaurants)

    def test_on_delete_restaurant(self):
        """刪除餐廳物件後測試"""

        with self.fake_database.get_db() as db:
            restaurant_obj1, restaurant_obj2 = self._get_restaurant_objs(db)
            r_type_obj1, r_type_obj2 = self._get_restaurant_type_objs(db)

            self.assertIsNotNone(restaurant_obj1)
            self.assertIsNotNone(restaurant_obj2)
            self.assertIsNotNone(r_type_obj1)
            self.assertIsNotNone(r_type_obj2)

            db.delete(restaurant_obj1)
            db.commit()

            new_restaurant_obj1 = db.get(Restaurant, restaurant_obj1.id)
            new_restaurant_obj2 = db.get(Restaurant, restaurant_obj2.id)
            new_r_type_obj1 = db.get(RestaurantType, r_type_obj1.id)
            new_r_type_obj2 = db.get(RestaurantType, r_type_obj2.id)

            self.assertIsNone(new_restaurant_obj1)
            self.assertIsNotNone(new_restaurant_obj2)
            self.assertIsNotNone(new_r_type_obj1)
            self.assertIsNotNone(new_r_type_obj2)

            self.assertIn(new_restaurant_obj2, new_r_type_obj1.restaurants)
            self.assertNotIn(new_restaurant_obj1, new_r_type_obj1.restaurants)

    def test_on_delete_type(self):
        """刪除餐廳種類物件後測試"""

        with self.fake_database.get_db() as db:
            restaurant_obj1, restaurant_obj2 = self._get_restaurant_objs(db)
            r_type_obj1, r_type_obj2 = self._get_restaurant_type_objs(db)

            self.assertIsNotNone(restaurant_obj1)
            self.assertIsNotNone(restaurant_obj2)
            self.assertIsNotNone(r_type_obj1)
            self.assertIsNotNone(r_type_obj2)

            db.delete(r_type_obj1)
            db.commit()

            new_restaurant_obj1 = db.get(Restaurant, restaurant_obj1.id)
            new_restaurant_obj2 = db.get(Restaurant, restaurant_obj2.id)
            new_r_type_obj1 = db.get(RestaurantType, r_type_obj1.id)
            new_r_type_obj2 = db.get(RestaurantType, r_type_obj2.id)

            self.assertIsNone(new_r_type_obj1)
            self.assertIsNotNone(new_restaurant_obj2)
            self.assertIsNotNone(new_restaurant_obj1)
            self.assertIsNotNone(new_r_type_obj2)

            self.assertIn(new_r_type_obj2, new_restaurant_obj1.types)
            self.assertNotIn(new_r_type_obj1, new_restaurant_obj1.types)


class TestUserAndRestaurantRelation(InitialDataBaseTest):
    """User model 與 Restaurant model 多對多關聯性測試"""

    def _get_restaurant_objs(self, db) -> Tuple["Restaurant"]:
        """取得資料庫中的餐廳物件"""

        r_obj1 = (
            db.query(Restaurant)
            .filter(Restaurant.name == self.fake_restaurant_data1["name"])
            .first()
        )

        r_obj2 = (
            db.query(Restaurant)
            .filter(Restaurant.name == self.fake_restaurant_data2["name"])
            .first()
        )

        return r_obj1, r_obj2

    def _get_user_objs(self, db) -> Tuple["User"]:
        """取得資料庫中的使用者物件"""

        u_obj1 = db.query(User).filter(User.username == self.fake_user_data1["username"]).first()

        u_obj2 = db.query(User).filter(User.username == self.fake_user_data2["username"]).first()

        return u_obj1, u_obj2

    def setUp(self) -> None:
        """在每個測試前，先新增資料"""

        restaurant_datas = FakeData.fake_restaurant(number=2)
        self.fake_restaurant_data1 = restaurant_datas[0]
        self.fake_restaurant_data2 = restaurant_datas[1]

        user_datas = FakeData.fake_user(number=2)
        self.fake_user_data1 = user_datas[0]
        self.fake_user_data2 = user_datas[1]

        with self.fake_database.get_db() as db:
            db_r_obj1 = Restaurant(**self.fake_restaurant_data1)
            db_r_obj2 = Restaurant(**self.fake_restaurant_data2)

            db_user_obj1 = User(**self.fake_user_data1)
            db_user_obj2 = User(**self.fake_user_data2)

            db_user_obj1.restaurants.append(db_r_obj1)
            db_user_obj1.restaurants.append(db_r_obj2)

            db_user_obj2.restaurants.append(db_r_obj1)
            db_user_obj2.restaurants.append(db_r_obj2)

            db.add_all([db_r_obj1, db_r_obj2, db_user_obj1, db_user_obj2])
            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant"))
            db.execute(text("DELETE FROM user"))
            db.execute(text("DELETE FROM user_restaurant_intermediary"))
            db.commit()

    def test_read(self):
        """新增使用者與餐廳關聯測試"""

        with self.fake_database.get_db() as db:
            r_obj1, r_obj2 = self._get_restaurant_objs(db)
            u_obj1, u_obj2 = self._get_user_objs(db)

            u_obj1_restaurants = u_obj1.restaurants
            u_obj2_restaurants = u_obj2.restaurants

            self.assertIn(r_obj1, u_obj1_restaurants)
            self.assertIn(r_obj2, u_obj1_restaurants)
            self.assertIn(r_obj1, u_obj2_restaurants)
            self.assertIn(r_obj2, u_obj2_restaurants)

            self.assertIn(u_obj1, r_obj1.users)
            self.assertIn(u_obj2, r_obj1.users)
            self.assertIn(u_obj1, r_obj2.users)
            self.assertIn(u_obj2, r_obj2.users)

    def test_on_remove(self):
        """移除使用者與餐廳關聯測試"""

        with self.fake_database.get_db() as db:
            r_obj1, r_obj2 = self._get_restaurant_objs(db)
            u_obj1, u_obj2 = self._get_user_objs(db)

            u_obj1.restaurants.remove(r_obj1)
            u_obj2.restaurants.remove(r_obj2)

            db.commit()

            new_r_obj1, new_r_obj2 = self._get_restaurant_objs(db)
            new_u_obj1, new_u_obj2 = self._get_user_objs(db)

            self.assertIn(new_r_obj2, new_u_obj1.restaurants)
            self.assertNotIn(new_r_obj1, new_u_obj1.restaurants)
            self.assertIn(new_r_obj1, new_u_obj2.restaurants)
            self.assertNotIn(new_r_obj2, new_u_obj2.restaurants)

            self.assertIn(new_u_obj1, new_r_obj2.users)
            self.assertIn(new_u_obj2, new_r_obj1.users)
            self.assertNotIn(new_u_obj1, new_r_obj1.users)
            self.assertNotIn(new_u_obj2, new_r_obj2.users)

    def test_on_delete_restaurant(self):
        """刪除餐廳物件後測試"""

        with self.fake_database.get_db() as db:
            r_obj1, r_obj2 = self._get_restaurant_objs(db)
            u_obj1, u_obj2 = self._get_user_objs(db)

            self.assertIsNotNone(r_obj1)
            self.assertIsNotNone(r_obj2)
            self.assertIsNotNone(u_obj1)
            self.assertIsNotNone(u_obj2)

            db.delete(r_obj1)
            db.commit()

            new_r_obj1, new_r_obj2 = self._get_restaurant_objs(db)
            new_u_obj1, new_u_obj2 = self._get_user_objs(db)

            self.assertIsNone(new_r_obj1)
            self.assertIsNotNone(new_r_obj2)
            self.assertIsNotNone(new_u_obj1)
            self.assertIsNotNone(new_u_obj2)

            self.assertIn(new_r_obj2, new_u_obj1.restaurants)
            self.assertIn(new_r_obj2, new_u_obj2.restaurants)

    def test_on_delete_user(self):
        """刪除使用者物件後測試"""

        with self.fake_database.get_db() as db:
            r_obj1, r_obj2 = self._get_restaurant_objs(db)
            u_obj1, u_obj2 = self._get_user_objs(db)

            self.assertIsNotNone(r_obj1)
            self.assertIsNotNone(r_obj2)
            self.assertIsNotNone(u_obj1)
            self.assertIsNotNone(u_obj2)

            db.delete(u_obj1)
            db.commit()

            new_r_obj1, new_r_obj2 = self._get_restaurant_objs(db)
            new_u_obj1, new_u_obj2 = self._get_user_objs(db)

            self.assertIsNone(new_u_obj1)
            self.assertIsNotNone(new_r_obj1)
            self.assertIsNotNone(new_r_obj2)
            self.assertIsNotNone(new_u_obj2)

            self.assertIn(new_u_obj2, new_r_obj1.users)
            self.assertIn(new_u_obj2, new_r_obj2.users)


class TestUserAndOAuthRelation(InitialDataBaseTest):
    """User model 與 OAuth model 一對一關聯性測試"""

    def _get_user_obj(self, db) -> "User":
        """取得資料庫中的 user 物件"""

        u_obj = db.query(User).filter(User.username == self.fake_user_data["username"]).first()

        return u_obj

    def _get_oauth_obj(self, db) -> "OAuth":
        """取得資料庫中的 oauth 物件"""

        o_obj = (
            db.query(OAuth)
            .filter(OAuth.access_token == self.fake_oauth_data["access_token"])
            .first()
        )

        return o_obj

    def setUp(self) -> None:
        """在每個測試前，先新增資料"""

        self.fake_user_data = FakeData.fake_user(is_oauth=True, number=1)
        self.fake_oauth_data = FakeData.fake_oauth(number=1)

        with self.fake_database.get_db() as db:
            db_user_obj = User(**self.fake_user_data)
            db_oauth_obj = OAuth(**self.fake_oauth_data)

            db_user_obj.oauth = db_oauth_obj

            db.add_all([db_user_obj, db_oauth_obj])
            db.commit()

    def tearDown(self) -> None:
        """在每個測試結束時，刪除資料表的資料"""

        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM oauth"))
            db.execute(text("DELETE FROM user"))
            db.commit()

    def test_read(self):
        """使用者和 oauth 關聯測試"""

        with self.fake_database.get_db() as db:
            u_obj = self._get_user_obj(db)
            o_obj = self._get_oauth_obj(db)

            self.assertIs(o_obj, u_obj.oauth)
            self.assertIs(u_obj, o_obj.user)

    def test_on_delete_user(self):
        """刪除使用者物件後後測試"""

        with self.fake_database.get_db() as db:
            u_obj = self._get_user_obj(db)
            o_obj = self._get_oauth_obj(db)

            self.assertIsNotNone(u_obj)
            self.assertIsNotNone(o_obj)

            db.delete(u_obj)
            db.commit()

            new_u_obj = self._get_user_obj(db)
            new_o_obj = self._get_oauth_obj(db)

            self.assertIsNone(new_u_obj)
            self.assertIsNone(new_o_obj)
