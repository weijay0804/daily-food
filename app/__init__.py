'''
Author: weijay
Date: 2023-04-24 15:56:42
LastEditors: weijay
LastEditTime: 2023-04-24 17:55:12
Description: 初始化 App
'''


import os

from fastapi import FastAPI
from dotenv import load_dotenv

from app.config import config


def create_app(config_name: str = None) -> FastAPI:
    """根據傳入的設定建立 FastAPI 實例

    Args:
        config_name (str, optional): 如果沒有傳入值，就去環境變數找 `APP_ENV` 設定的值. Defaults to None.

    Returns:
        FastAPI: FastAPI 實例
    """

    if not config_name:
        load_dotenv()

        config_name = os.getenv("APP_ENV")

    api_config = config.config_dict[config_name]

    app = FastAPI(debug=api_config.DEBUG, title=api_config.TITLE, description=api_config.API_DESC)

    app.api_version = api_config.API_VERSION

    return app
