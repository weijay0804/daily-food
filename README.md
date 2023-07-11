## Daily Food Api

一個能夠幫你決定要吃什麼的服務

> 目前架構是採用前後端分離，後端使用 FastAPI，前端目前是想說用 React

> 從最簡單的開始，目前先讓使用者能夠新增餐廳，在使用者不知到吃什麼的時候，根據距離隨機幫他選擇一種

### 環境架設

* 建立環境 & 安裝套件
``` bash
$ pipenv install
```

* 執行程式
``` bash
$ uvicorn main:app --reload --reload-dir main.py
```