'''
Author: weijay
Date: 2023-04-24 16:13:51
LastEditors: weijay
LastEditTime: 2023-04-24 16:54:20
Description: Api 環境設定
'''

import os

BASE_DIR = os.path.abspath(os.path.dirname(__name__))

API_DESC = """
## 這個是 Daily Food 應用程式的 API

目前想法很簡單，使用者新增餐廳，程式幫他選擇今天要吃什麼
"""


class BaseConfig:
    API_VERSION = "v1"
    DEBUG = False
    TITLE = "Daily Food"
    API_DESC = API_DESC


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    pass


config_dict = {"dev": DevelopmentConfig, "test": TestConfig}
