"""Twelve published adaptation checks, five automated points each."""
import inspect
import pytest

from calculator.calculation import Calculation
from calculator.cli import prepare_command, run
from calculator.commands import Command, HistoryCommand
from calculator.factory import CalculationFactory
from calculator.history import History
from calculator.operations import Operations
from calculator.session import CalculatorSession


def test_adjust_static_keyword_configuration():
    assert isinstance(inspect.getattr_static(Operations, 'adjust'), staticmethod)
    assert Operations.adjust(7) == 7
    assert Operations.adjust(3, offset=2, scale=4) == 20
    assert Operations.adjust(-3, offset=1, scale=-2) == 4
    assert Operations.adjust(100, scale=0) == 0
    with pytest.raises(TypeError):
        Operations.adjust(3, 2, 4)


def test_span_static_variable_inputs():
    assert isinstance(inspect.getattr_static(Operations, 'span'), staticmethod)
    assert Operations.span(-4, 3, 8) == 12
    assert Operations.span(2, 2) == 0
    assert Operations.span(-3.5, -1.25, -2) == pytest.approx(2.25)
    for values in ((), (9,)):
        with pytest.raises(ValueError):
            Operations.span(*values)


def test_factory_constructs_adjust():
    calculation = CalculationFactory.create(' ADJUST ', '3', offset='2', scale='4')
    assert isinstance(calculation, Calculation)
    assert calculation.operation is Operations.adjust
    assert calculation.values == (3.0,)
    assert calculation.options == {'offset': 2.0, 'scale': 4.0}
    assert calculation.get_result() == 20
    assert CalculationFactory.create('adjust', 7).get_result() == 7
    for values in ((), (1, 2)):
        with pytest.raises(ValueError):
            CalculationFactory.create('adjust', *values)


def test_factory_constructs_span_without_execution(monkeypatch):
    calls = []
    def measured_span(*values):
        calls.append(values)
        return Operations.span(*values)
    # Registered callables must be selected at construction, not executed there.
    assert CalculationFactory.operations['span'] is Operations.span
    monkeypatch.setitem(CalculationFactory.operations, 'span', measured_span)
    calculation = CalculationFactory.create('SPAN', '-4', '3', '8')
    assert calls == []
    assert calculation.values == (-4.0, 3.0, 8.0)
    assert calculation.get_result() == 12
    assert calls == [(-4.0, 3.0, 8.0)]
    short = CalculationFactory.create('span', 1)
    assert len(calls) == 1
    with pytest.raises(ValueError):
        short.get_result()
    assert CalculationFactory.create('divide', 1, 0).values == (1.0, 0.0)


def test_factory_rejects_bad_options():
    # Successful defaults prevent "reject every new operation" from passing.
    assert CalculationFactory.create('adjust', 2, offset=1).get_result() == 3
    for options in ({'exponent': 2}, {'offset': 'bad'}, {'scale': float('inf')},
                    {'scale': float('nan')}, {'offset': None}):
        with pytest.raises(ValueError):
            CalculationFactory.create('adjust', 2, **options)
    with pytest.raises(ValueError):
        CalculationFactory.create('span', 1, 3, scale=2)
    with pytest.raises(ValueError):
        CalculationFactory.create('adjust', 'bad')
    assert CalculationFactory.create('power', 2, exponent=3).get_result() == 8


def test_last_command_contract_and_empty():
    from calculator.commands import LastCommand
    command = LastCommand(CalculatorSession())
    assert isinstance(command, Command)
    assert command.execute() == 'History is empty.'
    with pytest.raises(TypeError):
        Command()
    class IncompleteCommand(Command):
        pass
    with pytest.raises(TypeError):
        IncompleteCommand()


def test_last_displays_saved_request():
    from calculator.commands import LastCommand
    session = CalculatorSession()
    first = CalculationFactory.create('adjust', 3, offset=2, scale=4)
    assert session.calculate(first) == 20
    output = LastCommand(session).execute()
    for text in ('adjust', '3.0', 'offset=2.0', 'scale=4.0', '= 20.0000'):
        assert text in output
    session.calculate(CalculationFactory.create('span', -4, 3, 8))
    output = LastCommand(session).execute()
    assert output == HistoryCommand(session).execute().splitlines()[-1]
    assert output == 'span -4.0 3.0 8.0 = 12.0000'


