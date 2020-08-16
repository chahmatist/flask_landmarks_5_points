# Landmarks are 5 points
web-сервис (REST API) на flask, который принимает фронтальное изображение лица человека в формате 'jpg' или 'jpeg'
и везвращает координаты 5-и точек на лице (глаза и носа)

### Docker

Создание образа контейнера

Для создания собственного контейнера, находясь внутри директории face_detector необходимо выполнить команду:
```bash
$ docker build -t landmarks_5_points_app:v0.1 .
```
Запуск контейнера из собранного образа

Для запуска Docker контейнера из подготовленного вами образа необходимо выполнить команду 
```bash
$ docker run -d -p 5000:5000 landmarks_5_points_app:v0.1
```

#### Пример запроса

**Request**

```bash
$ curl -F file=@<picture file path> -F submit=OK http://localhost:5000/upload
```

**Response**

```json
{
  "status": "success",
  "points": [
    [
      "bounding box",
      [
        111,
        171,
        379,
        439
      ]
    ],
    "right_eye_0",
    [
      339,
      243
    ],
    "right_eye_1",
    [
      291,
      247
    ],
    "left_eye_2",
    [
      171,
      243
    ],
    "left_eye_3",
    [
      220,
      247
    ],
    "nose_4",
    [
      258,
      339
    ]
  ],
  "message": "photo uploaded"
}
```


