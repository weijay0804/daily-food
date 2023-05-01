'''
Author: weijay
Date: 2023-04-26 01:40:39
LastEditors: weijay
LastEditTime: 2023-05-01 16:53:21
Description: app.utils 單元測試
'''

import os
import unittest
from unittest.mock import patch, MagicMock

import requests

from app.utils import MapApi


class TestMapApi(unittest.TestCase):
    def setUp(self) -> None:
        os.environ.setdefault("MAP_API_KEY", "test_api_key")
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
