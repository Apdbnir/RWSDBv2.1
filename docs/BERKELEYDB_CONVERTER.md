# Конвертер базы данных PostgreSQL в BerkeleyDB

## Технические требования

Конвертер предназначенся для преобразования таблиц базы данных PostgreSQL в набор отдельных баз данных BerkeleyDB.

### Основные требования

- Для каждой таблицы базы данных PostgreSQL создаётся соответствующая база данных BerkeleyDB
- В качестве ключей в базах данных BerkeleyDB используются первичные ключи таблиц PostgreSQL
- В качестве значений используются сериализованные значения столбцов в формате JSON
- Конвертер представляет собой программный модуль в составе системы RWSDBv2.3
- При запуске конвертер выполняет конвертацию всех таблиц и завершает работу

## Формат хранения данных

В таблице ниже приведено описание формата хранения данных, конвертированных из таблиц PostgreSQL в базы данных BerkeleyDB.

Таблица 3.1 – Формат хранения данных в BerkeleyDB

| Таблица PostgreSQL | Ключ BerkeleyDB | Значение (JSON) |
|-------------------|-----------------|-----------------|
| passenger | passenger_number | `{"passenger_number", "full_name", "passport_series", "passport_number", "phone", "address"}` |
| train | train_number | `{"train_number", "departure_city", "arrival_city", "departure_time", "arrival_time", "train_type"}` |
| platform | platform_number | `{"platform_number", "platform_type", "capacity", "status"}` |
| ticket | ticket_number | `{"ticket_number", "passenger_number", "train_number", "schedule_number", "seat_number", "price", "purchase_date"}` |
| schedule | schedule_number | `{"schedule_number", "train_number", "platform_number", "departure_time", "arrival_time", "status"}` |
| employee | employee_number | `{"employee_number", "full_name", "position", "hire_date", "phone", "passport_series", "passport_number"}` |
| work | {train_number}_{employee_number} | `{"train_number", "employee_number", "role", "start_date", "end_date"}` |
| service | service_number | `{"service_number", "service_name", "description", "cost"}` |
| appointment | {employee_number}_{service_number} | `{"employee_number", "service_number", "appointment_date", "status", "notes"}` |

## Алгоритм работы конвертера

Конвертер работает по следующему алгоритму:

1. **Подключение к базе данных PostgreSQL** - установление соединения с сервером PostgreSQL используя конфигурацию
2. **Получение метаданных** - извлечение информации о таблицах, их столбцах и содержимом
3. **Создание баз данных BerkeleyDB** - инициализация окружения BerkeleyDB и создание файлов баз данных
4. **Заполнение данными** - конвертация каждой записи в JSON формат и сохранение в BerkeleyDB
5. **Закрытие соединений** - корректное закрытие всех открытых соединений

## SQL-запросы для извлечения данных

Для извлечения информации из PostgreSQL используются следующие запросы:

### 1. Получение имён всех таблиц схемы public

```sql
SELECT table_name 
FROM information_schema.tables
WHERE table_schema = 'public'
```

### 2. Получение названий столбцов таблицы

```sql
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'table_name'
  AND table_schema = 'public'
ORDER BY ordinal_position
```

### 3. Получение данных таблицы

```sql
SELECT column1, column2, column3 FROM table_name
```

## Реализация

### Класс BerkeleyDBConverter

Основной функционал конвертера реализован в классе `BerkeleyDBConverter`.

#### Инициализация

```python
converter = BerkeleyDBConverter(
    pg_config={
        'host': 'localhost',
        'database': 'railway_station',
        'user': 'postgres',
        'password': 'postgres',
        'port': 5432
    },
    output_dir='berkeleydb'
)
```

#### Основные методы

- `connect_postgresql()` - подключение к PostgreSQL
- `disconnect_postgresql()` - отключение от PostgreSQL
- `init_berkeleydb_env()` - инициализация окружения BerkeleyDB
- `close_berkeleydb_env()` - закрытие окружения BerkeleyDB
- `get_table_columns(table_name)` - получение имён столбцов таблицы
- `get_table_data(table_name)` - получение всех данных таблицы
- `create_composite_key(row, key_columns)` - создание составного ключа
- `convert_table(table_name)` - конвертация одной таблицы
- `convert_all_tables()` - конвертация всех таблиц
- `run()` - запуск полного процесса конвертации

