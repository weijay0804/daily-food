# 跟 Restaurant 相關操作的 Router Schemas

- [跟 Restaurant 相關操作的 Router Schemas](#跟-restaurant-相關操作的-router-schemas)
  - [Restaurants](#restaurants)
    - [Read](#read)
    - [Create](#create)
  - [Restaurant](#restaurant)
    - [Read](#read-1)
    - [Update](#update)
    - [Delete](#delete)
  - [Restaurant Open Times](#restaurant-open-times)
    - [Read](#read-2)
    - [Create](#create-1)
  - [Restaurant Open Time](#restaurant-open-time)
    - [Update](#update-1)
    - [Delete](#delete-1)


---
## Restaurants 

> 餐廳路由

( `/restaurants` )

---

### Read

> (GET) 取得多筆餐廳資料

Args:
* skip ( 相當於 offset )
* limit ( 一次最大的回傳資料量 MAX = 10)

Return
```json
{

    "items": [
        {
            "name" : "鼎泰豐",
            "address" : "台北市信義區松高路一段",
            "phone" : "0228472392",
            "is_open" : true
        },
        {
            "name" : "麥當勞",
            "address" : "台北市信義區松仁路二段",
            "phone" : "022844313",
            "is_open" : false
        }
    ]
}
```

---

### Create

> (POST) 新增一筆餐廳資料

Send
```json
{

    "name" : "鼎泰豐",
    "address" : "台北市信義區松高路一段",
    "phone" : "0228472392",

}
```

---

## Restaurant 
> 單一餐廳路由
> 
( `/restaurant/[restaurant_id]` )

---

### Read

> (GET) 取得 *`restaurant_id`* 餐廳資料

Return
```json
{
    
    "name" : "鼎泰豐",
    "address" : "台北市信義區松高路一段",
    "phone" : "02254134"
    
}
```

---

### Update

> (PATCH) 更新 *`restaurant_id`* 餐廳資料

Send
使用 `patch` 方法，所以只需要傳送需要更新的資料即可
```json
{
    "name" : "更新資料",
    "adderss" : "更新資料",
    "phone" : "更新資料"
}
```

---

### Delete

> (DELETE) 刪除 *`restaurant_id`* 餐廳資料

None

---
## Restaurant Open Times 
( `/restaurant/[restauratn_id]/open_time` )
> 餐廳營業時間路由

---

### Read

> (GET) 取得 *`restaurant_id`* 餐廳的所有營業時間資料

Return
```json
{
    "items" : [
        {
            "id" : 1,
            "day_of_week" : 1,
            "open_time" : "12:00",
            "close_time" : "21:00"
        },
        {
            "id" : 2,
            "day_of_week" : 3,
            "open_time" : "12:00",
            "close_time" : "21:00"
        }
    ]
}
```

---

### Create

> 新增一筆 *`restaurant_id`* 的營業時間資料

Send
```json
{
    "items" : [
        {
            "day_of_week" : 1,
            "open_time" : "12:00",
            "close_time" : "21:00"
        },
        {
            "day_of_week" : 2,
            "open_time" : "12:00",
            "close_time" : "21:00"
        }
    ]
}
```

---
## Restaurant Open Time 
( `/restaurant/[restaurant_id]/open_time/[open_time_id]` )
> 單一餐廳營業時間路由

---

### Update

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

### Delete

> (DELETE) 刪除 *`open_time_id`* 營業時間的資料

None

---