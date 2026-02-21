class DivisionByZeroError(Exception):
    """Исключение при делении на ноль."""
    pass


def add(a: float, b: float) -> float:
    """Сложение двух чисел."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Вычитание: a - b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Умножение двух чисел."""
    return a * b


def divide(a: float, b: float) -> float:
    """
    Деление: a / b.
    Вызывает DivisionByZeroError при b == 0.
    """
    if b == 0:
        raise DivisionByZeroError("Деление на ноль невозможно")
    return a / b
