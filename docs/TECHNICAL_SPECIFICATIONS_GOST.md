# ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ К СЕРВЕРНОЙ ЧАСТИ
# RWSDBv2.1 - Railway Station Database System v2.1
# Лабораторная работа №1, Вариант 18

## 1. ОБЩИЕ ПОЛОЖЕНИЯ

### 1.1. Назначение документа
Настоящий документ определяет технические требования к серверной части прикладной программы управления базой данных железнодорожного вокзала.

### 1.2. Область применения
Серверная часть предназначена для предоставления HTTP API для работы с базой данных PostgreSQL.

### 1.3. Термины и определения
- **Backend** - серверная часть приложения
- **HTTP API** - программный интерфейс на основе HTTP протокола
- **JSON** - формат обмена данными JavaScript Object Notation
- **CRUD** - Create, Read, Update, Delete (создание, чтение, обновление, удаление)
- **Lookup Table** - справочная таблица

---

## 2. ТРЕБОВАНИЯ К БАЗЕ ДАННЫХ

### 2.1. Реляционная схема

```
┌─────────────┐       ┌─────────────┐
│   train     │       │   platform  │
│ (справочник)│       │ (справочник)│
└──────┬──────┘       └──────┬──────┘
       │                     │
       │                     │
       ▼                     ▼
┌─────────────┐       ┌─────────────┐
│  schedule   │◀──────┤   ticket    │
│   (основная)│       └──────┬──────┘
└──────┬──────┘              │
       │                     │
       │         ┌───────────┘
       │         │
       ▼         ▼
┌─────────────┐
│  passenger  │
└─────────────┘

┌─────────────┐       ┌─────────────┐
│   service   │       │   employee  │
│ (справочник)│       │ (справочник)│
└──────┬──────┘       └──────┬──────┘
       │                     │
       │         ┌───────────┘
       │         │
       ▼         ▼
┌─────────────┐       ┌─────────────┐
│ appointment │       │    work     │
└─────────────┘       └─────────────┘
```

### 2.2. Описание таблиц

#### 2.2.1. Справочные таблицы (Lookup Tables)

**Таблица: train (Поезда)**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| train_number | VARCHAR(20) | Уникальный номер поезда | PRIMARY KEY |
| speed | INTEGER | Максимальная скорость (км/ч) | CHECK (0 < speed ≤ 400) |
| year_of_manufacture | INTEGER | Год выпуска | CHECK (1900 ≤ year ≤ 2100) |
| type | VARCHAR(255) | Тип поезда | - |
| number_of_cars | INTEGER | Количество вагонов | CHECK (number_of_cars > 0) |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

**Таблица: platform (Платформы)**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| platform_number | VARCHAR(10) | Уникальный номер платформы | PRIMARY KEY |
| capacity | INTEGER | Вместимость (человек) | CHECK (capacity > 0) |
| location | VARCHAR(255) | Расположение | - |
| number_of_tracks | INTEGER | Количество путей | DEFAULT 1 |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

**Таблица: service (Услуги)**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| service_number | VARCHAR(20) | Уникальный номер услуги | PRIMARY KEY |
| service_name | VARCHAR(255) | Название услуги | NOT NULL |
| price | DECIMAL(10,2) | Стоимость | CHECK (price ≥ 0) |
| type | VARCHAR(100) | Тип услуги | - |
| date | DATE | Дата предоставления | DEFAULT CURRENT_DATE |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

**Таблица: employee (Сотрудники)**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| employee_number | VARCHAR(20) | Уникальный номер сотрудника | PRIMARY KEY |
| full_name | VARCHAR(255) | ФИО сотрудника | NOT NULL |
| position | VARCHAR(255) | Должность | - |
| work_experience | INTEGER | Стаж работы (лет) | DEFAULT 0 |
| passport_information | VARCHAR(100) | Паспортные данные | - |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

#### 2.2.2. Операционные таблицы

