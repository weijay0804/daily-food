'''
Author: weijay
Date: 2023-04-24 23:09:25
LastEditors: weijay
LastEditTime: 2023-06-30 02:05:30
Description: 定義一些測試會用到的通用測試 case
'''


import os
import unittest

from tests.utils import FakeDataBase


class BaseDataBaseTestCase(unittest.TestCase):
    """如果會需要使用的測試資料庫的話，可以繼承這個類別

    Args:
        `fake_database`: 測試資料庫實例
    """

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
