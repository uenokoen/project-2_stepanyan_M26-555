# primitive_db

Учебный проект: консольное приложение, имитирующее работу с базой данных.

## Установка и запуск

Режим разработки:

```bash
uv sync
uv run database
```

Установка как отдельной программы:

```bash
uv build
uv tool install dist/*.whl
database
```

## Управление таблицами

Команды:

- `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...` — создать таблицу. Поддерживаемые типы: `int`, `str`, `bool`. Столбец `ID:int` добавляется автоматически.
- `list_tables` — показать список всех таблиц.
- `drop_table <имя_таблицы>` — удалить таблицу.
- `help` — справочная информация.
- `exit` — выход из программы.

Метаданные таблиц хранятся в файле `db_meta.json`.

Пример:

```
>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool
>>>Введите команду: create_table users name:str
Ошибка: Таблица "users" уже существует.
>>>Введите команду: list_tables
- users
>>>Введите команду: drop_table users
Таблица "users" успешно удалена.
>>>Введите команду: drop_table products
Ошибка: Таблица "products" не существует.
```

## Демонстрация

[![asciicast](https://asciinema.org/a/mZVPdzfXdlUdGByA.svg)](https://asciinema.org/a/mZVPdzfXdlUdGByA)
