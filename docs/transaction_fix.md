# Исправление ошибки транзакции PostgreSQL

## Проблема

После выполнения неверного SQL-запроса (например, некорректный custom query) PostgreSQL прерывает текущую транзакцию. Все последующие запросы возвращают ошибку:

```json
{
  "error": "ОШИБКА: текущая транзакция прервана, команды до конца блока транзакции игнорируются"
}
```

Это происходит потому, что psycopg2 (интерфейс к libpq) по умолчанию работает в режиме транзакций, и при ошибке транзакция остаётся в состоянии "aborted" до явного rollback.

## Решение

В файл `server.py` добавлены следующие изменения:

### 1. Метод `_check_and_recover_connection()`

Этот метод проверяет состояние подключения и автоматически восстанавливает его после прерванной транзакции:

```python
def _check_and_recover_connection(self):
    """Check connection status and recover from aborted transaction if needed"""
    if not self.connection:
        return self._connect()
    
    try:
        # Test connection with a simple query
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return True
    except psycopg2.InternalError as e:
        # Transaction is aborted, need to rollback
        if "current transaction is aborted" in str(e).lower():
            logger.warning("Transaction aborted, rolling back...")
            try:
                self.connection.rollback()
                logger.info("Transaction rolled back successfully")
                return True
            except Exception as rollback_error:
                logger.error(f"Rollback failed: {rollback_error}")
                self.connection.close()
                return self._connect()
        return False
    except Exception as e:
        logger.error(f"Connection check failed: {e}")
        try:
            self.connection.close()
        except:
            pass
        return self._connect()
```

### 2. Обработка ошибок в каждом методе

Все методы работы с БД теперь:
1. Вызывают `_check_and_recover_connection()` перед выполнением запроса
2. Обрабатывают `psycopg2.InternalError` для обнаружения прерванной транзакции
3. Выполняют `rollback()` при необходимости
4. Возвращают ошибку в виде словаря вместо выбрасывания исключения

Пример для `get_table_data()`:

```python
def get_table_data(self, table_name, filters=None, limit=None, offset=None):
    # Check and recover connection if needed
    if not self._check_and_recover_connection():
        return {'columns': [], 'data': [], 'count': 0, 'error': 'Not connected'}

    try:
        cursor = self.connection.cursor()
        # ... выполнение запроса ...
        cursor.execute(query, params)
        # ...
    except psycopg2.InternalError as e:
        if "current transaction is aborted" in str(e).lower():
            logger.warning("Transaction aborted during query, rolling back...")
            try:
                self.connection.rollback()
            except:
                self._connect()
        return {'columns': [], 'data': [], 'count': 0, 'error': str(e)}
```

### 3. Обновлены HTTP обработчики

Обработчики GET, POST, PUT, DELETE и PATCH теперь проверяют результат на наличие ошибки:

```python
def do_GET(self):
    # ...
    result = self.db_manager.get_table_data(table_name, filters, limit, offset)
    # Check if result contains an error
    if 'error' in result and result.get('columns') == []:
        self._send_json_response({'error': result['error']}, 500)
    else:
        self._send_json_response(result)
```

## Обновлённые методы

- `_check_and_recover_connection()` - новый метод
- `get_table_data()` - добавлена проверка подключения и обработка ошибок
- `insert_record()` - добавлена проверка подключения и обработка ошибок
- `update_record()` - добавлена проверка подключения и обработка ошибок
- `delete_record()` - добавлена проверка подключения и обработка ошибок
- `execute_custom_query()` - добавлена проверка подключения и обработка ошибок
- `get_database_statistics()` - добавлена проверка подключения и обработка ошибок
- `create_backup()` - добавлена проверка подключения
- `do_GET()` - проверка результата на наличие ошибок
- `do_POST()` - проверка результата на наличие ошибок
- `do_PUT()` - проверка результата на наличие ошибок
- `do_DELETE()` - проверка результата на наличие ошибок
- `_handle_custom_query()` - проверка результата на наличие ошибок
- `_handle_statistics()` - проверка результата на наличие ошибок

## Результат

Теперь при выполнении неверного запроса:
1. Ошибка фиксируется в логе
2. Транзакция автоматически откатывается (rollback)
3. Пользователь получает ошибку только для текущего запроса
4. **Последующие запросы выполняются нормально** без ошибки "текущая транзакция прервана"

## Тестирование

Проверить исправление можно следующим образом:

```bash
# 1. Запустить сервер
python server.py

# 2. Выполнить неверный запрос (должен вернуть ошибку)
curl -X PATCH http://localhost:8080/api/custom_query \
  -H "Content-Type: application/json" \
  -d '{"query":"INVALID SQL QUERY"}'

# 3. Выполнить корректный запрос (должен работать без ошибок)
curl http://localhost:8080/api/employees
```

Второй запрос должен успешно вернуть данные, а не ошибку транзакции.
