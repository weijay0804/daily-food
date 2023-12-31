'''
Author: weijay
Date: 2023-04-27 14:59:26
LastEditors: weijay
LastEditTime: 2023-07-03 23:07:56
Description: 測試資料
'''

from datetime import time


class FakeRestaurantData:
    FAKE_RESTAURANT_NAME = ["金陵小火鍋", "長疆羊肉爐(平鎮店)", "豆魚町碳烤啤酒屋", "局外人甜點(自忠店)", "味亦美"]

    FAKE_RESTAURANT_ADDRESS = [
        "桃園市中壢區林森路106號",
        "桃園市中壢區自忠街66號",
        "桃園市中壢區環中東路二段777號",
        "桃園市平鎮區環南路三段269號",
        "桃園市平鎮區金陵路二段57號",
    ]

    FAKE_RESTAURANT_LAT_LNG = [
        (24.94197, 121.22291),
        (24.94097, 121.22354),
        (24.94283, 121.22705),
        (24.94306, 121.22496),
        (24.94509, 121.22648),
    ]

    FAKE_RESTAURANT_NAME_FAR = ["十色鍋物", "吾私拉麵", "福來鱔魚意麵", "億哥牛肉大王", "裕農燒肉飯"]

    FAKE_RESTAURANT_ADDRESS_FAR = [
        "台南市東區裕農路574號",
        "台南市東區中華東路二段3號",
        "台南市東區裕農路588號",
        "台南市東區裕農路582號",
        "台南市東區裕農路581號",
    ]

    FAKE_RESTAURANT_LAT_LNG_FAR = [
        (22.98854, 120.23418),
        (22.98829, 120.23394),
        (22.98854, 120.23483),
        (22.98896, 120.23459),
        (22.98885, 120.23370),
    ]


class FakeRestaurantOpenTimeData:
    DAY_OF_WEEK = [1, 2, 3, 4, 5, 6, 7]

    OPEN_TIME = [time(hour=12, minute=0), time(hour=9, minute=30), time(hour=15, minute=0)]
    CLOSE_TIME = [time(hour=20, minute=30), time(hour=21, minute=0), time(hour=22, minute=0)]


class FakeRestaurantType:
    NAME = ["中式", "美式", "義大利麵", "素食", "炸雞"]

    DESC = ["好好吃", "家的味道", "吃了會露出笑容", "開始養生吧"]


class FakeUser:
    USERNAME = ["user1", "user2", "user3", "user4"]
    EMAIL = ["user1@test.com", "user2@test.com", "user3@test.com", "user4@test.com"]
    PASSWORD = ["user1_password", "user2_password", "user3_password", "user4_password"]


class FakeOAuth:
    PROVIDER = ["google", "github", "facebook", "twitter"]
    ACCESS_TOKEN = ["token1", "token2", "token3", "token4"]
