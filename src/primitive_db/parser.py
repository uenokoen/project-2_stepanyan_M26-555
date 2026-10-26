import re

COMMAND_PATTERNS = {
    "insert": r"insert\s+into\s+(?P<table>\w+)\s+values\s*\((?P<values>.*)\)",
    "select": r"select\s+from\s+(?P<table>\w+)(?:\s+where\s+(?P<where>.+))?",
    "update": r"update\s+(?P<table>\w+)\s+set\s+(?P<set>.+?)\s+where\s+(?P<where>.+)",
    "delete": r"delete\s+from\s+(?P<table>\w+)\s+where\s+(?P<where>.+)",
    "info": r"info\s+(?P<table>\w+)",
}


def split_values(text):
    """Делит строку по запятым, не трогая запятые внутри кавычек."""
    values = []
    current = ""
    quote = None
    for char in text:
        if quote:
            current += char
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
            current += char
        elif char == ",":
            values.append(current.strip())
            current = ""
        else:
            current += char

    if quote:
        raise ValueError(text)
    values.append(current.strip())
    return values


def parse_value(raw):
    """Превращает строку в значение: "текст" -> str, true/false -> bool, 28 -> int."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    try:
        return int(raw)
    except ValueError:
        raise ValueError(raw) from None


def parse_clause(text):
    """Превращает строку вида 'age = 28, name = "Sergei"' в словарь."""
    clause = {}
    for condition in split_values(text):
        column, sep, raw_value = condition.partition("=")
        column = column.strip()
        if not sep or not column.isidentifier():
            raise ValueError(condition)
        clause[column] = parse_value(raw_value)
    return clause


def parse_command(command, user_input):
    """Разбирает команду insert/select/update/delete/info в словарь."""
    match = re.fullmatch(COMMAND_PATTERNS[command], user_input)
    if not match:
        raise ValueError(user_input)

    parts = match.groupdict()
    parsed = {"table": parts["table"]}
    if parts.get("values") is not None:
        parsed["values"] = [parse_value(v) for v in split_values(parts["values"])]
    if parts.get("set"):
        parsed["set"] = parse_clause(parts["set"])
    if parts.get("where"):
        parsed["where"] = parse_clause(parts["where"])
    return parsed
