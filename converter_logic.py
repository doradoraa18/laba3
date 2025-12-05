# converter_logic.py

from exceptions import ConversionError, UnknownUnitError

# сколько байт в 1 единице (строго по 1024, как в информатике)
UNIT_FACTORS = {
    "бит": 1 / 8,                 # 1 байт = 8 бит
    "байт": 1,
    "килобайт (КБ)": 1024,
    "мегабайт (МБ)": 1024 ** 2,
    "гигабайт (ГБ)": 1024 ** 3,
    "терабайт (ТБ)": 1024 ** 4,
    "петабайт (ПБ)": 1024 ** 5,
    "эксабайт (ЭБ)": 1024 ** 6,
    "зеттабайт (ЗБ)": 1024 ** 7,
    "йоттабайт (ЙБ)": 1024 ** 8,
}


def format_number(x: float) -> str:
    """Форматирование без экспоненты: до 6 знаков после запятой, пробелы между тысячами."""
    s = f"{x:,.6f}"
    s = s.rstrip("0").rstrip(",")
    return s.replace(",", " ")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Перевод value из from_unit в to_unit через байты."""
    if from_unit not in UNIT_FACTORS or to_unit not in UNIT_FACTORS:
        raise UnknownUnitError("Неизвестная единица измерения")

    try:
        bytes_value = value * UNIT_FACTORS[from_unit]
        result = bytes_value / UNIT_FACTORS[to_unit]
    except Exception as e:
        raise ConversionError(f"Ошибка при вычислении: {e}") from e

    return result
