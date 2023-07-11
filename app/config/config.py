'''
Author: weijay
Date: 2023-04-24 16:13:51
LastEditors: andy
LastEditTime: 2023-06-20 22:19:28
Description: Api 環境設定
'''

import os

from dotenv import load_dotenv

load_dotenv()

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
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
    JWT_TOKEN_EXPIRE_MIN = os.environ.get("JWT_TOKEN_EXPIRE_MIN", 15)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    pass


config_dict = {"dev": DevelopmentConfig, "test": TestConfig}
