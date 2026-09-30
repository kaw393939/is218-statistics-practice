"""Simple Factory: centralize which concrete command to construct."""
from calculator.commands import Command, CsvStdDevCommand, ManualStdDevCommand


class CommandFactory:
    @staticmethod
    def create(name: str, values=None) -> Command:
        name = name.strip().lower()
        if name == "manual":
            if values is None:
                raise ValueError("Manual command requires values.")
            return ManualStdDevCommand(values)
        if name == "csv":
            return CsvStdDevCommand()
        raise ValueError(f"Unknown command: {name}")
