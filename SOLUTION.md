# Worked practice solution — review after the timed attempt

This branch implements measurement adjustment, span, factory configuration, the last-result action, CSV span, and the history-order repair. It is not an exam solution. Reusing course infrastructure is permitted; the assessment asks for changed behavior and evidence that explains it.

Run `python -m pytest` and `python grading/grade.py`. Automated feedback is out of 60; the published manual rubric requires a separate review of student tests and explanations. The examples below illustrate reasoning, rather than awarding this reference an automatic manual grade.

## Successful flow

For `adjust 3 offset=2 scale=4`, the parser separates the operation name, the text operand `"3"`, and text options `{"offset": "2", "scale": "4"}`. The factory chooses `Operations.adjust`, converts options to finite floats, and constructs `Calculation` with operand tuple `(3.0,)`. No math has run. The prepared `CalculateCommand` holds the session and calculation.

`execute()` calls `session.calculate(calculation)`. `get_result()` unpacks `(3.0,)` and the options into the static operation, which computes `(3.0 + 2.0) * 4.0 = 20.0`. Only after that succeeds does the session record `(calculation, 20.0)`. The command returns `Result: 20.0000`, and the CLI prints it.

`last` creates a different action object. It reads a copied history list, selects its final pair, and formats the saved result. It never calls `get_result()`. It has instance state because it needs this session; the mathematical operation needs only its arguments and is static.

## Failure and recovery

After the adjustment, `span 1` can be constructed: `span` accepts variable operands. On execution, `Operations.span` rejects the single observation with `ValueError`. The exception unwinds through calculation, session, and command to the CLI. Because recording follows successful execution, history still contains only the adjustment. The CLI reports an error and accepts `last`, which displays the saved adjustment.

The repair changes the session's order, not the display command. A failure cannot leave a placeholder entry, and a success records the actual result.

## Why these component choices fit

The factory is a Simple Factory helper configuring the same Calculation product with different callables; it is not formal Factory Method. Commands represent application actions. `*args` allows span to receive variable readings; `**kwargs` carries named settings. The `*` in `adjust(value, *, offset=0, scale=1)` makes the settings keyword-only, preventing ambiguous positional calls.

The span-count check is LBYL: it expresses a cheap, reliable domain requirement. Float conversion uses EAFP: attempt conversion and catch its documented conversion failures. An `if` is not automatically bad, and exception handling is not only a memory cost. Correctness and understandable responsibilities come before speculative performance claims.

The code supplied in the starter is derived from the six-part teaching calculator. These additional adaptation methods and routes implement the published practice contract. The extra tests demonstrate cancellation of calibration settings, snapshot behavior after clear, repeated domain failures, recovery after a nonfinite result, and the difference between displaying a saved result and executing a request again.