**Таблица: schedule (Расписание) - ОСНОВНАЯ ТАБЛИЦА**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| schedule_number | VARCHAR(20) | Уникальный номер рейса | PRIMARY KEY |
| arrival_time | TIME | Время прибытия | - |
| departure_time | TIME | Время отправления | - |
| date | DATE | Дата рейса | DEFAULT CURRENT_DATE |
| carriage_numbering | VARCHAR(100) | Нумерация вагонов | - |
| train_number | VARCHAR(20) | Номер поезда | FOREIGN KEY → train |
| platform_number | VARCHAR(10) | Номер платформы | FOREIGN KEY → platform |
| ticket_number | VARCHAR(20) | Номер билета | - |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

**Таблица: passenger (Пассажиры)**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| passenger_number | VARCHAR(20) | Уникальный номер пассажира | PRIMARY KEY |
| full_name | VARCHAR(255) | ФИО пассажира | NOT NULL |
| passport_number | VARCHAR(20) | Паспортный номер | UNIQUE NOT NULL |
| mobile_phone | VARCHAR(20) | Мобильный телефон | - |
| feature | TEXT | Особенности | - |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

**Таблица: ticket (Билеты)**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| ticket_number | VARCHAR(20) | Уникальный номер билета | PRIMARY KEY |
| carriage_number | VARCHAR(10) | Номер вагона | - |
| ticket_price | DECIMAL(10,2) | Стоимость билета | CHECK (ticket_price ≥ 0) |
| seat_number | VARCHAR(10) | Номер места | - |
| passenger_number | VARCHAR(20) | Номер пассажира | FOREIGN KEY → passenger |
| train_number | VARCHAR(20) | Номер поезда | FOREIGN KEY → train |
| purchase_date | DATE | Дата покупки | DEFAULT CURRENT_DATE |
| travel_date | DATE | Дата поездки | - |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

**Таблица: appointment (Назначения услуг)**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| appointment_id | SERIAL | Идентификатор назначения | PRIMARY KEY |
| employee_number | VARCHAR(20) | Номер сотрудника | FOREIGN KEY → employee |
| service_number | VARCHAR(20) | Номер услуги | FOREIGN KEY → service |
| appointment_date | DATE | Дата назначения | DEFAULT CURRENT_DATE |
| status | VARCHAR(50) | Статус | DEFAULT 'active' |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

**Таблица: work (Назначения на поезда)**

| Имя поля | Тип данных | Описание | Ограничения |
|----------|------------|----------|-------------|
| work_id | SERIAL | Идентификатор работы | PRIMARY KEY |
| train_number | VARCHAR(20) | Номер поезда | FOREIGN KEY → train |
| employee_number | VARCHAR(20) | Номер сотрудника | FOREIGN KEY → employee |
| work_date | DATE | Дата работы | DEFAULT CURRENT_DATE |
| role | VARCHAR(100) | Роль | - |
| status | VARCHAR(50) | Статус | DEFAULT 'active' |
| created_at | TIMESTAMP | Дата создания | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления | DEFAULT CURRENT_TIMESTAMP |

### 2.3. Классификация таблиц

#### Справочные таблицы (Lookup Tables)
Только для чтения для обычных пользователей. Запись требует прав суперпользователя:
- `train` - Поезда
- `platform` - Платформы
- `service` - Услуги
- `employee` - Сотрудники

#### Операционные таблицы
Доступны для чтения и записи всем пользователям:
- `schedule` - Расписание (основная таблица по умолчанию)
- `passenger` - Пассажиры
- `ticket` - Билеты
- `appointment` - Назначения услуг
- `work` - Назначения на поезда

---

## 3. РОЛЕВАЯ МОДЕЛЬ

### 3.1. Роль: Пользователь

**Права доступа:**
- Просмотр всех таблиц (GET запросы)
- Фильтрация содержимого таблиц
- Добавление записей в операционные таблицы (POST запросы)
- Обновление записей в операционных таблицах (PUT запросы)
- Удаление записей из операционных таблиц (DELETE запросы)
- Выполнение специальных запросов (SELECT)
- Сохранение результатов запросов в файл (JSON, CSV, Excel)

