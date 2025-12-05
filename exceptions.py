# exceptions.py

class ConversionError(Exception):
    """Общая ошибка при конвертации единиц."""
    pass


class UnknownUnitError(ConversionError):
    """Единица измерения не найдена в словаре."""
    pass
