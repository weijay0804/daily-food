'''
Author: weijay
Date: 2023-04-26 01:40:39
LastEditors: weijay
LastEditTime: 2023-04-26 20:42:27
Description: app.utils 單元測試
'''

import unittest
from unittest.mock import patch, MagicMock

import requests

from app.utils import LatLng, MapApi


class TestLatLng(unittest.TestCase):
    CASE = [
        (24.94093, 121.21433),
        (24.94112, 121.21438),
        (24.94057, 121.21526),
        (24.98239, 121.26795),
        (25.00352, 121.16513),
        (25.04174, 121.07653),
    ]

    def test_get_distance(self):
        lat = 24.94097
        lng = 121.21456

        lat_min, lat_max, lng_min, lng_max = LatLng(lat, lng).get_distance(0.5)

        r = []

        for d in self.CASE:
            d_lat, d_lng = d

            if lat_min <= d_lat <= lat_max and lng_min <= d_lng <= lng_max:
                r.append((d_lat, d_lng))

        self.assertEqual(
            r,
            [
                (24.94093, 121.21433),
                (24.94112, 121.21438),
                (24.94057, 121.21526),
            ],
        )


class TestMapApi(unittest.TestCase):
    def setUp(self) -> None:
        self.map_api = MapApi()

    def test_get_coords_with_vaild_address(self):
        execpt_result = (25.03299, 121.5648)

        with patch("requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "results": [
                    {
                        "locations": [
                            {
                                "latLng": {
                                    "lat": execpt_result[0],
                                    "lng": execpt_result[1],
                                }
                            }
                        ]
                    }
                ]
            }

            mock_post.return_value = mock_response

            result = self.map_api.get_coords("台北市信義區信義路五段7號")

            self.assertEqual(result, execpt_result)

    def test_get_coords_with_invild_address(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.ReadTimeout()

            result = self.map_api.get_coords("Invaild address")

            self.assertEqual(result, (None, None))
