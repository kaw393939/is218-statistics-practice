"""Supplied application actions; add one action that reads a saved result."""
from abc import ABC, abstractmethod

HELP = ("Commands: add/subtract/multiply/divide A B; square/sqrt VALUE; "
        "power VALUE exponent=N; sum/mean/stddev VALUES (stddev ddof=0/1); "
        "adjust VALUE offset=N scale=N; span VALUES; csv mean/stddev/span PATH; "
        "history; last; clear; help; exit")


def _format_entry(calculation, result) -> str:
    values = " ".join(str(value) for value in calculation.values)
    options = " ".join(f"{key}={value}" for key, value in calculation.options.items())
    request = " ".join(part for part in (calculation.operation.__name__, values, options) if part)
    return f"{request} = {result:.4f}"


class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        """Return display text; expected failures propagate to the CLI."""


class CalculateCommand(Command):
    def __init__(self, session, calculation):
        self.session = session
        self.calculation = calculation

    def execute(self) -> str:
        result = self.session.calculate(self.calculation)
        return f"Result: {result:.4f}"


class HistoryCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        lines = [_format_entry(calculation, result)
                 for calculation, result in self.session.get_history()]
        return "\n".join(lines) or "History is empty."


class LastCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        entries = self.session.get_history()
        if not entries:
            return "History is empty."
        calculation, result = entries[-1]
        return _format_entry(calculation, result)


class ClearHistoryCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        self.session.clear()
        return "History cleared."


class HelpCommand(Command):
    def execute(self) -> str:
        return HELP
