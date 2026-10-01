# Practice: adapt a measurement-calibration calculator

This is a **90-minute, open-notes and open-code practice assessment** following the six-part [teaching course](https://github.com/kaw393939/is218-command-factory-statistics). You already built an OOP calculator. Here you receive working infrastructure and adapt it to new requirements; rebuilding the textbook application is not the task.

A laboratory needs to adjust a reading using named calibration settings, calculate the spread of several readings, and recall its last successful calculation. A known history defect must also be repaired. The formulas are supplied; no laboratory or statistical knowledge is assumed.

## Before the timer

Read this page and verify your Python/GitHub environment. Use Python 3.11–3.14. Fork this repository and clone your fork. Environment installation is preparation rather than assessed work.

```bash
git clone https://github.com/YOUR-USERNAME/is218-statistics-practice.git
cd is218-statistics-practice
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
python grading/grade.py
```

Windows PowerShell: `py -m venv .venv`, then `.venv\Scripts\Activate.ps1`. If activation is restricted, use `.venv\Scripts\python.exe` or `.venv/bin/python` directly. Do not commit `.venv`.

The untouched starter scores **5/60** for supplied controlled-history infrastructure; its eleven failed adaptation checks are expected. `NotImplementedError` marks unfinished work. `python -m calculator` runs the supplied loop, though new requests will not work until you implement them. The supplied grader reports only the automated **60-point** portion of the assessment.

## What is supplied and what you change

Supplied and working: arithmetic/unary/statistical operations, numeric conversion, `Calculation`, factory selection logic, `History`, the command base class, calculate/history/clear/help commands, CSV reading, parser and interactive loop, pytest setup, and feedback infrastructure.

Your changes are limited to these adaptations:

1. Implement static `Operations.adjust` and `Operations.span`.
2. Extend the factory registries for their operand and option policies.
3. Implement `LastCommand.execute()` using saved history.
4. Connect `last` and `csv span PATH` through the supplied parser.
5. Repair the clearly marked ordering bug in `CalculatorSession.calculate`.
6. Add your own tests and a short request trace/design explanation.

There is no requirement to implement an additional design pattern, rebuild parsing, add persistent storage, or change statistical policy. You may refactor within `calculator/` if the published contracts continue to work. Keep the supplied acceptance tests, rubric, grader, and workflow unchanged.

## New required behavior

| Request/API | Contract |
| --- | --- |
| `adjust VALUE [offset=N] [scale=N]` | Exactly one value. Compute `(value + offset) * scale`; defaults: `offset=0`, `scale=1`. Order matters: add before multiplying. |
| `Operations.adjust(value, *, offset=0, scale=1)` | Static method. Both settings are keyword-only. Negative and zero offsets/scales are valid. |
| `span VALUES` / `Operations.span(*values)` | Static method accepting two or more readings. Return `max(values) - min(values)`; duplicates and negative numbers are valid. Reject fewer than two values with `ValueError`. |
| `CalculationFactory.create("adjust", *values, **options)` | Select `Operations.adjust`, enforce exactly one operand, permit only `offset` and `scale`, convert supplied numeric options to finite floats. Return an unexecuted `Calculation`. |
| `CalculationFactory.create("span", *values, **options)` | Select `Operations.span`, accept variable operands, reject all named options. The operation checks its minimum observation count when executed. |
| `last` / `LastCommand(session).execute()` | Return the most recent saved successful request and result, in the same format as the final line of `history`. Return `History is empty.` when there are no entries. Never execute a calculation again. |
| `csv span PATH` | Read the supplied `value` column and use the same factory/calculation/span operation as typed values. |
| `CalculatorSession.calculate(calculation)` | Execute once; only after success, record `(calculation, actual_result)` and return that result. A failed calculation adds nothing. |

The factory strips surrounding whitespace and normalizes operation names to lowercase. Existing conversion rejects nonnumeric/nonfinite operands and options; `Calculation.get_result()` rejects a nonfinite result. Do not duplicate that policy inside every operation. Construction must not perform arithmetic: an insufficient `span` request can be constructed but raises its domain error when executed.

Parser settings use `key=value`; duplicate names are invalid. New CLI actions follow the existing rule: `last` accepts no arguments. CSV is supported for `mean`, `stddev`, and now `span`; `adjust` remains a typed, single-value operation. Paths with spaces are outside this grammar.

Successful calculations are displayed as `Result: ` followed by four decimal places. Expected failures are displayed as `Error: ...` and permit another request. Exact error wording is flexible. `exit`, EOF, and Ctrl+C print `Goodbye!`. Missing, malformed, headerless, empty, or nonnumeric CSV data follows the supplied error/conversion policy; no observations are silently dropped.

## Preserve controlled history

`History` owns a private `_entries` list. Its supplied API is `add(calculation, result)`, `get_history()` (a **shallow list copy**), and `clear()`. `CalculatorSession` owns `_history = History()`, exposes `get_history()` and `clear()`, and has no public mutable `history` list. Clearing a returned list must not clear the session. This protects the collection; it does not deep-copy each calculation.

`HistoryCommand` already formats saved entries through the supplied `_format_entry(calculation, result)` helper. You may reuse that helper for `LastCommand`. Calculations must not be rerun merely to display history. Repair the marked session defect rather than hiding it in a display command.

## Example and deliberate failure

```text
> adjust 3 offset=2 scale=4
Result: 20.0000
> span -4 3 8
Result: 12.0000
> span 1
Error: Enter at least two values.
> last
span -4.0 3.0 8.0 = 12.0000
> clear
History cleared.
> last
History is empty.
> exit
Goodbye!
```

The supplied `values.csv` contains 10, 20, 30, 40, 50, so `csv span values.csv` displays `Result: 40.0000`. Checks use other inputs; hardcoded examples do not satisfy the contract. Options in a saved request may appear in either order, but both names and saved values must be visible.

## Assessment and feedback

| Evidence | Points |
| --- | ---: |
| Twelve published automated behavior checks, 5 points each | 60 |
| Your tests with justified cases | 20 |
| Request traces and design explanations | 20 |
| Total, including instructor review | 100 |

`python grading/grade.py` creates `grade-results.json` and `grade-summary.md`, reports **out of 60**, and exits 1 until every automated check passes. It does not award the manual 40 points. Actions → Practice feedback provides the same portion of feedback and downloadable `practice-feedback-60-points`; fork-owned results are feedback, not official grading or integrity review. The [manual rubric](MANUAL_REVIEW.md) and [alignment map](docs/alignment.md) publish the remaining expectations.

Add your tests in `tests/test_student_*.py`, without editing the acceptance tests. Include `REFLECTION.md` with:

- A trace of `adjust 3 offset=2 scale=4` from input to saved history, identifying values/types, construction versus execution, and returned display text.
- A trace of a one-value `span` failure followed by `last`, including the point of exception propagation and why history remains unchanged.
- An explanation of the static-operation/instance-command distinction, `*args`/`**kwargs`, factory versus command roles, and one deliberate EAFP/LBYL choice. Reason about correctness and expected failure; a CPU-versus-memory slogan earns no credit.
- Brief explanations of the behavior your tests establish and why their cases are useful.

Suggested timed allocation: 10 minutes inspect supplied flow; 20 operations/registries; 20 session repair/last; 15 CLI/CSV integration; 15 tests; 10 traces and submission. This is a target to pilot, not a measured completion guarantee.

```bash
python -m pytest
python grading/grade.py
git add calculator tests REFLECTION.md
git commit -m "Adapt calculator for measurement calibration"
git push origin main
git rev-parse HEAD
```

Submit your fork URL and full commit SHA through the announced course channel. There is no exact coverage-percentage requirement.

## Resource policy

Work individually. Course notes, the teaching repository, and your own prior calculator code are allowed; reuse understood components and identify reused sources in your reflection. AI assistance and communication with others during the timed attempt are prohibited. Do not use another student's work. The instructor may announce additional institutional rules before the attempt.

Do not open the practice `solution` branch until your timed attempt is complete. Afterward, compare responsibilities, failure flow, and test choices, then explain one improvement you would make. A copied teaching implementation lacks these new behaviors; copying an assessment solution is not application of the ideas.
