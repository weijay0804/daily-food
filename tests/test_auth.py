'''
Author: andy
Date: 2023-06-20 23:23:55
LastEditors: weijay
LastEditTime: 2023-06-30 02:03:35
Description: auth 單元測試
'''

from app import auth
from app.database.model import User
from tests import BaseDataBaseTestCase
from tests.utils import FakeData


class TestAuth(BaseDataBaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """先新增 user 資料"""

        super().setUpClass()

        cls._fake_user = FakeData.fake_user()

        user = User(
            username=cls._fake_user["username"],
            email=cls._fake_user["email"],
            password=cls._fake_user["password_hash"],
        )

        with cls.fake_database.get_db() as db:
            db.add(user)
            db.commit()

    def test_authenticate_user_with_corret_password(self):
        with self.fake_database.get_db() as db:
            user = auth.authenticate_user(
                db, self._fake_user["username"], self._fake_user["password_hash"]
            )

            self.assertTrue(user)

    def test_authenticate_user_with_wrong_password(self):
        with self.fake_database.get_db() as db:
            user = auth.authenticate_user(db, self._fake_user["username"], "wrong password")

            self.assertFalse(user)

    def test_authenticate_user_with_not_exist_user(self):
        with self.fake_database.get_db() as db:
            user = auth.authenticate_user(db, "not exist user", self._fake_user["password_hash"])

            self.assertFalse(user)

    def test_create_access_token(self):
        acess_token = auth.create_access_token({"sub": "test_username"})

        self.assertIsNotNone(acess_token)
