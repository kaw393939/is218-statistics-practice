"""Twenty independent checks worth five points each; the README defines the API."""
import inspect
import os
import math
import subprocess
import sys
from pathlib import Path
import pytest

EXPECTED = 15.811388300841896

# Manual calculation: 20 points.
def test_manual_known_values():
    from calculator.commands import ManualStdDevCommand
    assert ManualStdDevCommand([10, 20, 30, 40, 50]).execute() == pytest.approx(EXPECTED)


def test_manual_constant_values():
    from calculator.commands import ManualStdDevCommand
    assert ManualStdDevCommand([7, 7, 7]).execute() == pytest.approx(0)


def test_manual_numeric_text():
    from calculator.commands import ManualStdDevCommand
    assert ManualStdDevCommand(["10", "20", "30", "40", "50"]).execute() == pytest.approx(EXPECTED)


def test_shared_calculation():
    from calculator.statistics import standard_deviation
    assert standard_deviation([10, 20, 30, 40, 50]) == pytest.approx(EXPECTED)
    assert standard_deviation([2, 4, 6]) == pytest.approx(2.0)

# CSV input: 20 points.
def test_csv_known_values(tmp_path):
    from calculator.commands import CsvStdDevCommand
    path = tmp_path / "data.csv"
    path.write_text("value\n10\n20\n30\n40\n50\n")
    assert CsvStdDevCommand(path).execute() == pytest.approx(EXPECTED)


def test_csv_uses_pandas(monkeypatch, tmp_path):
    import pandas as pd
    from calculator.commands import CsvStdDevCommand
    calls = []
    original = pd.read_csv
    def spy(*args, **kwargs):
        calls.append(args)
        return original(*args, **kwargs)
    monkeypatch.setattr(pd, "read_csv", spy)
    path = tmp_path / "data.csv"
    path.write_text("value\n10\n20\n30\n40\n50\n")
    assert CsvStdDevCommand(path).execute() == pytest.approx(EXPECTED)
    assert calls, "CSV command must use pandas.read_csv"


def test_csv_fixed_default(monkeypatch, tmp_path):
    from calculator.commands import CsvStdDevCommand
    monkeypatch.chdir(tmp_path)
    (tmp_path / "values.csv").write_text("value\n10\n20\n30\n40\n50\n")
    assert CsvStdDevCommand().execute() == pytest.approx(EXPECTED)


def test_csv_missing_column(tmp_path):
    from calculator.commands import CsvStdDevCommand
    path = tmp_path / "data.csv"
    path.write_text("wrong\n10\n20\n")
    with pytest.raises(ValueError):
        CsvStdDevCommand(path).execute()

# Command architecture: 20 points.
def test_abstract_command():
    from calculator.commands import Command
    assert inspect.isabstract(Command)
    with pytest.raises(TypeError):
        Command()


def test_concrete_commands():
    from calculator.commands import Command, ManualStdDevCommand, CsvStdDevCommand
    assert issubclass(ManualStdDevCommand, Command)
    assert issubclass(CsvStdDevCommand, Command)
    assert callable(ManualStdDevCommand([1, 2]).execute)
    assert callable(CsvStdDevCommand().execute)


def test_commands_share_policy(monkeypatch, tmp_path):
    # Contract: commands import the shared function under this documented name.
    import calculator.commands as commands
    calls = []
    def fake(values):
        calls.append(list(values))
        return 42.0
    monkeypatch.setattr(commands, "standard_deviation", fake)
    path = tmp_path / "data.csv"
    path.write_text("value\n1\n2\n")
    assert commands.ManualStdDevCommand([1, 2]).execute() == 42
    assert commands.CsvStdDevCommand(path).execute() == 42
    assert len(calls) == 2


def test_cli_uses_factory_and_execute(monkeypatch, capsys):
    import calculator.cli as cli
    import calculator.factory as factory
    calls = []
    class FakeCommand:
        def execute(self):
            calls.append("execute")
            return 42.0
    def create(name, values=None):
        calls.append(name)
        return FakeCommand()
    monkeypatch.setattr(factory.CommandFactory, "create", staticmethod(create))
    answers = iter(["csv", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    cli.run()
    assert calls == ["csv", "execute"]
    assert "Standard deviation: 42.0000" in capsys.readouterr().out

# Simple Factory: 20 points.
def test_factory_manual():
    from calculator.factory import CommandFactory
    from calculator.commands import ManualStdDevCommand
    command = CommandFactory.create("manual", [10, 20, 30, 40, 50])
    assert isinstance(command, ManualStdDevCommand)
    assert command.execute() == pytest.approx(EXPECTED)


def test_factory_csv_normalization():
    from calculator.factory import CommandFactory
    from calculator.commands import CsvStdDevCommand
    assert isinstance(CommandFactory.create(" CSV "), CsvStdDevCommand)


def test_factory_unknown():
    from calculator.factory import CommandFactory
    with pytest.raises(ValueError):
        CommandFactory.create("unknown")


def test_factory_does_not_execute(monkeypatch):
    from calculator.factory import CommandFactory
    from calculator.commands import ManualStdDevCommand
    def forbidden(self):
        pytest.fail("Factory must construct without executing")
    monkeypatch.setattr(ManualStdDevCommand, "execute", forbidden)
    assert isinstance(CommandFactory.create("manual", [1, 2]), ManualStdDevCommand)
    with pytest.raises(ValueError):
        CommandFactory.create("manual")

# Validation and CLI: 20 points.
def test_invalid_values():
    from calculator.statistics import standard_deviation
    for values in ([], [1], [1, "x"], [1, None], [1, float("nan")], [1, float("inf")]):
        with pytest.raises(ValueError):
            standard_deviation(values)


def test_invalid_csv(tmp_path):
    from calculator.commands import CsvStdDevCommand
    path = tmp_path / "bad.csv"
    for text in ("value\n1\nword\n", "value\n1\n\"\"\n", "value\n1\n"):
        path.write_text(text)
        with pytest.raises(ValueError):
            CsvStdDevCommand(path).execute()
    with pytest.raises(OSError):
        CsvStdDevCommand(tmp_path / "absent.csv").execute()


def test_cli_session(tmp_path):
    import calculator
    (tmp_path / "values.csv").write_text("value\n10\n20\n30\n40\n50\n")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(calculator.__file__).resolve().parents[1])
    result = subprocess.run([sys.executable, "-m", "calculator"], input="manual\n10 20 30 40 50\ncsv\nexit\n", text=True, capture_output=True, timeout=10, cwd=tmp_path, env=env)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("Standard deviation: 15.8114") == 2
    assert "Goodbye!" in result.stdout


def test_cli_recovers_and_eof():
    result = subprocess.run([sys.executable, "-m", "calculator"], input="unknown\nmanual\nnot numbers\nmanual\n10 20 30 40 50\n", text=True, capture_output=True, timeout=10)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("Error:") >= 2
    assert "Standard deviation: 15.8114" in result.stdout
    assert "Goodbye!" in result.stdout
