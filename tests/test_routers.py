'''
Author: weijay
Date: 2023-04-25 16:26:37
LastEditors: weijay
LastEditTime: 2023-05-15 19:37:49
Description: Api Router 單元測試
'''


import os
import unittest
from unittest import mock

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.config import config
from app import create_app
from app.database.model import Restaurant
from app.routers import register_router
from tests.utils import FakeDataBase, FakeData
from app.routers.restaurant_router import get_db


class InitialTestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_app = create_app("test")

        register_router(cls.test_app, f"/api/{config.TestConfig.API_VERSION}")

        cls.fake_database = FakeDataBase()

        cls.fake_database.Base.metadata.create_all(bind=cls.fake_database.engine)

        cls.client = TestClient(cls.test_app)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fake_database.engine.clear_compiled_cache()
        cls.fake_database.engine.dispose()
        cls.fake_database.Base.metadata.drop_all(bind=cls.fake_database.engine)
        os.remove("test.db")


class TestResaurantRotuer(InitialTestClient):
    def setUp(self) -> None:
        self.test_app.dependency_overrides[get_db] = self.fake_database.override_get_db

    def tearDown(self) -> None:
        with self.fake_database.get_db() as db:
            db.execute(text("DELETE FROM restaurant"))
            db.commit()

    def test_read_restaurant_router(self):
        fake_data = FakeData.fake_restaurant()
        restaurant = Restaurant(**fake_data)

        with self.fake_database.get_db() as db:
            db.add(restaurant)
            db.commit()

        response = self.client.get("/api/v1/restaurant")

        data = response.json()["items"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        self.assertIsNotNone(data[0]["name"])
        self.assertIsNotNone(data[0]["address"])

    # 使用 測試方法層面 mock 直接替換掉 get_coords()
    @mock.patch("app.utils.MapApi.get_coords", return_value=(25.0, 121.0))
    def test_create_restaurant_router(self, mock_get_coords):
        fake_restaurant = FakeData.fake_restaurant(is_lat_lng=False)

        response = self.client.post(
            "/api/v1/restaurant",
            json=fake_restaurant,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "created."})

    def test_upate_restaurant_router(self):
        fake_data = FakeData.fake_restaurant()
        with self.fake_database.get_db() as db:
            db.add(Restaurant(**fake_data))
            db.commit()

        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

        response = self.client.patch(
            f"/api/v1/restaurant/{restaurant.id}",
            json={
                "name": "測試餐廳更新",
                "address": restaurant.address,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "測試餐廳更新")
        self.assertEqual(response.json()["address"], restaurant.address)

    def test_delete_restaurant_router(self):
        fake_data = FakeData.fake_restaurant()

        with self.fake_database.get_db() as db:
            db.add(Restaurant(**fake_data))
            db.commit()

        with self.fake_database.get_db() as db:
            restaurant = db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()

        response = self.client.delete(f"/api/v1/restaurant/{restaurant.id}")

        with self.fake_database.get_db() as db:
            deleted_restaurant = (
                db.query(Restaurant).filter(Restaurant.name == fake_data["name"]).first()
            )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(deleted_restaurant)

    def test_read_retaurant_randomly_router(self):
        inner_fake_data1 = FakeData.fake_restaurant()
        inner_fake_data2 = FakeData.fake_restaurant()
        outer_fake_data = FakeData.fake_restaurant_far()

        with self.fake_database.get_db() as db:
            db.add_all(
                [
                    Restaurant(**inner_fake_data1),
                    Restaurant(**inner_fake_data2),
                    Restaurant(**outer_fake_data),
                ]
            )

            db.commit()

        lat, lng = FakeData.fake_current_location()
        distance = 5.0

        response = self.client.get(
            f"/api/v1/restaurant/choice?lat={lat}&lng={lng}&distance={distance}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.json()['items'][0]["name"]
            in (inner_fake_data1["name"], inner_fake_data2["name"])
        )
        self.assertEqual(len(response.json()['items']), 1)

        response = self.client.get(
            f"/api/v1/restaurant/choice?lat={lat}&lng={lng}&distance={distance}&limit=2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['items']), 2)
