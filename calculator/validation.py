"""The finite-number input policy shared by calculations and statistics."""
from math import isfinite


def numeric_values(values) -> tuple[float, ...]:
    numbers = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError("Values must be numeric.") from error
        if not isfinite(number):
            raise ValueError("Values must be finite numbers.")
        numbers.append(number)
    return tuple(numbers)
