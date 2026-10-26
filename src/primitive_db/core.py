VALID_TYPES = {"int", "str", "bool"}
TYPES = {"int": int, "str": str, "bool": bool}


def format_columns(columns):
    """Возвращает столбцы в виде строки 'ID:int, name:str'."""
    return ", ".join(f"{name}:{type_}" for name, type_ in columns.items())


def create_table(metadata, table_name, columns):
    """Создаёт таблицу с указанными столбцами и столбцом ID:int в начале."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = {"ID": "int"}
    for column in columns:
        name, _, column_type = column.partition(":")
        if name == "ID" and column_type == "int":
            continue
        if not name or column_type not in VALID_TYPES or name in table_columns:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
        table_columns[name] = column_type

    metadata[table_name] = table_columns
    columns_text = format_columns(table_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_text}')
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata):
    """Печатает список всех таблиц."""
    if not metadata:
        print("Таблиц пока нет.")
        return

    for table_name in metadata:
        print(f"- {table_name}")


def is_valid_type(value, column_type):
    """Проверяет, что значение подходит под тип столбца."""
    # type() вместо isinstance(): иначе True прошло бы как int
    return type(value) is TYPES[column_type]


def check_clause(columns, clause):
    """Проверяет, что столбцы из условия есть в таблице и типы значений верные."""
    for column, value in clause.items():
        if column not in columns or not is_valid_type(value, columns[column]):
            print(f"Некорректное значение: {column} = {value}. Попробуйте снова.")
            return False
    return True


def matches(row, where_clause):
    """Проверяет, подходит ли запись под условие."""
    return all(row.get(column) == value for column, value in where_clause.items())


def insert(metadata, table_name, values, table_data):
    """Добавляет запись в таблицу. ID генерируется автоматически."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = list(metadata[table_name].items())[1:]
    if len(values) != len(columns):
        print(
            f"Некорректное значение: ожидается {len(columns)} значений, "
            f"получено {len(values)}. Попробуйте снова."
        )
        return table_data

    record = {"ID": max((row["ID"] for row in table_data), default=0) + 1}
    for (column, column_type), value in zip(columns, values):
        if not is_valid_type(value, column_type):
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return table_data
        record[column] = value

    table_data.append(record)
    print(f'Запись с ID={record["ID"]} успешно добавлена в таблицу "{table_name}".')
    return table_data


def select(table_data, where_clause=None):
    """Возвращает все записи или только подходящие под условие."""
    if not where_clause:
        return table_data
    return [row for row in table_data if matches(row, where_clause)]


def update(table_data, set_clause, where_clause):
    """Обновляет поля в записях, подходящих под условие."""
    for row in select(table_data, where_clause):
        row.update(set_clause)
    return table_data


def delete(table_data, where_clause):
    """Удаляет записи, подходящие под условие."""
    return [row for row in table_data if not matches(row, where_clause)]
