# RWSDBv2.1 - API CRUD Операции

## 📋 Обзор

Приложение поддерживает все CRUD операции через REST API:

| Операция | HTTP Метод | Описание | Пример |
|----------|-----------|----------|--------|
| **Create** | POST | Создание нового ресурса | `POST /api/train` |
| **Read** | GET | Получение данных о ресурсе | `GET /api/train` |
| **Update** | PUT | Обновление существующего ресурса | `PUT /api/train/1` |
| **Delete** | DELETE | Удаление ресурса | `DELETE /api/train/1` |

---

## 🔧 1. GET – Получение данных о ресурсе

### Получить все записи из таблицы

**Запрос:**
```http
GET /api/{table_name}
```

**Примеры:**

```bash
# Получить все поезда
GET http://localhost:8080/api/train

# Получить всех пассажиров
GET http://localhost:8080/api/passenger

# Получить все билеты
GET http://localhost:8080/api/ticket

# Получить всех сотрудников
GET http://localhost:8080/api/employee

# Получить все платформы
GET http://localhost:8080/api/platform
```

**Ответ:**
```json
{
  "columns": ["train_id", "speed", "year_manufactured", "type", "carriage_count"],
  "data": [
    {
      "train_id": 1,
      "speed": 120,
      "year_manufactured": 2015,
      "type": "Пассажирский",
      "carriage_count": 12
    },
    ...
  ],
  "count": 15
}
```

### С фильтрацией и пагинацией

**Запрос:**
```http
GET /api/{table_name}?limit=10&offset=0
```

**Пример:**
```bash
# Получить первые 10 поездов
GET http://localhost:8080/api/train?limit=10&offset=0

# Получить следующие 10 поездов
GET http://localhost:8080/api/train?limit=10&offset=10
```

---

## ➕ 2. POST – Создание нового ресурса

### Создать новую запись

**Запрос:**
```http
POST /api/{table_name}
Content-Type: application/json
```

**Примеры:**

#### Создать новый поезд
```bash
curl -X POST http://localhost:8080/api/train \
  -H "Content-Type: application/json" \
  -d '{
    "speed": 200,
    "year_manufactured": 2024,
    "type": "Скоростной",
    "carriage_count": 10
  }'
```

#### Создать нового пассажира
```bash
curl -X POST http://localhost:8080/api/passenger \
  -H "Content-Type: application/json" \
  -d '{
    "passport_number": "AB1234567",
    "full_name": "Иванов Иван Иванович",
    "mobile_phone": "+375291234567",
    "remark": ""
  }'
```

#### Создать новый билет
```bash
curl -X POST http://localhost:8080/api/ticket \
  -H "Content-Type: application/json" \
  -d '{
    "carriage_number": 5,
    "seat_number": 42,
    "price": 150,
    "passenger_id": 1
  }'
```

#### Создать нового сотрудника
```bash
curl -X POST http://localhost:8080/api/employee \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Петров Петр Петрович",
    "position": "Начальник поезда",
    "experience": 10,
    "passport_data": "AB1234567"
  }'
```

#### Создать новую платформу
```bash
curl -X POST http://localhost:8080/api/platform \
  -H "Content-Type: application/json" \
  -d '{
    "capacity": 1000,
    "location": "Северная",
    "track_count": 4
  }'
```

**Ответ:**
```json
{
  "train_id": 16,
  "speed": 200,
  "year_manufactured": 2024,
  "type": "Скоростной",
  "carriage_count": 10
}
```

---

## ✏️ 3. PUT – Обновление существующего ресурса

### Обновить запись по ID

**Запрос:**
```http
PUT /api/{table_name}/{id}
Content-Type: application/json
```

**Примеры:**

#### Обновить поезд (ID=1)
```bash
curl -X PUT http://localhost:8080/api/train/1 \
  -H "Content-Type: application/json" \
  -d '{
    "speed": 140,
    "carriage_count": 14
  }'
```

#### Обновить пассажира (ID=1)
```bash
curl -X PUT http://localhost:8080/api/passenger/1 \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_phone": "+375299876543",
    "remark": "Постоянный клиент"
  }'
```

