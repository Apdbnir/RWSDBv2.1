# RWSDBv2.1 - Railway Station Database System v2.1

> Belarusian Railway Station Database Management System

## 🏗️ Структура проекта

```
RWSDBv2.1/
├── backend/              # Python HTTP сервер
│   ├── server.py        # Основной сервер
│   ├── __main__.py      # Точка входа
│   └── config.json      # Конфигурация
├── web/                 # React клиент
│   ├── src/
│   │   ├── components/  # React компоненты
│   │   ├── pages/       # Страницы
│   │   ├── context/     # React Context
│   │   ├── services/    # API сервисы
│   │   └── index.css    # Стили
│   ├── index.html
│   └── package.json
├── database/            # SQL скрипты БД
│   ├── postgres_create_schema_belarus.sql
│   ├── populate_russian_belarus_data.sql
│   └── update_belarus_data.sql
├── data/                # Данные и бэкапы
├── docs/                # Документация
└── tests/               # Тесты
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Установка зависимостей для всего проекта
npm install

# Установка зависимостей для веб-клиента
cd web && npm install

# Установка зависимостей для бэкенда (опционально)
cd backend && pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
# Создание базы данных
psql -h localhost -U postgres -d railway_station -f database/postgres_create_schema_belarus.sql

# Заполнение данными
psql -h localhost -U postgres -d railway_station -f database/populate_russian_belarus_data.sql
```

Или используйте готовый скрипт:
```bash
populate_belarus_data.bat
```

### 3. Запуск приложения

#### Вариант A: Запуск всего приложения сразу
```bash
npm start
```

#### Вариант B: Раздельный запуск

**Backend (порт 8080):**
```bash
npm run server
# или
cd backend && python server.py 8080
```

**Frontend (порт 3000):**
```bash
npm run dev
# или
cd web && npm run dev
```

## 📊 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/train` | Получить все поезда |
| GET | `/api/platform` | Получить все платформы |
| GET | `/api/service` | Получить все услуги |
| GET | `/api/employee` | Получить всех сотрудников |
| GET | `/api/schedule` | Получить расписание |
| GET | `/api/passenger` | Получить пассажиров |
| GET | `/api/ticket` | Получить билеты |
| POST | `/api/{table}` | Создать запись |
| PUT | `/api/{table}/{id}` | Обновить запись |
| DELETE | `/api/{table}/{id}` | Удалить запись |
| PATCH | `/api/custom_query` | Выполнить SQL запрос |
| POST | `/api/backup` | Создать бэкап (суперпользователь) |

## 🔐 Аутентификация

Пароль суперпользователя по умолчанию: **4444**

## 📱 Веб-интерфейс

Откройте **http://localhost:3000** в браузере.

### Разделы:
- **Агляд** - Обзор и статистика
- **Табліцы** - Работа с таблицами
- **Запыты** - SQL запросы
- **Спец. запыты** - Специальные запросы (50+)
- **Экспарт** - Экспорт данных
- **Бэкап** - Бэкап БД (суперпользователь)

## 🗄️ База данных

### Таблицы:
1. **train** - Поезда (LOOKUP)
2. **platform** - Платформы (LOOKUP)
3. **service** - Услуги (LOOKUP)
4. **employee** - Сотрудники (LOOKUP)
5. **schedule** - Расписание
6. **passenger** - Пассажиры
7. **ticket** - Билеты

### Специальные запросы

Приложение включает **50+ специальных запросов**:

#### Статистика:
- Количество записей в таблицах
- Типы поездов и их количество
- Загруженность платформ
- Должности сотрудников
- Услуги по типам

#### Аналитика:
- Продажи билетов по типам поездов
- Топ-10 загруженных направлений
- Скорость и эффективность поездов
- Ежедневная статистика
- Пассажиры с несколькими билетами

#### Расписание:
- Поезда сегодня
- Ближайшие отправления
- Минское направление

#### И другие...

## 🛠️ Технологии

### Backend:
- Python 3.x
- HTTP Server (http.server)
- PostgreSQL (psycopg2-binary)

### Frontend:
- React 19
- Vite
- React Router
- Tailwind CSS
- Axios

## 📝 Конфигурация

Файл `backend/config.json`:

```json
{
  "admin_password": "4444",
  "pg_host": "localhost",
  "pg_database": "Railway sstation",
  "pg_user": "postgres",
  "pg_password": "postgres",
  "pg_port": 5432
}
```

## 🧪 Тестирование

```bash
cd backend
python -m pytest ../tests/
```

## 📄 Документация

- [UPDATE_SUMMARY_RU.md](UPDATE_SUMMARY_RU.md) - История обновлений
- [SPECIAL_QUERIES_SUMMARY.md](SPECIAL_QUERIES_SUMMARY.md) - Специальные запросы
- [docs/](docs/) - Полная документация

## 🇧🇾 Belarusian Edition

Эта версия приложения включает:
- Белорусские названия поездов (001БЧ - 025БЧ)
- Города Беларуси (Минск, Брест, Гомель, Витебск, etc.)
- Русские/белорусские имена сотрудников
- Белорусские паспорта (формат MP XXXXXXX)
- Телефоны Беларуси (+375(29)XXX-XXXX)

## 📞 Поддержка

Для вопросов и предложений создайте Issue в репозитории.

---

**RWSDBv2.1** © 2025 Belarusian Railway