### Интеграция с сервером

Конвертер интегрирован в основной сервер и доступен через API endpoint `/api/lab3-convert`.

## Пример использования

### Запуск через API

```bash
curl -X POST http://localhost:8080/api/lab3-convert \
  -H "Authorization: Bearer your_password"
```

### Запуск как отдельный скрипт

```bash
cd backend
python berkeleydb_converter.py
```

## Результат работы

После завершения работы конвертера для каждой таблицы PostgreSQL будет создана отдельная база данных BerkeleyDB.

Содержимое созданной базы данных можно просмотреть с помощью утилиты `db_dump`:

```bash
db_dump berkeleydb/passenger.db
```

### Пример вывода db_dump для таблицы passenger

```
VERSION=3
format=print
type=hash
h_nelem=1000
db_pagesize=4096
HEADER=END
 1
 {"passenger_number": 1, "full_name": "Иванов Иван Иванович", "passport_series": "1234", "passport_number": "567890", "phone": "+375291234567", "address": "г. Минск, ул. Примерная, д. 1"}
 2
 {"passenger_number": 2, "full_name": "Петрова Мария Сергеевна", "passport_series": "5678", "passport_number": "123456", "phone": "+375331234567", "address": "г. Гомель, ул. Тестовая, д. 2"}
DATA=END
```

## Обработка составных ключей

Для таблиц со составными первичными ключами (`work`, `appointment`) конвертер создаёт композитный ключ в формате `{key1}_{key2}`:

```python
def create_composite_key(self, row, key_columns):
    """Create composite key from multiple columns"""
    key_parts = [str(row[col]) for col in key_columns]
    return '_'.join(key_parts)
```

### Пример составного ключа

| Таблица | Столбцы ключа | Результирующий ключ |
|---------|--------------|---------------------|
| work | train_number, employee_number | `101_5001` |
| appointment | employee_number, service_number | `5001_301` |

## Обработка типов данных

Конвертер автоматически обрабатывает специальные типы данных PostgreSQL:

- **Дата/время** - преобразуется в ISO формат через `isoformat()`
- **Decimal** - преобразуется в `float`
- **NULL** - сохраняется как `null` в JSON
- **Строки** - сохраняются как есть с кодировкой UTF-8

## Логирование

Конвертер использует систему логирования сервера для отслеживания процесса конвертации:

```
2026-04-03 18:00:00,123 - berkeleydb_converter - INFO - ✓ Connected to PostgreSQL: railway_station
2026-04-03 18:00:00,234 - berkeleydb_converter - INFO - ✓ Initialized BerkeleyDB environment
2026-04-03 18:00:00,345 - berkeleydb_converter - INFO - Converting table: passenger
2026-04-03 18:00:00,456 - berkeleydb_converter - INFO -   Found 1500 records
2026-04-03 18:00:01,567 - berkeleydb_converter - INFO -   ✓ Converted 1500 records to passenger.db
...
2026-04-03 18:00:10,890 - berkeleydb_converter - INFO - CONVERSION COMPLETE
2026-04-03 18:00:10,891 - berkeleydb_converter - INFO - Tables converted: 9/9
2026-04-03 18:00:10,892 - berkeleydb_converter - INFO - Total records: 5234
```

## Требования к окружению

Для работы конвертера необходимы следующие зависимости:

```
psycopg2-binary  # Для подключения к PostgreSQL
berkeleydb       # Для работы с BerkeleyDB (или bsddb3 как альтернатива)
```

Установка зависимостей:

```bash
pip install psycopg2-binary berkeleydb
```

## Структура выходных данных

После конвертации создаётся директория `berkeleydb/` со следующей структурой:

```
berkeleydb/
├── passenger.db
├── train.db
├── platform.db
├── ticket.db
├── schedule.db
├── employee.db
├── work.db
├── service.db
└── appointment.db
```

Каждый файл `.db` представляет собой отдельную базу данных BerkeleyDB, доступную для чтения через API BerkeleyDB.
