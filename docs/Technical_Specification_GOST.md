# ТЕХНИЧЕСКОЕ ЗАДАНИЕ
## на разработку серверной части прикладной программы
### «Система управления базой данных железнодорожного вокзала RWSDBv2.1»

---

**Лист утверждения**

| Должность | Подпись | Ф.И.О. | Дата |
|-----------|---------|--------|------|
| Разработчик | | | |
| Заказчик | | | |

---

## СОДЕРЖАНИЕ

1. [Общие сведения](#1-общие-сведения)
2. [Назначение и цели разработки](#2-назначение-и-цели-разработки)
3. [Характеристика объектов автоматизации](#3-характеристика-объектов-автоматизации)
4. [Требования к системе](#4-требования-к-системе)
5. [Состав и содержание работ](#5-состав-и-содержание-работ)
6. [Порядок контроля и приемки](#6-порядок-контроля-и-приемки)
7. [Требования к документации](#7-требования-к-документации)
8. [Источники разработки](#8-источники-разработки)

---

## 1. ОБЩИЕ СВЕДЕНИЯ

### 1.1 Наименование системы
**Полное наименование:** Система управления базой данных железнодорожного вокзала RWSDBv2.1 (Railway Station Database System v2.1)

**Краткое наименование:** RWSDBv2.1

### 1.2 Область применения
Система предназначена для автоматизации управления данными железнодорожного вокзала, включая учет сотрудников, студентов, учебных занятий, поездов, платформ, расписания, пассажиров и билетов.

### 1.3 Основание для разработки
Разработка осуществляется в рамках выполнения лабораторной работы №1 по дисциплине «Базы данных» (вариант 18).

### 1.4 Нормативные ссылки
- ГОСТ 34.602-2020 «Техническое задание на создание автоматизированной системы»
- PostgreSQL 10+ (система управления базами данных)
- RFC 7230-7237 (протокол HTTP/1.1)
- RFC 8259 (формат JSON)

---

## 2. НАЗНАЧЕНИЕ И ЦЕЛИ РАЗБОТКИ

### 2.1 Назначение системы
Серверная часть прикладной программы RWSDBv2.1 предназначена для:
- Хранения и управления данными железнодорожного вокзала
- Предоставления программного интерфейса (API) для клиентских приложений
- Обеспечения разграничения прав доступа между пользователями
- Автоматизации процессов резервного копирования и восстановления данных

### 2.2 Цели разработки
- Создание надежного и производительного сервера баз данных
- Обеспечение целостности и согласованности данных
- Реализация ролевой модели доступа
- Предоставление RESTful API для операций CRUD

---

## 3. ХАРАКТЕРИСТИКА ОБЪЕКТОВ АВТОМАТИЗАЦИИ

### 3.1 Реляционная схема базы данных

#### 3.1.1 Справочники (Lookup Tables)
Данные таблицы доступны для чтения всем пользователям, запись разрешена только суперпользователю.

**Таблица: positions (Должности сотрудников)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| position_id | SERIAL | Уникальный идентификатор должности | PRIMARY KEY |
| name | VARCHAR(255) | Наименование должности | UNIQUE, NOT NULL |
| description | TEXT | Описание должности | |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: subjects (Учебные предметы/дисциплины)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| subject_id | SERIAL | Уникальный идентификатор предмета | PRIMARY KEY |
| subject_name | VARCHAR(255) | Наименование предмета | UNIQUE, NOT NULL |
| credits | INTEGER | Количество кредитов | DEFAULT 0 |
| description | TEXT | Описание предмета | |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: lesson_types (Типы занятий)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| type_id | SERIAL | Уникальный идентификатор типа занятия | PRIMARY KEY |
| type_name | VARCHAR(100) | Наименование типа занятия | UNIQUE, NOT NULL |
| description | TEXT | Описание типа занятия | |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

#### 3.1.2 Операционные таблицы
Данные таблицы доступны для чтения и записи всем авторизованным пользователям.

**Таблица: employees (Сотрудники) — ОСНОВНАЯ ТАБЛИЦА**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| employee_id | SERIAL | Уникальный идентификатор сотрудника | PRIMARY KEY |
| full_name | VARCHAR(255) | ФИО сотрудника | NOT NULL |
| position | VARCHAR(255) | Должность | FOREIGN KEY → positions.name |
| experience | INTEGER | Стаж работы (лет) | DEFAULT 0 |
| hire_date | DATE | Дата приема на работу | DEFAULT CURRENT_DATE |
| salary | DECIMAL(10,2) | Заработная плата | DEFAULT 0 |
| phone | VARCHAR(20) | Телефон | |
| email | VARCHAR(255) | Электронная почта | |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: groups (Учебные группы)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| group_id | SERIAL | Уникальный идентификатор группы | PRIMARY KEY |
| group_name | VARCHAR(50) | Наименование группы | UNIQUE, NOT NULL |
| year | INTEGER | Год набора | |
| specialty | VARCHAR(255) | Специальность | |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: students (Студенты)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| student_id | SERIAL | Уникальный идентификатор студента | PRIMARY KEY |
| full_name | VARCHAR(255) | ФИО студента | NOT NULL |
| group_id | INTEGER | Идентификатор группы | FOREIGN KEY → groups.group_id |
| birth_date | DATE | Дата рождения | |
| phone | VARCHAR(20) | Телефон | |
| email | VARCHAR(255) | Электронная почта | |
| enrollment_date | DATE | Дата зачисления | DEFAULT CURRENT_DATE |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: lessons (Занятия)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| lesson_id | SERIAL | Уникальный идентификатор занятия | PRIMARY KEY |
| subject_id | INTEGER | Идентификатор предмета | FOREIGN KEY → subjects.subject_id |
| lesson_type_id | INTEGER | Идентификатор типа занятия | FOREIGN KEY → lesson_types.type_id |
| lesson_date | DATE | Дата занятия | |
| room | VARCHAR(20) | Аудитория | |
| start_time | TIME | Время начала | |
| end_time | TIME | Время окончания | |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: marks (Оценки)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| mark_id | SERIAL | Уникальный идентификатор оценки | PRIMARY KEY |
| student_id | INTEGER | Идентификатор студента | FOREIGN KEY → students.student_id |
| lesson_id | INTEGER | Идентификатор занятия | FOREIGN KEY → lessons.lesson_id |
| mark_value | INTEGER | Значение оценки | CHECK (2-5) |
| mark_date | DATE | Дата выставления | DEFAULT CURRENT_DATE |
| comment | TEXT | Комментарий | |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: employees_subjects (Сотрудники-Предметы)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| id | SERIAL | Уникальный идентификатор связи | PRIMARY KEY |
| employee_id | INTEGER | Идентификатор сотрудника | FOREIGN KEY → employees.employee_id |
| subject_id | INTEGER | Идентификатор предмета | FOREIGN KEY → subjects.subject_id |
| assigned_date | DATE | Дата назначения | DEFAULT CURRENT_DATE |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |
| | | | UNIQUE (employee_id, subject_id) |

**Таблица: trains (Поезда)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| train_id | SERIAL | Уникальный идентификатор поезда | PRIMARY KEY |
| train_number | VARCHAR(20) | Номер поезда | UNIQUE |
| speed | INTEGER | Скорость (км/ч) | CHECK (0-400] |
| year_manufactured | INTEGER | Год выпуска | CHECK (1900-2100) |
| type | VARCHAR(255) | Тип поезда | |
| carriage_count | INTEGER | Количество вагонов | CHECK > 0 |
| route | VARCHAR(255) | Маршрут | |
| status | VARCHAR(50) | Статус | DEFAULT 'active' |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: platforms (Платформы)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| platform_id | SERIAL | Уникальный идентификатор платформы | PRIMARY KEY |
| location | VARCHAR(255) | Расположение | |
| capacity | INTEGER | Вместимость | CHECK > 0 |
| platform_number | INTEGER | Номер платформы | |
| status | VARCHAR(50) | Статус | DEFAULT 'active' |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: schedules (Расписание)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| schedule_id | SERIAL | Уникальный идентификатор расписания | PRIMARY KEY |
| arrival_time | TIME | Время прибытия | |
| departure_time | TIME | Время отправления | |
| date | DATE | Дата | DEFAULT CURRENT_DATE |
| train_id | INTEGER | Идентификатор поезда | FOREIGN KEY → trains.train_id |
| platform_id | INTEGER | Идентификатор платформы | FOREIGN KEY → platforms.platform_id |
| ticket_id | INTEGER | Идентификатор билета | |
| status | VARCHAR(50) | Статус | DEFAULT 'scheduled' |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: passengers (Пассажиры)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| passenger_id | SERIAL | Уникальный идентификатор пассажира | PRIMARY KEY |
| full_name | VARCHAR(255) | ФИО пассажира | NOT NULL |
| passport_number | VARCHAR(20) | Номер паспорта | UNIQUE |
| contact_info | TEXT | Контактная информация | |
| birth_date | DATE | Дата рождения | |
| email | VARCHAR(255) | Электронная почта | |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: tickets (Билеты)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| ticket_id | SERIAL | Уникальный идентификатор билета | PRIMARY KEY |
| seat_number | VARCHAR(10) | Номер места | |
| price | DECIMAL(10,2) | Цена | CHECK ≥ 0 |
| passenger_id | INTEGER | Идентификатор пассажира | FOREIGN KEY → passengers.passenger_id |
| train_id | INTEGER | Идентификатор поезда | FOREIGN KEY → trains.train_id |
| purchase_date | DATE | Дата покупки | DEFAULT CURRENT_DATE |
| travel_date | DATE | Дата поездки | |
| status | VARCHAR(50) | Статус | DEFAULT 'active' |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: assignments (Назначения сотрудников)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| assignment_id | SERIAL | Уникальный идентификатор назначения | PRIMARY KEY |
| employee_id | INTEGER | Идентификатор сотрудника | FOREIGN KEY → employees.employee_id |
| train_id | INTEGER | Идентификатор поезда | FOREIGN KEY → trains.train_id |
| assignment_date | DATE | Дата назначения | DEFAULT CURRENT_DATE |
| end_date | DATE | Дата окончания | |
| role | VARCHAR(100) | Роль | |
| status | VARCHAR(50) | Статус | DEFAULT 'active' |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: services (Услуги)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| service_id | SERIAL | Уникальный идентификатор услуги | PRIMARY KEY |
| service_name | VARCHAR(255) | Наименование услуги | NOT NULL |
| price | DECIMAL(10,2) | Цена | CHECK ≥ 0 |
| type | VARCHAR(100) | Тип услуги | |
| description | TEXT | Описание | |
| service_date | DATE | Дата оказания | DEFAULT CURRENT_DATE |
| available | BOOLEAN | Доступность | DEFAULT TRUE |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

**Таблица: service_assignments (Назначения услуг)**

| Поле | Тип данных | Описание | Ограничения |
|------|------------|----------|-------------|
| service_assignment_id | SERIAL | Уникальный идентификатор назначения | PRIMARY KEY |
| service_id | INTEGER | Идентификатор услуги | FOREIGN KEY → services.service_id |
| employee_id | INTEGER | Идентификатор сотрудника | FOREIGN KEY → employees.employee_id |
| assignment_date | DATE | Дата назначения | DEFAULT CURRENT_DATE |
| status | VARCHAR(50) | Статус | DEFAULT 'active' |
| created_at | TIMESTAMP | Дата создания записи | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | Дата обновления записи | DEFAULT CURRENT_TIMESTAMP |

### 3.2 Ролевая модель доступа

#### 3.2.1 Роль «Пользователь» (Regular User)
Пользователь обладает правами:
- Просмотра всех таблиц (GET-запросы)
- Сохранения результатов запросов (экспорт в JSON, CSV, Excel)
- Редактирования всех таблиц, **кроме справочных**

| Операция | Справочники | Операционные таблицы |
|----------|-------------|---------------------|
| SELECT (чтение) | ✓ | ✓ |
| INSERT (добавление) | ✗ | ✓ |
| UPDATE (обновление) | ✗ | ✓ |
| DELETE (удаление) | ✗ | ✓ |
| BACKUP (резервное копирование) | ✗ | ✗ |
| EXPORT (экспорт результатов) | ✓ | ✓ |
| CUSTOM_QUERY (выполнение запросов) | ✓ | ✓ |

#### 3.2.2 Роль «Суперпользователь» (Superuser)
Суперпользователь обладает теми же правами, что и обычный пользователь, **плюс**:
- Возможность редактирования справочных таблиц
- Возможность создания бэкапов базы данных

**Важно:** Для выполнения действий от имени суперпользователя приложение должно запрашивать пароль суперпользователя.

| Операция | Справочники | Операционные таблицы |
|----------|-------------|---------------------|
| SELECT (чтение) | ✓ | ✓ |
| INSERT (добавление) | ✓ | ✓ |
| UPDATE (обновление) | ✓ | ✓ |
| DELETE (удаление) | ✓ | ✓ |
| BACKUP (резервное копирование) | ✓ | ✓ |
| EXPORT (экспорт результатов) | ✓ | ✓ |
| CUSTOM_QUERY (выполнение запросов) | ✓ | ✓ |

#### 3.2.3 Аутентификация суперпользователя
Аутентификация осуществляется через передачу пароля в заголовке HTTP-запроса:
```
Authorization: Bearer {admin_password}
```

Пароль суперпользователя хранится в конфигурационном файле `config.json`:
```json
{
  "admin_password": "4444"
}
```

### 3.3 Основная таблица приложения
**Таблица по умолчанию:** `employees` (Сотрудники)

При старте приложения пользователю отображается содержимое таблицы `employees`.

---

## 4. ТРЕБОВАНИЯ К СИСТЕМЕ

### 4.1 Функциональные требования

#### 4.1.1 Архитектура системы
Серверная часть прикладной программы должна быть реализована в виде **HTTP-сервера**.

**Требования к формату обмена:**
- Тела запросов: формат JSON
- Тела ответов: формат JSON

#### 4.1.2 HTTP-методы для работы с ресурсами
Для взаимодействия с ресурсами (таблицами) должны использоваться стандартные HTTP-методы:

| Метод | Назначение |
|-------|------------|
| GET | Получение данных о ресурсе (просмотр таблиц, фильтрация) |
| POST | Создание нового ресурса (добавление записи в таблицу) |
| PUT | Обновление существующего ресурса (обновление записи) |
| DELETE | Удаление ресурса (удаление записи из таблицы) |

**Требование:** Каждый ресурс должен быть доступен по уникальному URL.

#### 4.1.3 Операции для работы с базой данных
Серверная часть прикладной программы должна предоставлять следующие операции:

| Операция | Описание | HTTP-метод | URL |
|----------|----------|------------|-----|
| Просмотр таблиц | Получение всех записей из таблицы | GET | `/api/{table}` |
| Фильтрация содержимого таблиц | Получение записей по условию | GET | `/api/{table}?field=value` |
| Добавление записей в таблицы | Создание новой записи | POST | `/api/{table}` |
| Обновление записей в таблицах | Изменение существующей записи | PUT | `/api/{table}/{id}` |
| Удаление записей из таблиц | Удаление записи | DELETE | `/api/{table}/{id}` |
| Выполнение специальных запросов | Произвольные SELECT-запросы | PATCH | `/api/custom_query` |
| Создание бэкапов базы данных | Резервное копирование (суперпользователь) | POST | `/api/backup` |
| Сохранение результатов запросов в файл | Экспорт в JSON/CSV/Excel | PATCH | `/api/export` |

### 4.2 Требования к данным

#### 4.2.1 Объемы данных
| Таблица | Минимальное количество записей |
|---------|-------------------------------|
| employees | 100 |
| students | 200 |
| groups | 20 |
| marks | 500 |
| lessons | 100 |
| trains | 50 |
| platforms | 20 |
| schedules | 100 |
| passengers | 100 |
| tickets | 100 |
| positions | 25 |
| subjects | 20 |
| lesson_types | 10 |

#### 4.2.2 Целостность данных
- Все внешние ключи должны быть определены
- Должны быть реализованы ограничения CHECK
- Должны быть реализованы триггеры валидации

### 4.3 Технические требования

#### 4.3.1 Программное окружение
- **СУБД:** PostgreSQL 10+
- **Язык сервера:** Python 3.8+
- **Библиотека доступа к БД:** psycopg2 (на основе libpq)
- **Протокол:** HTTP/1.1 (REST)

#### 4.3.2 Требования к серверу
- Поддержка многопоточной обработки запросов
- Таймаут соединений
- Логирование событий

#### 4.3.3 Форматы обмена
- **Запросы:** JSON
- **Ответы:** JSON
- **Экспорт:** JSON, CSV, Excel (XLSX)

### 4.4 Требования к надежности
- Автоматическое восстановление соединения с БД
- Обработка транзакционных ошибок (ROLLBACK)
- Резервное копирование по требованию

### 4.5 Триггеры и функции
Система должна включать:
- Автоматическое обновление поля `updated_at`
- Валидацию данных (проверка оценок, должностей)
- Защиту справочников от несанкционированной записи
- Каскадное удаление связанных записей
- Функции для получения статистики

---

## 5. СОСТАВ И СОДЕРЖАНИЕ РАБОТ

### 5.1 Этапы разработки

| Этап | Наименование работ | Результат |
|------|-------------------|-----------|
| 1 | Разработка спецификаций | Техническое задание (ГОСТ) |
| 2 | Создание схемы БД | postgres_create_schema.sql |
| 3 | Наполнение справочников | postgres_populate_lookup_tables.sql |
| 4 | Генерация данных | postgres_generate_main_data.sql |
| 5 | Разработка функций и триггеров | postgres_functions_triggers.sql |
| 6 | Создание скриптов бэкапа | postgres_backup_restore.sql |
| 7 | Программирование сервера | server.py |
| 8 | Тестирование | tests/test_basic.py, test_api.bat |
| 9 | Документирование | README.md, API_INSTRUCTIONS.md |

### 5.2 Скрипты базы данных

#### 5.2.1 Скрипт создания схемы
**Файл:** `database/postgres_create_schema.sql`

Содержит:
- Создание всех таблиц (19 таблиц)
- Определение первичных и внешних ключей
- Создание индексов для производительности
- Создание представлений (views)
- Комментарии к таблицам

#### 5.2.2 Скрипт наполнения справочников
**Файл:** `database/postgres_populate_lookup_tables.sql`

Содержит:
- INSERT для таблицы positions (25 записей)
- INSERT для таблицы subjects (20 записей)
- INSERT для таблицы lesson_types (10 записей)

#### 5.2.3 Скрипт генерации данных
**Файл:** `database/postgres_generate_main_data.sql`

Содержит:
- Генерация данных для operational tables
- Использование generate_series для эффективности
- Реалистичные тестовые данные

#### 5.2.4 Скрипт функций и триггеров
**Файл:** `database/postgres_functions_triggers.sql`

Содержит:
- Функцию update_updated_at_column()
- Функцию validate_employee_position()
- Функцию validate_mark_value()
- Функцию check_lookup_table_access()
- Функцию get_database_statistics()
- Триггеры для всех таблиц
- Таблицу audit_log для аудита

#### 5.2.5 Скрипт резервного копирования
**Файл:** `database/postgres_backup_restore.sql`

Содержит:
- Таблицу backup_history
- Функции управления бэкапами
- Функции восстановления

### 5.3 Серверная часть

#### 5.3.1 Архитектура сервера
**Файл:** `server.py`

Компоненты:
- **DatabaseManager** — управление подключением к PostgreSQL
- **RequestHandler** — обработка HTTP-запросов
- **HTTPServer** — многопоточный HTTP-сервер

#### 5.3.2 Конечные точки API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/employees` | Получить всех сотрудников |
| GET | `/api/employees?id=1` | Получить сотрудника по ID |
| POST | `/api/employees` | Создать сотрудника |
| PUT | `/api/employees/{id}` | Обновить сотрудника |
| DELETE | `/api/employees/{id}` | Удалить сотрудника |
| GET | `/api/students` | Получить студентов |
| GET | `/api/groups` | Получить группы |
| GET | `/api/marks` | Получить оценки |
| GET | `/api/lessons` | Получить занятия |
| GET | `/api/subjects` | Получить предметы |
| GET | `/api/lesson-types` | Получить типы занятий |
| GET | `/api/positions` | Получить должности |
| GET | `/api/trains` | Получить поезда |
| GET | `/api/platforms` | Получить платформы |
| GET | `/api/schedules` | Получить расписание |
| GET | `/api/passengers` | Получить пассажиров |
| GET | `/api/tickets` | Получить билеты |
| POST | `/api/backup` | Создать бэкап (суперпользователь) |
| GET | `/api/statistics` | Получить статистику БД |

---

## 6. ПОРЯДОК КОНТРОЛЯ И ПРИЕМКИ

### 6.1 Тестирование

#### 6.1.1 Модульное тестирование
**Файл:** `tests/test_basic.py`

Проверяет:
- Импорт модулей
- Создание DatabaseManager

#### 6.1.2 Интеграционное тестирование
**Файл:** `tests/test_api.bat`

Проверяет:
- Доступность сервера
- Работу GET-запросов
- Работу фильтрации

#### 6.1.3 Тестирование с помощью psql
**Команды для тестирования:**

```bash
# Создание схемы
psql -h localhost -U postgres -d railway_station -f database/postgres_create_schema.sql

# Наполнение справочников
psql -h localhost -U postgres -d railway_station -f database/postgres_populate_lookup_tables.sql

# Генерация данных
psql -h localhost -U postgres -d railway_station -f database/postgres_generate_main_data.sql

# Создание функций и триггеров
psql -h localhost -U postgres -d railway_station -f database/postgres_functions_triggers.sql

# Проверка количества записей
psql -h localhost -U postgres -d railway_station -c "SELECT * FROM get_database_statistics();"
```

### 6.2 Критерии приемки

| Критерий | Требование | Статус |
|----------|------------|--------|
| Схема БД создана | 19 таблиц | ✓ |
| Справочники наполнены | 55+ записей | ✓ |
| Данные сгенерированы | 1000+ записей | ✓ |
| Триггеры работают | 20+ триггеров | ✓ |
| API доступно | 17+ endpoints | ✓ |
| Роли реализованы | User/Superuser | ✓ |
| Бэкап работает | pg_dump | ✓ |
| libpq используется | psycopg2 | ✓ |

---

## 7. ТРЕБОВАНИЯ К ДОКУМЕНТАЦИИ

### 7.1 Состав документации

| Документ | Файл | Назначение |
|----------|------|------------|
| Техническое задание | docs/Technical_Specification_GOST.md | Требования к системе |
| Руководство пользователя | README.md | Общая информация |
| Инструкция по API | API_INSTRUCTIONS.md | Примеры запросов |
| Быстрый старт | QUICKSTART.md | Запуск системы |

### 7.2 Требования к оформлению
- Документация в формате Markdown
- Примеры кода с подсветкой синтаксиса
- Таблицы для структурированных данных

---

## 8. ИСТОЧНИКИ РАЗРАБОТКИ

### 8.1 Исходные документы
- Лабораторная работа №6 (1 семестр) — исходная десктопная версия
- Вариант 18 — индивидуальное задание

### 8.2 Используемые технологии
- **PostgreSQL 10+** — СУБД
- **Python 3.8+** — язык программирования
- **psycopg2-binary** — драйвер PostgreSQL (libpq wrapper)
- **http.server** — стандартная библиотека HTTP-сервера

### 8.3 Структура проекта

```
RWSDBv2.1/
├── database/
│   ├── postgres_create_schema.sql
│   ├── postgres_populate_lookup_tables.sql
│   ├── postgres_generate_main_data.sql
│   ├── postgres_functions_triggers.sql
│   └── postgres_backup_restore.sql
├── server.py
├── config.json
├── requirements.txt
├── tests/
│   ├── test_basic.py
│   └── test_api.bat
└── docs/
    └── Technical_Specification_GOST.md
```

---

## ПРИЛОЖЕНИЕ А
### Лист регистрации изменений

| Версия | Дата | Описание изменений | Разработчик |
|--------|------|-------------------|-------------|
| 2.1 | 2026-02-24 | Initial release | |

---

**Документ разработан в соответствии с требованиями ГОСТ 34.602-2020**

---

## ПРИЛОЖЕНИЕ Б
### Сводная таблица соответствия требованиям

| № | Требование | Статус | Подтверждение |
|---|------------|--------|---------------|
| 1 | HTTP-сервер | ✅ | `server.py`, классы HTTPServer, BaseHTTPRequestHandler |
| 2 | JSON формат | ✅ | Все запросы/ответы в JSON |
| 3 | HTTP-методы | ✅ | do_GET, do_POST, do_PUT, do_DELETE |
| 4 | Уникальные URL | ✅ | `/api/{table}`, `/api/{table}/{id}` |
| 5 | Просмотр таблиц | ✅ | GET `/api/{table}` |
| 6 | Фильтрация | ✅ | GET `/api/{table}?field=value` |
| 7 | Добавление записей | ✅ | POST `/api/{table}` |
| 8 | Обновление записей | ✅ | PUT `/api/{table}/{id}` |
| 9 | Удаление записей | ✅ | DELETE `/api/{table}/{id}` |
| 10 | Специальные запросы | ✅ | PATCH `/api/custom_query` |
| 11 | Бэкапы БД | ✅ | POST `/api/backup` (суперпользователь) |
| 12 | Сохранение в файл | ✅ | PATCH `/api/export` (JSON/CSV/Excel) |
| 13 | Права пользователя | ✅ | Чтение всех таблиц, запись кроме справочников |
| 14 | Права суперпользователя | ✅ | Все права + справочники + бэкапы |
| 15 | Аутентификация | ✅ | Заголовок `Authorization: Bearer {password}` |
| 16 | Справочные таблицы | ✅ | positions, subjects, lesson_types |
| 17 | Защита справочников | ✅ | Trigger + проверка в коде |
| 18 | Основная таблица | ✅ | employees (GET `/api/` возвращает employees) |
| 19 | Триггеры и функции | ✅ | `postgres_functions_triggers.sql` |
| 20 | Скрипты БД | ✅ | 5 SQL скриптов в `database/` |
| 21 | Тестирование psql | ✅ | `tests/test_database.bat` |
| 22 | libpq | ✅ | psycopg2 (Python libpq wrapper) |

**Итого:** 22 из 22 требований выполнены ✅
