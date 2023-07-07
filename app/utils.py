"""
Author: weijay
Date: 2023-03-21 01:19:20
LastEditors: weijay
LastEditTime: 2023-04-21 22:56:10
Description: 放一些輔助通用的函示
"""


import os
from typing import Tuple

from dotenv import load_dotenv
from requests.exceptions import ReadTimeout
import requests


class MapApi:
    """地址轉換經緯度 (使用單例模式)"""

    BASE_URL = "https://www.mapquestapi.com/geocoding/v1"

    def __init__(self,map_api_key):
        # 檢查是不是第一個實例化的
        if not hasattr(MapApi, "_first_init"):
            # 取得 api key

            if not map_api_key:
                raise Exception("Can't load 'MAP_API_KEY' from .env file.")

            self.api_key = map_api_key

            MapApi._first_init = True

    def __new__(cls,*args):
        # 檢查之前有沒有實例化過，如果有直接回將該實例
        if not hasattr(MapApi, "_instance"):
            MapApi._instance = object.__new__(cls)

        return MapApi._instance

    def get_coords(self, address: str) -> Tuple[float, float]:
        """根據地址轉換成經緯度

        Args:
            address (str): 地址

        Returns:
            Tuple[float, float]: (緯度, 經度)
        """

        payload = {"location": address}

        try:
            resp = requests.post(
                f"{self.BASE_URL}/address?key={self.api_key}", json=payload, timeout=10
            )

        except ReadTimeout:
            return None, None

        coords = resp.json()["results"][0]["locations"][0]["latLng"]

        return coords.get("lat"), coords.get("lng")
