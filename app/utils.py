"""
Author: weijay
Date: 2023-03-21 01:19:20
LastEditors: weijay
LastEditTime: 2023-04-21 22:56:10
Description: 放一些輔助通用的函示
"""


from typing import Tuple
import math

from requests.exceptions import ReadTimeout
import requests


class LatLng:
    """經緯度轉換"""

    R = 6371  # 地球半徑 (km)

    def _to_radian(self, radius: float) -> float:
        return radius * 180 / math.pi

    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

    def _haversine(self, dis: float) -> Tuple[float, float]:
        """計算以經緯度為圓心， r為半徑的東西向半徑長度和南北向半徑長度

        Args:
            dis (int): 範圍 (km)

        Returns:
            Tuple[float, float]: [lat 方向半徑長度, lng 方向半徑長度]
        """

        # fmt:off
        d_lng = (
            2 * math.asin(math.sin(dis / (2 * self.R))) / math.cos(self.lat * math.pi / 180)
        )
        d_lng = self._to_radian(d_lng)

        d_lat = dis / self.R
        d_lat = self._to_radian(d_lat)

        return (d_lat, d_lng)

    def get_distance(self, dis: float) -> Tuple[float, float, float, float]:
        """取得以自身經緯度為圓心，dis 為半徑，計算出的矩形的四個點

        Args:
            dis (float): 半徑 (km)

        Returns:
            Tuple[float, float, float, float]: (lat_min, lat_max, lng_min, lng_max)
        """

        d_lat, d_lng = self._haversine(dis)

        return (self.lat - d_lat, self.lat + d_lat, self.lng - d_lng, self.lng + d_lng)


class MapApi:
    """地址轉換經緯度 (使用單例模式)"""

    BASE_URL = "https://www.mapquestapi.com/geocoding/v1"

    # TODO 這邊 key 不要使用參數傳入，而是直接讀取環境變數
    def __init__(self):
        # 檢查是不是第一個實例化的
        if not hasattr(MapApi, "_first_init"):
            self.api_key = "test_api"

            MapApi._first_init = True

    def __new__(cls):
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