def test_last_never_reexecutes():
    from calculator.commands import LastCommand
    calls = []
    def changing_reading(value):
        calls.append(value)
        return value + len(calls)
    session = CalculatorSession()
    calculation = Calculation([10], changing_reading)
    assert session.calculate(calculation) == 11
    for _ in range(3):
        assert LastCommand(session).execute() == 'changing_reading 10.0 = 11.0000'
    assert calls == [10.0]
    assert len(session.get_history()) == 1


def test_history_exposes_safe_snapshot():
    calculation = Calculation([2, 3], Operations.add)
    history = History()
    history.add(calculation, 5.0)
    saved = history.get_history()
    assert saved == [(calculation, 5.0)]
    assert saved is not history.get_history()
    saved.clear()
    assert history.get_history() == [(calculation, 5.0)]
    session, other = CalculatorSession(), CalculatorSession()
    assert not hasattr(session, 'history')
    session.calculate(calculation)
    snapshot = session.get_history()
    snapshot.clear()
    assert len(session.get_history()) == 1
    assert other.get_history() == []
    session.clear()
    assert session.get_history() == []
    assert history.get_history() == [(calculation, 5.0)]


def test_session_records_only_success():
    calls = []
    def successful(value):
        calls.append(('success', value))
        return value + 7
    def failed(value):
        calls.append(('failed', value))
        raise ValueError('Bad reading.')
    session = CalculatorSession()
    calculation = Calculation([3], successful)
    assert session.calculate(calculation) == 10
    assert session.get_history() == [(calculation, 10.0)]
    before = session.get_history()
    with pytest.raises(ValueError):
        session.calculate(Calculation([5], failed))
    assert session.get_history() == before
    assert calls == [('success', 3.0), ('failed', 5.0)]
    with pytest.raises(ValueError):
        session.calculate(Calculation([1], lambda value: float('inf')))
    assert session.get_history() == before


def test_cli_adaptations_and_recovery(monkeypatch, capsys):
    from calculator.commands import LastCommand
    session = CalculatorSession()
    assert isinstance(prepare_command('last', session), LastCommand)
    with pytest.raises(ValueError):
        prepare_command('last 1', session)
    answers = iter(['adjust 3 offset=2 scale=4', 'span -4 3 8', 'last',
                    'span 1', 'adjust', 'adjust 1 unknown=2',
                    'adjust 1 offset=2 offset=3', 'adjust 1 scale=oops',
                    'last', 'clear', 'last', 'square 3', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert output.count('Error:') == 5
    for text in ('Result: 20.0000', 'Result: 12.0000', 'Result: 9.0000',
                 'History cleared.', 'History is empty.', 'Goodbye!'):
        assert text in output
    assert output.count('span -4.0 3.0 8.0 = 12.0000') == 2


def test_csv_span_reuses_calculation_flow(monkeypatch, tmp_path, capsys):
    from calculator.commands import LastCommand
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'readings.csv').write_text('value\n9\n-2\n4\n')
    (tmp_path / 'missing.csv').write_text('value\n9\n""\n4\n')
    (tmp_path / 'single.csv').write_text('value\n9\n')
    calls = []
    original = CalculationFactory.create
    def create(name, *values, **options):
        calls.append((name, values, options))
        return original(name, *values, **options)
    monkeypatch.setattr(CalculationFactory, 'create', create)
    session = CalculatorSession()
    command = prepare_command('csv span readings.csv', session)
    assert session.get_history() == []
    assert calls[-1] == ('span', (9, -2, 4), {})
    assert command.execute() == 'Result: 11.0000'
    assert LastCommand(session).execute() == 'span 9.0 -2.0 4.0 = 11.0000'
    with pytest.raises(ValueError):
        prepare_command('csv adjust readings.csv', session)
    answers = iter(['csv span missing.csv', 'csv span single.csv',
                    'csv span absent.csv', 'csv span readings.csv', 'last', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert output.count('Error:') == 3
    assert 'Result: 11.0000' in output
    assert 'span 9.0 -2.0 4.0 = 11.0000' in output
