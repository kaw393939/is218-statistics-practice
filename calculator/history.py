"""Supplied controlled history, extending the prerequisite calculator API."""
from calculator.calculation import Calculation


class History:
    def __init__(self):
        self._entries: list[tuple[Calculation, float]] = []

    def add(self, calculation: Calculation, result: float) -> None:
        self._entries.append((calculation, result))

    def get_history(self) -> list[tuple[Calculation, float]]:
        # A shallow copy protects the collection; entries share their objects.
        return list(self._entries)

    def clear(self) -> None:
        self._entries.clear()
