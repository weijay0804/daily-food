# 跟 Restaurant 相關操作的 Router Schemas

- [跟 Restaurant 相關操作的 Router Schemas](#跟-restaurant-相關操作的-router-schemas)
  - [Restaurants](#restaurants)
    - [`Read`](#read)
    - [`Create`](#create)
  - [Restaurant](#restaurant)
    - [`Read`](#read-1)
    - [`Update`](#update)
    - [`Delete`](#delete)
  - [Restaurant Open Time](#restaurant-open-time)
    - [`Update`](#update-1)
    - [`Delete`](#delete-1)
  - [None](#none)


---
## Restaurants 

> 餐廳路由

( `/restaurants` )

---

### `Read`

> (GET) 取得多筆餐廳資料

Args:
* skip ( 相當於 offset )
* limit ( 一次最大的回傳資料量 MAX = 10)

Return
```json
{

    "items": [
        {
            "id" : 1,
            "name" : "鼎泰豐",
            "address" : "台北市信義區松高路一段",
            "phone" : "0228472392",
            "lat" : 23.00123,
            "lng" : 120.2314,
            "price" : "中",
            "is_open" : true
        },
        {
            "id" : 2,
            "name" : "麥當勞",
            "address" : "台北市信義區松仁路二段",
            "phone" : "022844313",
            "price" : "低",
            "lat" : 23.00123,
            "lng" : 120.2314,
            "is_open" : false
        }
    ]
}
```

---

### `Create`

> (POST) 新增一筆餐廳資料

Send
```json
{

    "name" : "鼎泰豐",
    "address" : "台北市信義區松高路一段",
    "phone" : "0228472392",
    "desc" : "好吃的小籠包",
    "price" : -1,
    "b_hours" : [
        {
            "day_of_week" : 1,
            "open_time" : "12:00",
            "close_time" : "20:00"
        },
        {
            "day_of_week" : 2,
            "open_time" : "12:00",
            "close_time" : "20:00"
        }
    ]
}
```

---

## Restaurant 
> 單一餐廳路由
> 
( `/restaurant/[restaurant_id]` )

---

### `Read`

> (GET) 取得 *`restaurant_id`* 餐廳資料

Return
```json
{
    
    "id" : 1,
    "name" : "鼎泰豐",
    "address" : "台北市信義區松高路一段",
    "phone" : "02254134",
    "lat" : 23.001,
    "lng" : 120.001,
    "desc" : "好吃的小籠包",
    "price" : 0,
    "b_hours" : [
        {
            "id" : 1,
            "day_of_week" : 1,
            "open_time" : "12:00",
            "close_time" : "20:00"
        },
        {
            "id" : 3,
            "day_of_week" : 3,
            "open_time" : "12:00",
            "close_time" : "20:00"
        }
    ]
    
}
```

---

### `Update`

> (PATCH) 更新 *`restaurant_id`* 餐廳資料

Send
使用 `patch` 方法，所以只需要傳送需要更新的資料即可
```json
{
    "name" : "更新資料",
    "adderss" : "更新資料",
    "phone" : "更新資料",
    "desc" : "更新資料",
    "price" : "更新資料"
}
```

---

### `Delete`

> (DELETE) 刪除 *`restaurant_id`* 餐廳資料

None

---
---
## Restaurant Open Time 
> 單一餐廳營業時間路由
( `/restaurant/[restaurant_id]/open_time/[open_time_id]` )

---

### `Update`

> (PATCH) 更新 *`open_time_id`* 營業時間資料

Send
使用 `patch` 方法，所以只需要傳送需要更新的資料即可
```json
{
    "day_of_week" : 2,
    "open_time" : "20:00",
    "close_time" : "21:00"
}
```

---

### `Delete`

> (DELETE) 刪除 *`open_time_id`* 營業時間的資料

None
---