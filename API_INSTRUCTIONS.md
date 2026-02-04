# Инструкция по работе с API RWSDBv2.1

## 1. Просмотр таблиц
```
http://localhost:8080/api/train
```

## 2. Фильтрация содержимого таблиц
```
http://localhost:8080/api/train?train_id=1
```
или
```
http://localhost:8080/api/train?type=Пассажирский
```

## 3. Добавление записей в таблицы
Для этого потребуется использовать инструменты разработчика в браузере (F12) или расширение для API-запросов:
- Открыть вкладку Network (Сеть)
- Перейти на вкладку Console (Консоль)
- Выполнить:
```javascript
fetch('http://localhost:8080/api/train', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({"type": "Грузовой", "carriage_count": 20})
})
.then(response => response.json())
.then(data => console.log(data));
```

## 4. Обновление записей в таблицах
В консоли браузера выполнить:
```javascript
fetch('http://localhost:8080/api/train/1', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({"type": "Скоростной", "carriage_count": 15})
})
.then(response => response.json())
.then(data => console.log(data));
```

## 5. Удаление записей из таблиц
В консоли браузера выполнить:
```javascript
fetch('http://localhost:8080/api/train/1', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

## 6. Выполнение специальных запросов
В консоли браузера выполнить:
```javascript
fetch('http://localhost:8080/api/custom_query', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({"query": "SELECT * FROM train WHERE type = 'Пассажирский'"})
})
.then(response => response.json())
.then(data => console.log(data));
```

## 7. Создание бэкапов базы данных
В консоли браузера выполнить:
```javascript
fetch('http://localhost:8080/api/backup', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer 4444'
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

## 8. Сохранение результатов запросов в файл
В консоли браузера выполнить:

- Экспорт всей таблицы в JSON:
```javascript
fetch('http://localhost:8080/api/export', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({"table": "train", "format": "json"})
})
.then(response => response.json())
.then(data => console.log(data));
```

- Экспорт всей таблицы в CSV (браузер автоматически начнет скачивание):
```javascript
fetch('http://localhost:8080/api/export', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({"table": "train", "format": "csv"})
})
.then(response => {
  response.blob().then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'export.csv';
    a.click();
  });
});
```

- Экспорт результата запроса в Excel:
```javascript
fetch('http://localhost:8080/api/export', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({"query": "SELECT * FROM train WHERE type = 'Пассажирский'", "format": "excel"})
})
.then(response => {
  response.blob().then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'export.xlsx';
    a.click();
  });
});
```

## Альтернативный способ:
Можно использовать расширения для браузера, такие как:
- Postman Interceptor
- RESTClient
- или встроенные инструменты разработчика в Firefox/Chrome

Для GET-запросов (просмотр таблиц и фильтрация) достаточно просто ввести URL в адресную строку браузера.