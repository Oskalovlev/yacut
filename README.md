# YaCut

### Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Технологии:

* Python - 3.10
* Flask - 2.0.2
* SQLAlchemy - 1.4.29
##### P.S. Остальной стек в requirements.txt

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Oskalovlev/yacut.git 
```

```
cd yacut
```

### Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

### Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

# Создать env.:

```
touch .env
```

### Заполните .env:
```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=SECRET
```
##### PS Для работы в дебаг режиме необходимо указать ```FLASK_DEBUG=True```

### Выполнить миграции и запустить проект:

```
flask db upgrade
```
```
flask run
```

### Автор 
#### Оскалов Лев
