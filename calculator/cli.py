"""Supplied parser and loop; extend only the last-action and CSV routes."""
import pandas as pd
from calculator.commands import (CalculateCommand, ClearHistoryCommand, HelpCommand,
                                 HistoryCommand, LastCommand)
from calculator.factory import CalculationFactory
from calculator.inputs import read_csv_values
from calculator.session import CalculatorSession


def prepare_command(text, session):
    parts = text.split()
    if not parts:
        raise ValueError("Enter a command; use help for examples.")
    name, *arguments = parts
    name = name.lower()
    actions = {"history": HistoryCommand, "clear": ClearHistoryCommand, "last": LastCommand}
    if name in actions:
        if arguments:
            raise ValueError(f"{name} does not accept values.")
        return actions[name](session)
    if name == "help":
        if arguments:
            raise ValueError("help does not accept values.")
        return HelpCommand()
    values = []
    options = {}
    for argument in arguments:
        if "=" in argument:
            key, value = argument.split("=", 1)
            if not key or key in options:
                raise ValueError("Options need unique names: key=value.")
            options[key] = value
        else:
            values.append(argument)
    if name == "csv":
        if len(values) != 2:
            raise ValueError("Use: csv mean/stddev/span PATH (a path without spaces).")
        operation, path = values
        if operation.lower() not in {"mean", "stddev", "span"}:
            raise ValueError("CSV supports mean, stddev, or span.")
        values = read_csv_values(path)
        name = operation
    calculation = CalculationFactory.create(name, *values, **options)
    return CalculateCommand(session, calculation)


def run() -> None:
    session = CalculatorSession()
    print("Measurement calculator")
    print(HelpCommand().execute())
    while True:
        try:
            text = input("> ").strip()
            if text.lower() == "exit":
                break
            command = prepare_command(text, session)
            print(command.execute())
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except (ValueError, OSError, ZeroDivisionError, OverflowError,
                pd.errors.ParserError, pd.errors.EmptyDataError) as error:
            print(f"Error: {error}")
    print("Goodbye!")
