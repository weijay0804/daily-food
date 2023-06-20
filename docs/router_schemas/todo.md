# 代辦事項

整體的進度應該是：
餐廳系統 -> 使用者系統

## 餐廳系統
---
- [ ] 使用者自己建立餐廳  
  餐廳名稱、地址、電話、價錢、備註、營業時間、種類等，其中後端會串第三方 API 根據地址轉會成經緯度存入資料庫

    - [x] 新增餐廳基本資料
    - [x] 新增餐廳營業時間
    - [ ] 新增餐廳種類
    - [ ] ( 需要等待會員系統完成 ) 將餐廳關聯到對應的會員中，其他會員看不到別的會員新增的餐廳
    - [ ] ( 構想 ) 是否要新增一個功能是，使用者新增餐廳時可以設定要公開還是私人，如果公開，別的使用者也能看到，但推薦的時候，還是只推薦使用者收藏的餐廳
 - [ ] 推薦餐廳給使用者  
  根據使用者目前的位置和時間，根據餐廳經緯度和營業時間，隨機選擇餐廳給使用者 ( 目前不想做的太複雜，先很單純的用隨機推薦的方式就好，之後再根據種類、價錢之類的加入計算變數 )
  

 - [ ] ( 構想 ) - 串接第三方的 API 來獲得餐廳訊息  
  可以串接像是 Google API 來獲得餐廳的訊息，這樣使用者就不用自己建立，但以目前來說，先不把這個功能加進去，以減少複雜度，二來是 Google API 是要收費的，所以要先評估一下

## 使用者系統
---
- [x] 基本使用者註冊登入系統
  這個部分應該會搭配 JWT 實現

- [ ] OAuth2.0
  讓使用者可以使用 Google 登入，目前先用 Google 就好

## 權限保護
---
- [ ] 取得餐廳時保護
- [ ] 新增餐廳時保護
- [ ] 更新餐廳保護
- [ ] 刪除餐廳保護
- [ ] 新增餐廳營業時間保護
- [ ] 刪除餐廳營業時間保護
- [ ] 更新餐廳營業時間保護

## 重構
---
- [ ] 在有使用的測試資料庫的單元測試中，把初始化測試資料庫的部分獨立出來
  - [ ] `test_auth`
  - [ ] `test_db_curd`
  - [ ] `test_db_model_relation`
  - [ ] `test_db_model`
  - [ ] `test_routers`  
- [ ] 把有使用到需要產生測試資料的部分獨立出來
  - [ ] `test_db_curd.TestRestaurantCURD`
  - [ ] `test_db_curd.TestRestaurantOpenTimeCRUD`
  - [ ] `test_db_curd.TestUserCRUD`
  - [ ] `test_db_model.TestRestaurantModel`
  - [ ] `test_db_model.TestRestaurantOpenTimeModel`
  - [ ] `test_db_model.TestRestaurantTypeModel`
  - [ ] `test_db_model.TestUserModel`
  - [ ] `test_db_model.TestOAuthModel`
- [ ] 把跟 randomly 相關的操作單獨成一個測試 Case
  - [ ] `test_db_curd.test_get_restaurant_randomly_function`
  - [ ] `test_db_curd.test_get_restaurant_randomly_with_open_time_function`
  - [ ] `test_routers.test_read_retaurant_randomly_router`
  - [ ] `test_routers.test_read_retaurant_randomly_router_with_open_time`
- [ ] 重構 `tests.utils.FakeData`