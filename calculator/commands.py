"""Command objects package requests behind one execute() contract."""
from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from calculator.statistics import standard_deviation


class Command(ABC):
    @abstractmethod
    def execute(self) -> float:
        """Return a numeric result or raise a useful input/file error."""


class ManualStdDevCommand(Command):
    def __init__(self, values):
        # Snapshot inputs so the request owns its values.
        self.values = list(values)

    def execute(self) -> float:
        return standard_deviation(self.values)


class CsvStdDevCommand(Command):
    def __init__(self, path="values.csv"):
        self.path = Path(path)

    def execute(self) -> float:
        frame = pd.read_csv(self.path)
        if "value" not in frame.columns:
            raise ValueError("CSV must contain a column named value.")
        # Do not silently drop missing values: both sources follow the same policy.
        return standard_deviation(frame["value"])
