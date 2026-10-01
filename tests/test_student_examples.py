"""After-attempt examples: extra cases and the regressions they distinguish."""
import pytest
from calculator.calculation import Calculation
from calculator.commands import LastCommand
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def test_adjust_offset_and_scale_can_cancel():
    # Add-then-scale returns the original reading; scale-then-add would return 9.
    assert CalculationFactory.create('adjust', 8, offset=-4, scale=2).get_result() == 8


def test_clear_leaves_previously_returned_snapshot_readable():
    session = CalculatorSession()
    calculation = CalculationFactory.create('adjust', 2, scale=.5)
    session.calculate(calculation)
    snapshot = session.get_history()
    session.clear()
    assert session.get_history() == []
    assert snapshot == [(calculation, 1.0)]


def test_failed_span_preserves_last_across_multiple_failures():
    session = CalculatorSession()
    session.calculate(CalculationFactory.create('adjust', -2, offset=1, scale=3))
    expected = LastCommand(session).execute()
    for values in ((), (2,)):
        with pytest.raises(ValueError):
            session.calculate(CalculationFactory.create('span', *values))
    assert LastCommand(session).execute() == expected
    assert len(session.get_history()) == 1


def test_nonfinite_result_does_not_prevent_a_later_success():
    session = CalculatorSession()
    with pytest.raises(ValueError):
        session.calculate(CalculationFactory.create('adjust', 1e308, scale=1e308))
    assert session.calculate(CalculationFactory.create('span', -1, 2)) == 3
    assert len(session.get_history()) == 1


def test_reexecuting_a_request_is_distinct_from_reading_its_last_result():
    session = CalculatorSession()
    request = CalculationFactory.create('span', 5, 9)
    session.calculate(request)
    LastCommand(session).execute()
    assert len(session.get_history()) == 1
    session.calculate(request)
    assert len(session.get_history()) == 2