**Ограничения:**
- Запрещено изменение справочных таблиц (train, platform, service, employee)
- Запрещено создание бэкапов базы данных

### 3.2. Роль: Суперпользователь

**Права доступа:**
- Все права обычного пользователя
- Редактирование справочных таблиц (train, platform, service, employee)
- Создание бэкапов базы данных

**Аутентификация:**
- Для выполнения действий суперпользователя требуется ввод пароля
- Пароль передается в заголовке Authorization: Bearer {password}
- Пароль суперпользователя по умолчанию: 4444

---

## 4. ТРЕБОВАНИЯ К HTTP API

### 4.1. Общие требования

- Протокол: HTTP/1.1
- Формат запросов: JSON
- Формат ответов: JSON
- Кодировка: UTF-8

### 4.2. HTTP методы

| Метод | Описание |
|-------|----------|
| GET | Получение данных о ресурсе |
| POST | Создание нового ресурса |
| PUT | Обновление существующего ресурса |
| DELETE | Удаление ресурса |

### 4.3. URL ресурсы

| URL | Таблица | Описание |
|-----|---------|----------|
| `/api/train` | train | Поезда (справочник) |
| `/api/platform` | platform | Платформы (справочник) |
| `/api/service` | service | Услуги (справочник) |
| `/api/employee` | employee | Сотрудники (справочник) |
| `/api/schedule` | schedule | Расписание (основная таблица) |
| `/api/passenger` | passenger | Пассажиры |
| `/api/ticket` | ticket | Билеты |
| `/api/appointment` | appointment | Назначения услуг |
| `/api/work` | work | Назначения на поезда |

### 4.4. Специальные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| PATCH | `/api/custom_query` | Выполнение SQL запроса |
| POST | `/api/backup` | Создание бэкапа БД (суперпользователь) |
| PATCH | `/api/export` | Экспорт данных в файл |
| GET | `/api/statistics` | Статистика базы данных |

### 4.5. Форматы запросов

#### GET - Получение всех записей
```
GET /api/schedule
```

#### GET - Фильтрация
```
GET /api/schedule?train_number=001А&date=2025-01-15
```

#### POST - Создание записи
```json
POST /api/schedule
Content-Type: application/json

{
  "schedule_number": "SCH000001",
  "arrival_time": "10:30:00",
  "departure_time": "10:45:00",
  "date": "2025-01-15",
  "train_number": "001А",
  "platform_number": "1А"
}
```

#### PUT - Обновление записи
```json
PUT /api/schedule/SCH000001
Content-Type: application/json

{
  "arrival_time": "11:00:00"
}
```

#### DELETE - Удаление записи
```
DELETE /api/schedule/SCH000001
```

---

## 5. ТРЕБОВАНИЯ К СЕРВЕРНОЙ ЧАСТИ

### 5.1. Архитектура

- Тип: HTTP сервер
- Язык реализации: Python 3.8+
- Библиотека для работы с БД: libpq (через psycopg2-binary)
- Порт по умолчанию: 8080

### 5.2. Функциональные требования

**Сервер должен обеспечивать:**
1. Просмотр таблиц базы данных
2. Фильтрацию содержимого таблиц
3. Добавление записей в таблицы
4. Обновление записей в таблицах
5. Удаление записей из таблиц
6. Выполнение специальных запросов (SELECT)
7. Создание бэкапов базы данных
8. Сохранение результатов запросов в файлы (JSON, CSV, Excel)

### 5.3. Требования к обработке ошибок

- Все ошибки должны возвращаться в формате JSON
- Формат ответа при ошибке:
```json
{
  "error": "Описание ошибки",
  "code": "код_ошибки"
}
```

### 5.4. Требования к логированию

- Логирование всех запросов
- Логирование ошибок
- Логирование действий суперпользователя

---

## 6. ТРЕБОВАНИЯ К СКРИПТАМ БАЗЫ ДАННЫХ

