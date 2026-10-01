"""Supplied construction logic; extend its registries for adjust and span."""
from calculator.calculation import Calculation
from calculator.operations import Operations
from calculator.validation import numeric_values


class CalculationFactory:
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
        "square": Operations.square,
        "sqrt": Operations.sqrt,
        "power": Operations.power,
        "sum": Operations.sum,
        "mean": Operations.mean,
        "stddev": Operations.stddev,
        "adjust": Operations.adjust,
        "span": Operations.span,
    }
    operand_counts = {"add": 2, "subtract": 2, "multiply": 2, "divide": 2,
                      "square": 1, "sqrt": 1, "power": 1, "adjust": 1}
    allowed_options = {"power": {"exponent"}, "stddev": {"ddof"},
                       "adjust": {"offset", "scale"}}

    @staticmethod
    def create(name: str, *values, **options) -> Calculation:
        name = name.strip().lower()
        try:
            operation = CalculationFactory.operations[name]
        except KeyError:
            raise ValueError(f"Unknown operation: {name}") from None

        allowed = CalculationFactory.allowed_options.get(name, set())
        converted_options = {}
        for key, value in options.items():
            if key not in allowed:
                raise ValueError(f"Unsupported option for {name}: {key}")
            converted_options[key] = numeric_values([value])[0]

        count = CalculationFactory.operand_counts.get(name)
        if count is not None and len(values) != count:
            raise ValueError(f"{name} requires exactly {count} value(s).")
        return Calculation(values, operation, **converted_options)
