'''
Author: weijay
Date: 2023-04-24 23:09:47
LastEditors: weijay
LastEditTime: 2023-05-04 21:00:29
Description: DataBase ORM 模型單元測試
'''

import os
import unittest
from datetime import datetime

from app.schemas import restaurant_schema
from app.database.model import Restaurant
from app.database import crud
from tests.utils import FakeData, FakeDataBase


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
    def setUp(self) -> None:
        fake_restaurant = Restaurant(
            name="測試1",
            address="台北市信義區松壽路6段",
            lat=25.03586,
            lng=121.56433,
            phone="02-1284193212",
        )

        with self.fake_database.get_db() as db:
            db.add(fake_restaurant)
            db.commit()

    def test_create_restaurant(self):
        restaurant = Restaurant(
            name="測試2",
            address="新北市汐止區大同路一段",
            lat=25.05741,
            lng=121.63418,
        )

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

            self.assertIsNotNone(restaurant.id)
            self.assertEqual(restaurant.name, "測試2")
            self.assertEqual(restaurant.address, "新北市汐止區大同路一段")
            self.assertEqual(restaurant.lat, 25.05741)
            self.assertEqual(restaurant.lng, 121.63418)
            self.assertEqual(restaurant.phone, None)
            self.assertEqual(restaurant.is_enable, 1)
            self.assertTrue(isinstance(restaurant.create_at, datetime))

    def test_read_restaurant(self):
        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.name == "測試1").first()

        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.name, "測試1")
        self.assertEqual(restaurant.address, "台北市信義區松壽路6段")
        self.assertEqual(restaurant.lat, 25.03586)
        self.assertEqual(restaurant.lng, 121.56433)
        self.assertEqual(restaurant.phone, "02-1284193212")
        self.assertEqual(restaurant.is_enable, 1)
        self.assertTrue(isinstance(restaurant.create_at, datetime))
        self.assertEqual(restaurant.update_at, None)

    def test_update_restaurant(self):
        restaurant = Restaurant(name="測試3", address="test", lat=25.00000, lng=120.00000)

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

            restaurant = db.query(Restaurant).filter(Restaurant.name == "測試3").first()

            self.assertEqual(restaurant.address, "test")
            self.assertEqual(restaurant.update_at, None)

            restaurant.address = "update_test"
            restaurant.update_at = datetime.utcnow()
            db.commit()

            restaurant = db.query(Restaurant).filter(Restaurant.name == "測試3").first()

        self.assertEqual(restaurant.address, "update_test")
        self.assertTrue(isinstance(restaurant.update_at, datetime))

    def test_delete_restaurant(self):
        restaurant = Restaurant(name="測試4", address="test", lat=23.00000, lng=120.00000)

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

            restaurant = db.query(Restaurant).filter(Restaurant.name == "測試4").first()

            self.assertIsNotNone(restaurant)

            db.delete(restaurant)
            db.commit()

            restaurant = db.query(Restaurant).filter(Restaurant.name == "測試4").first()

        self.assertIsNone(restaurant)


class TestRestaurantCURD(InitialDataBaseTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        fake_data = []

        for _ in range(2):
            data = FakeData.fake_restaurant()
            fake_data.append(Restaurant(**data))

        with cls.fake_database.get_db() as db:
            db.add_all(fake_data)
            db.commit()
            db.close()

    def test_get_restaurants_function(self):
        with self.fake_database.get_db() as db:
            restaurants = crud.get_restaurants(db)

        self.assertTrue(isinstance(restaurants, list))
        self.assertTrue(isinstance(restaurants[0], Restaurant))

    def test_create_restaurant_function(self):
        fake_data = FakeData.fake_restaurant()

        restaurant = restaurant_schema.ResFullCreateModel(**fake_data, phone="0932212849")

        with self.fake_database.get_db() as db:
            db_restaurant = crud.create_restaurant(db, restaurant)

        self.assertIsNotNone(db_restaurant)
        self.assertTrue(isinstance(db_restaurant, Restaurant))
        self.assertEqual(db_restaurant.name, fake_data["name"])

    def test_update_restaurant_function(self):
        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.id == 1).first()

            update_data = restaurant_schema.ResFullCreateModel(
                name="測試2更新", address=restaurant.address, lat=restaurant.lat, lng=restaurant.lng
            )

            updated_restaurant = crud.update_restaurant(db, restaurant.id, update_data)

        self.assertIsNotNone(updated_restaurant)
        self.assertEqual(updated_restaurant.name, "測試2更新")
        self.assertEqual(updated_restaurant.address, restaurant.address)
        self.assertEqual(updated_restaurant.phone, restaurant.phone)

    def test_update_restaurant_function_with_not_exist_id(self):
        update_data = restaurant_schema.ResFullCreateModel(
            name="not exist", address="not exist", lat=23.001, lng=120.321
        )

        with self.fake_database.get_db() as db:
            upadted_restaurant = crud.update_restaurant(db, 1000, update_data)

        self.assertIsNone(upadted_restaurant)

    def test_delete_restaurant_function(self):
        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.id == 2).first()

            crud.delete_restaurant(db, restaurant.id)

            deleted_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant.id).first()

        self.assertIsNotNone(restaurant)
        self.assertIsNone(deleted_restaurant)

    def test_delete_restaurant_function_with_not_eixst_id(self):
        with self.fake_database.get_db() as db:
            deleted_restaurant = crud.delete_restaurant(db, 1000)

        self.assertIsNone(deleted_restaurant)

    def test_get_restaurant_randomly_function(self):
        inner_restaurant = Restaurant(
            name="範圍內餐廳", address="test address", lat=23.15668, lng=120.39037
        )

        outer_restaurant = Restaurant(
            name="範圍外餐廳", address="test address", lat=25.01681, lng=121.29261
        )

        with self.fake_database.get_db() as db:
            db.add_all([inner_restaurant, outer_restaurant])
            db.commit()

            random_restaurant = crud.get_restaurant_randomly(db, 23.15703, 120.390386, 0.2, 1)

        self.assertIsNotNone(random_restaurant)
        self.assertEqual(random_restaurant[0].name, "範圍內餐廳")
        self.assertEqual(len(random_restaurant), 1)
