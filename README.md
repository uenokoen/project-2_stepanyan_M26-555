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

### Демонстрация

[![asciicast](https://asciinema.org/a/mZVPdzfXdlUdGByA.svg)](https://asciinema.org/a/mZVPdzfXdlUdGByA)

## CRUD-операции

Записи каждой таблицы хранятся в отдельном файле `data/<имя_таблицы>.json`.

Команды:

- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — создать запись. `ID` генерируется автоматически, его указывать не нужно. Все поля обязательны.
- `select from <имя_таблицы>` — прочитать все записи.
- `select from <имя_таблицы> where <столбец> = <значение>` — прочитать записи по условию.
- `update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия>` — обновить запись.
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить запись.
- `info <имя_таблицы>` — вывести информацию о таблице.

Как записывать значения:

- строки — всегда в кавычках: `"Sergei"`;
- числа — без кавычек: `28`;
- логические значения — `true` или `false`.

Пример:

```
>>>Введите команду: insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".
>>>Введите команду: select from users where age = 28
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei |  28 |    True   |
+----+--------+-----+-----------+
>>>Введите команду: update users set age = 29 where name = "Sergei"
Запись с ID=1 в таблице "users" успешно обновлена.
>>>Введите команду: delete from users where ID = 1
Запись с ID=1 успешно удалена из таблицы "users".
>>>Введите команду: info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0
```

### Демонстрация

[![asciicast](https://asciinema.org/a/acfcvQfhU8SBmP1d.svg)](https://asciinema.org/a/acfcvQfhU8SBmP1d)
