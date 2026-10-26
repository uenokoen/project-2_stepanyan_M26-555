VALID_TYPES = {"int", "str", "bool"}


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
    columns_text = ", ".join(f"{name}:{type_}" for name, type_ in table_columns.items())
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