### 6.1. Скрипт создания схемы
**Файл:** `database/postgres_create_schema_lab1.sql`

**Назначение:** Создание всех таблиц, ограничений, индексов и представлений

### 6.2. Скрипт наполнения справочников
**Файл:** `database/populate_lookup_tables_lab1.sql`

**Назначение:** Первичное наполнение справочных таблиц (train, platform, service, employee)

### 6.3. Скрипт генерации данных
**Файл:** `database/generate_main_data_lab1.sql`

**Назначение:** Генерация тестовых данных для операционных таблиц (не менее 100 записей на таблицу)

**Объем данных:**
- passenger: 300 записей
- schedule: 500 записей
- ticket: 500 записей
- appointment: 100 записей
- work: 200 записей

### 6.4. Скрипты бэкапа/восстановления
**Файлы:**
- `database/backup_database.bat` - создание бэкапа
- `database/restore_database.bat` - восстановление из бэкапа

---

## 7. ИНСТРУКЦИЯ ПО РАЗВЕРТЫВАНИЮ

### 7.1. Создание базы данных

```sql
CREATE DATABASE "Railway sstation";
```

### 7.2. Создание схемы

```bash
psql -h localhost -U postgres -d "Railway sstation" -f database/postgres_create_schema_lab1.sql
```

### 7.3. Наполнение справочников

```bash
psql -h localhost -U postgres -d "Railway sstation" -f database/populate_lookup_tables_lab1.sql
```

### 7.4. Генерация данных

```bash
psql -h localhost -U postgres -d "Railway sstation" -f database/generate_main_data_lab1.sql
```

### 7.5. Запуск сервера

```bash
python server.py
```

### 7.6. Проверка работы

```bash
curl http://localhost:8080/api/schedule
curl http://localhost:8080/api/statistics
```

---

## 8. КОНТРОЛЬНЫЙ ПРИМЕР

### 8.1. Получение расписания (GET)

**Запрос:**
```
GET http://localhost:8080/api/schedule
```

**Ответ:**
```json
{
  "columns": ["schedule_number", "arrival_time", "departure_time", "date", ...],
  "data": [
    {
      "schedule_number": "SCH000001",
      "arrival_time": "10:30:00",
      "departure_time": "10:45:00",
      "date": "2025-01-15",
      ...
    }
  ],
  "count": 500
}
```

### 8.2. Создание билета (POST)

**Запрос:**
```json
POST /api/ticket
Content-Type: application/json

{
  "ticket_number": "TKT000501",
  "carriage_number": "5",
  "ticket_price": 1500.00,
  "seat_number": "12В",
  "passenger_number": "PASS000001",
  "train_number": "001А"
}
```

### 8.3. Попытка изменения справочника без прав суперпользователя

**Запрос:**
```json
POST /api/train
Content-Type: application/json

{
  "train_number": "016А",
  "speed": 150,
  "type": "Пассажирский"
}
```

**Ответ:**
```json
{
  "error": "Superuser authentication required for lookup table modification",
  "code": "AUTH_REQUIRED"
}
```

---

## 9. ПРИЛОЖЕНИЕ А (СПРАВОЧНОЕ)
### Диаграмма UML

```
+----------------+          +----------------+
|    train       |          |   platform     |
+----------------+          +----------------+
| PK train_number|          | PK platform_no |
|    speed       |          |    capacity    |
|    year_...    |          |    location    |
|    type        |          |    no_tracks   |
|    no_cars     |          +----------------+
+----------------+                   |
        |                            |
        | 1                          | 1
        |                            |
        | N                          | N
+----------------+                   |
|   schedule     |◀──────────────────+
+----------------+
| PK schedule_no |
|    arrival_tm  |
|    depart_tm   |
|    date        |
| FK train_number|
| FK platform_no |
+----------------+
```

---

**Документ разработан в соответствии с требованиями ГОСТ**
**Версия:** 1.0
**Дата:** Март 2026
