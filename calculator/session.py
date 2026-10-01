"""Receiver records only completed calculations and exposes controlled history."""
from calculator.history import History


class CalculatorSession:
    def __init__(self):
        self._history = History()

    def calculate(self, calculation) -> float:
        result = calculation.get_result()
        self._history.add(calculation, result)
        return result

    def get_history(self):
        return self._history.get_history()

    def clear(self) -> None:
        self._history.clear()
