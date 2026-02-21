import unittest
from calculator import (
    add,
    subtract,
    multiply,
    divide,
    DivisionByZeroError,
)


class CalculatorAddTests(unittest.TestCase):
    """Тесты сложения."""

    def test_add(self):
        """Сложение двух положительных чисел."""
        self.assertEqual(add(5, 3), 8)
        self.assertEqual(add(10, 20), 30)

    def test_add_with_negative_numbers(self):
        """Сложение с отрицательными числами."""
        self.assertEqual(add(-5, 3), -2)
        self.assertEqual(add(-10, -20), -30)


class CalculatorSubtractTests(unittest.TestCase):
    """Тесты вычитания."""

    def test_subtract(self):
        """Вычитание двух чисел."""
        self.assertEqual(subtract(10, 3), 7)
        self.assertEqual(subtract(5, 10), -5)


class CalculatorMultiplyTests(unittest.TestCase):
    """Тесты умножения."""

    def test_multiply(self):
        """Умножение двух чисел."""
        self.assertEqual(multiply(4, 5), 20)
        self.assertEqual(multiply(-3, 4), -12)

    def test_multiply_by_zero(self):
        """Умножение на ноль всегда даёт ноль."""
        self.assertEqual(multiply(5, 0), 0)
        self.assertEqual(multiply(0, 100), 0)


class CalculatorDivideTests(unittest.TestCase):
    """Тесты деления."""

    def test_divide(self):
        """Деление двух чисел."""
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(divide(15, 3), 5.0)

    def test_divide_by_zero_raises_error(self):
        """Деление на ноль вызывает DivisionByZeroError."""
        with self.assertRaises(DivisionByZeroError):
            divide(10, 0)
        with self.assertRaises(DivisionByZeroError):
            divide(-5, 0)

    def test_divide_zero_by_number(self):
        """Деление нуля на число даёт ноль."""
        self.assertEqual(divide(0, 5), 0.0)
        self.assertEqual(divide(0, -10), -0.0)


if __name__ == '__main__':
    unittest.main()
