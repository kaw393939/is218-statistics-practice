"""The invoker collects text, creates a request, and executes it."""
import pandas as pd
from calculator.factory import CommandFactory


def run() -> None:
    print("Statistics Calculator\nCommands: manual, csv, exit")
    while True:
        try:
            name = input("> ").strip().lower()
            if name == "exit":
                break
            values = None
            if name == "manual":
                values = input("Enter values separated by spaces: ").split()
            command = CommandFactory.create(name, values)
            result = command.execute()
            print(f"Standard deviation: {result:.4f}")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except (ValueError, OSError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
            print(f"Error: {error}")
    print("Goodbye!")
