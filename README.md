О проекте
```
Проект YaCut предназначен для создания укороченных ссылок,
которыми удобно делиться. Сервис предоставляет два интерфейса
для работы:
* UI, доступный по адресу http://127.0.0.1:5000/
* API для возможности интеграции с другими приложениями
```

Эндпоинты API
```
* POST http://127.0.0.1:5000/api/id/
  тело запроса:
  {
    "url": "string",
    "custom_id": "string"
  }
  url - обязательный параметр. Ссылка, которуб нужно укоротить
  custom_id - необязательный параметр. Если не указать, сервис
              самостоятельно сформирует короткую ссылку.
              
  Тело ответа:
  {
    "url": "string",
    "short_link": "string"
  }
              
* GET http://127.0.0.1:5000/api/id/{short_id}
  short_id - уникальный идентификатор короткой ссылки
  
  Тело ответа:
  {
    "url": "string"
  }
```


**Как развернуть**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Применить миграции:

```
flask db upgrade
```

Запустить проект на локальном сервере:

```
flask run
```

**Автор:** [Алексей Данилов](https://github.com/AlexeyDanilov/)

Проект доступен [по ссылке](https://github.com/AlexeyDanilov/yacut)
