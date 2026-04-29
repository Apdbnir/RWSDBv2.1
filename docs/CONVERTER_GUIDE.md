# BerkeleyDB Converter - Краткое руководство

## Что это такое?

BerkeleyDB Converter - это модуль конвертации данных из PostgreSQL в BerkeleyDB/JSON, интегрированный в систему RWSDBv2.3.

**Важно:** На Windows библиотеки BerkeleyDB (berkeleydb/bsddb3) не устанавливаются. Конвертер автоматически использует **JSON fallback режим**.

## Функциональность

Конвертер выполняет следующие действия:

1. Подключается к базе данных PostgreSQL
2. Извлекает метаданные таблиц (названия, столбцы, типы данных)
3. Получает все данные из каждой таблицы
4. Создаёт отдельные файлы для каждой таблицы:
   - **BerkeleyDB**: `.db` файлы (Linux/Mac с установленной библиотекой)
   - **JSON**: `.json` файлы (Windows fallback)
5. Конвертирует данные в JSON формат
6. Использует первичные ключи PostgreSQL как ключи в выходных файлах

## Использование

### Способ 1: Через веб-интерфейс

1. Войдите в систему как суперпользователь
2. Перейдите на страницу "Конвертация BerkeleyDB"
3. Нажмите кнопку "Начать конвертацию"
4. Дождитесь завершения процесса

### Способ 2: Через API

```bash
curl -X POST http://localhost:8080/api/lab3-convert \
  -H "Authorization: Bearer your_password"
```

### Способ 3: Как отдельный скрипт

```bash
cd backend
python berkeleydb_converter.py
```

## Формат данных

### Таблицы с простым первичным ключом

| PostgreSQL Table | BerkeleyDB Key | BerkeleyDB Value (JSON) |
|-----------------|----------------|------------------------|
| passenger | passenger_number | `{"passenger_number": 1, "full_name": "...", ...}` |
| train | train_number | `{"train_number": 101, "departure_city": "...", ...}` |
| employee | employee_number | `{"employee_number": 5001, "full_name": "...", ...}` |

### Таблицы с составным первичным ключом

| PostgreSQL Table | BerkeleyDB Key | BerkeleyDB Value (JSON) |
|-----------------|----------------|------------------------|
| work | {train_number}_{employee_number} | `{"train_number": 101, "employee_number": 5001, ...}` |
| appointment | {employee_number}_{service_number} | `{"employee_number": 5001, "service_number": 301, ...}` |

## Результат

После завершения конвертации создаётся директория `berkeleydb/` с файлами:

### На Windows (JSON режим):
```
berkeleydb/
├── passenger.json
├── train.json
├── platform.json
├── ticket.json
├── schedule.json
├── employee.json
├── work.json
├── service.json
└── appointment.json
```

### На Linux/Mac с BerkeleyDB:
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

## Проверка результатов

Для просмотра содержимого BerkeleyDB можно использовать утилиту `db_dump`:

```bash
db_dump berkeleydb/passenger.db
```

Пример вывода:

```
VERSION=3
format=print
type=hash
h_nelem=1000
db_pagesize=4096
HEADER=END
 1
 {"passenger_number": 1, "full_name": "Иванов Иван Иванович", ...}
 2
 {"passenger_number": 2, "full_name": "Петрова Мария Сергеевна", ...}
DATA=END
```

## Логирование

Все операции конвертации записываются в лог-файлы:

- `logs/server.log` - полный лог операций
- `logs/error.log` - только ошибки

Пример записи в логе (JSON режим):

```
2026-04-03 18:11:32,544 - berkeleydb_converter - INFO - Using JSON export mode (BerkeleyDB not available)
2026-04-03 18:11:32,544 - berkeleydb_converter - INFO - Converting table: passenger
2026-04-03 18:11:32,544 - berkeleydb_converter - INFO -   Found 30 records
2026-04-03 18:11:32,545 - berkeleydb_converter - INFO -   ✓ Exported 30 records to passenger.json
...
2026-04-03 18:11:32,546 - berkeleydb_converter - INFO - CONVERSION COMPLETE
2026-04-03 18:11:32,546 - berkeleydb_converter - INFO - Tables converted: 9/9
2026-04-03 18:11:32,546 - berkeleydb_converter - INFO - Total records: 291
```

## Требования

Для работы конвертера необходимы:

```bash
pip install psycopg2-binary
```

**Опционально** (только для Linux/Mac):
```bash
pip install berkeleydb   # или bsddb3
```

**На Windows** конвертер автоматически работает в JSON режиме без BerkeleyDB.

## Документация

Полная документация доступна в файле `docs/BERKELEYDB_CONVERTER.md`.
