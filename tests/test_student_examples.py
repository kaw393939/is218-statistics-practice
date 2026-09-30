import pytest
from calculator.statistics import standard_deviation


def test_known_sample():
    assert standard_deviation([10, 20, 30, 40, 50]) == pytest.approx(15.811388300841896)


def test_constant_values():
    assert standard_deviation([7, 7, 7]) == 0


@pytest.mark.parametrize("values", [[], [1], [1, "x"], [1, None], [1, float("inf")], [1, float("nan")]])
def test_reject_invalid_values(values):
    with pytest.raises(ValueError):
        standard_deviation(values)
