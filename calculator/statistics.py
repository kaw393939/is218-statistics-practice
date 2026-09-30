"""One shared calculation policy, independent of terminal and file input."""
from math import isfinite
import pandas as pd


def standard_deviation(values) -> float:
    """Return sample standard deviation; require two or more finite numbers."""
    try:
        numbers = pd.to_numeric(pd.Series(list(values), dtype="object"), errors="raise")
    except (TypeError, ValueError) as error:
        raise ValueError("Values must be numeric.") from error
    if len(numbers) < 2:
        raise ValueError("Enter at least two values.")
    if not all(isfinite(float(value)) for value in numbers):
        raise ValueError("Values must be finite numbers.")
    # ddof=1 divides by n-1: this is the sample statistic.
    result = float(numbers.astype(float).std(ddof=1))
    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result