#### Обновить билет (ID=1)
```bash
curl -X PUT http://localhost:8080/api/ticket/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 200,
    "seat_number": 50
  }'
```

#### Обновить сотрудника (ID=1)
```bash
curl -X PUT http://localhost:8080/api/employee/1 \
  -H "Content-Type: application/json" \
  -d '{
    "position": "Старший начальник",
    "experience": 15
  }'
```

#### Обновить платформу (ID=1)
```bash
curl -X PUT http://localhost:8080/api/platform/1 \
  -H "Content-Type: application/json" \
  -d '{
    "capacity": 1500,
    "location": "Южная"
  }'
```

**Ответ:**
```json
{
  "train_id": 1,
  "speed": 140,
  "year_manufactured": 2015,
  "type": "Пассажирский",
  "carriage_count": 14
}
```

---

## 🗑️ 4. DELETE – Удаление ресурса

### Удалить запись по ID

**Запрос:**
```http
DELETE /api/{table_name}/{id}
```

**Примеры:**

```bash
# Удалить поезд с ID=16
curl -X DELETE http://localhost:8080/api/train/16

# Удалить пассажира с ID=25
curl -X DELETE http://localhost:8080/api/passenger/25

# Удалить билет с ID=10
curl -X DELETE http://localhost:8080/api/ticket/10

# Удалить сотрудника с ID=5
curl -X DELETE http://localhost:8080/api/employee/5

# Удалить платформу с ID=3
curl -X DELETE http://localhost:8080/api/platform/3
```

**Ответ:**
```json
{
  "success": true
}
```

---

## 📊 Структура таблиц

### train (Поезда)
| Столбец | Тип | Описание |
|---------|-----|----------|
| train_id | SERIAL | ID поезда (PK) |
| speed | INTEGER | Скорость (км/ч) |
| year_manufactured | INTEGER | Год выпуска |
| type | TEXT | Тип (Пассажирский/Грузовой/Скоростной) |
| carriage_count | INTEGER | Количество вагонов |

### passenger (Пассажиры)
| Столбец | Тип | Описание |
|---------|-----|----------|
| passenger_id | SERIAL | ID пассажира (PK) |
| passport_number | TEXT | Номер паспорта |
| full_name | TEXT | ФИО |
| mobile_phone | TEXT | Телефон |
| remark | TEXT | Примечание |

### ticket (Билеты)
| Столбец | Тип | Описание |
|---------|-----|----------|
| ticket_id | SERIAL | ID билета (PK) |
| carriage_number | INTEGER | Номер вагона |
| seat_number | INTEGER | Номер места |
| price | NUMERIC | Цена |
| passenger_id | INTEGER | ID пассажира (FK) |

### employee (Сотрудники)
| Столбец | Тип | Описание |
|---------|-----|----------|
| employee_id | SERIAL | ID сотрудника (PK) |
| full_name | TEXT | ФИО |
| position | TEXT | Должность |
| experience | INTEGER | Стаж (лет) |
| passport_data | TEXT | Паспортные данные |

### platform (Платформы)
| Столбец | Тип | Описание |
|---------|-----|----------|
| platform_id | SERIAL | ID платформы (PK) |
| capacity | INTEGER | Вместимость |
| location | TEXT | Расположение |
| track_count | INTEGER | Количество путей |

---

## 🔐 Аутентификация

Для входа как суперпользователь:

```bash
curl -X PATCH http://localhost:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"password": "4444"}'
```

**Ответ:**
```json
{
  "success": true,
  "message": "Authentication successful",
  "token": "4444"
}
```

---

## 📝 Примечания

1. **Все таблицы доступны для редактирования** - в текущей схеме нет справочных таблиц
2. **Автоматическое восстановление** - сервер автоматически восстанавливает подключение к БД после ошибок
3. **Валидация данных** - сервер проверяет корректность данных перед сохранением
4. **Каскадное удаление** - при удалении связанных записей могут возникнуть ошибки

---

**Версия:** 2.1 Modernized  
**Дата:** Февраль 2026
