import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    check_clause,
    create_table,
    delete,
    drop_table,
    format_columns,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.parser import parse_command
from primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

META_FILE = "db_meta.json"
DATA_COMMANDS = {"insert", "select", "update", "delete", "info"}


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def print_records(columns, records):
    """Выводит записи таблицей с помощью PrettyTable."""
    if not records:
        print("Записи не найдены.")
        return

    table = PrettyTable()
    table.field_names = list(columns)
    for record in records:
        table.add_row([record[column] for column in columns])
    print(table)


def handle_data_command(metadata, command, user_input):
    """Выполняет команды insert/select/update/delete/info."""
    try:
        parsed = parse_command(command, user_input)
    except ValueError as error:
        print(f"Некорректное значение: {error}. Попробуйте снова.")
        return

    table_name = parsed["table"]
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]
    where_clause = parsed.get("where")
    set_clause = parsed.get("set")
    if where_clause and not check_clause(columns, where_clause):
        return
    if set_clause:
        if "ID" in set_clause:
            print("Некорректное значение: ID нельзя изменить. Попробуйте снова.")
            return
        if not check_clause(columns, set_clause):
            return

    table_data = load_table_data(table_name)
    match command:
        case "insert":
            table_data = insert(metadata, table_name, parsed["values"], table_data)
            save_table_data(table_name, table_data)
        case "select":
            print_records(columns, select(table_data, where_clause))
        case "update":
            found_ids = [row["ID"] for row in select(table_data, where_clause)]
            if not found_ids:
                print("Записи не найдены.")
                return
            table_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, table_data)
            for record_id in found_ids:
                print(
                    f'Запись с ID={record_id} в таблице "{table_name}" '
                    "успешно обновлена."
                )
        case "delete":
            found_ids = [row["ID"] for row in select(table_data, where_clause)]
            if not found_ids:
                print("Записи не найдены.")
                return
            table_data = delete(table_data, where_clause)
            save_table_data(table_name, table_data)
            for record_id in found_ids:
                print(
                    f'Запись с ID={record_id} успешно удалена '
                    f'из таблицы "{table_name}".'
                )
        case "info":
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {format_columns(columns)}")
            print(f"Количество записей: {len(table_data)}")


def run():
    """Главный цикл программы: читает команды и выполняет их."""
    print("***База данных***")
    print_help()

    while True:
        metadata = load_metadata(META_FILE)
        try:
            user_input = prompt.string(">>>Введите команду: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        try:
            args = shlex.split(user_input)
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue

        if not args:
            continue

        command = args[0]
        match command:
            case "create_table":
                if len(args) < 2:
                    print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                    continue
                metadata = create_table(metadata, args[1], args[2:])
                save_metadata(META_FILE, metadata)
            case "drop_table":
                if len(args) != 2:
                    print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                    continue
                if args[1] in metadata:
                    delete_table_data(args[1])
                metadata = drop_table(metadata, args[1])
                save_metadata(META_FILE, metadata)
            case "list_tables":
                list_tables(metadata)
            case _ if command in DATA_COMMANDS:
                handle_data_command(metadata, command, user_input)
            case "help":
                print_help()
            case "exit":
                break
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")
