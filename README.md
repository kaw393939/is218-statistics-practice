# Practice test: Command, Simple Factory, and pandas

This is a full 90-minute practice test. The real test will not be exactly the same: expect a small change to the statistic or requirements. The setup, architecture, and workflow will be familiar. Understand your code so you can adapt it.

**Time limit: 90 minutes.** Start timing after reading the instructions; setup is part of the attempt. Infrastructure is supplied so you can focus on implementation. Before the exam, verify Python and GitHub access. Complete TODOs in calculator/, keep the documented API, and add your own meaningful tests. The starter is intentionally incomplete and its initial grading run is expected to fail.


## Set up your workspace

Use Python 3.11–3.14. Fork the repository on GitHub, then clone **your fork** and change into its folder. Replace YOUR-USERNAME and REPOSITORY below.

```bash
git clone https://github.com/YOUR-USERNAME/REPOSITORY.git
cd REPOSITORY
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell use `py -m venv .venv` and `.venv\Scripts\Activate.ps1` instead. If activation is restricted, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and that interpreter for the commands below. On macOS/Linux you can likewise use `.venv/bin/python` without activation.

```bash
python -m calculator
python -m pytest
```

Run from the repository root: `csv` reads `values.csv` in the current working directory. Use `deactivate` when finished. Do not commit `.venv`.


## What to build

An interactive calculator with exactly these commands:

| Command | Behavior |
| --- | --- |
| manual | Prompt for whitespace-separated numbers and calculate sample standard deviation |
| csv | Read the supplied values.csv automatically; use its value column |
| exit | Print Goodbye! and end the session |

No filename or column selection is required. No history, removal, GUI, undo, Facade, or extra arithmetic is required.

Use pandas for CSV reading and calculation. **Use sample standard deviation, explicitly ddof=1.** Both sources use one shared calculation function. Require at least two finite numeric values, including for this exam's population calculation. Reject nonnumeric values, missing cells, NaN, infinity, and nonfinite results. Blank CSV lines ignored by read_csv do not count as observations; an empty quoted cell is a missing value and must be rejected. Missing files, malformed/empty CSVs, missing value columns, and unknown commands produce a clear Error: message and return to the prompt. EOF and Ctrl+C end cleanly.

The supplied CSV contains 10, 20, 30, 40, 50. Its sample standard deviation displays 15.8114. Do not hardcode data or expected answers. Tests also use other values.

## Required API and responsibilities

| File | Contract |
| --- | --- |
| calculator/statistics.py | standard_deviation(values) -> float; raise ValueError for invalid values |
| calculator/commands.py | Abstract Command with execute(); concrete ManualStdDevCommand(values) and CsvStdDevCommand(path="values.csv") |
| calculator/factory.py | CommandFactory.create(name, values=None) -> Command; normalize whitespace/case; reject unknown names or absent manual values with ValueError |
| calculator/cli.py | run() implements the loop using CommandFactory.create and command.execute() |
| calculator/__main__.py | Supplied entry point for python -m calculator |

Commands must import `standard_deviation` from calculator.statistics under that name and call it. They must not prompt for input. CsvStdDevCommand.execute() must use pandas.read_csv; its optional path supports testing, while the CLI always uses the default. The factory constructs and returns objects without executing them. The CLI invokes execute() and formats results to four decimal places.

## Example manual session

```text
> manual
Enter values separated by spaces: 10 20 30 40 50
Standard deviation: 15.8114
> exit
Goodbye!
```

Prompts can include a greeting; retain the result prefix Standard deviation:, error prefix Error:, and Goodbye! output. On invalid input, keep accepting commands.

## Run the grading feedback

```bash
python -m pytest
python grading/grade.py
```

Twenty named acceptance checks are worth five points each. The grader creates grade-results.json and grade-summary.md and exits with code 1 below 100 points. A failing grade is normal while you work. The untouched starter scores 5/100 because its abstract Command interface is supplied; the remaining 95 points require implementation. Add your tests in a separate test file; do not edit the supplied acceptance tests, rubric, grading script, or workflow.

| Category | Points |
| --- | ---: |
| Manual calculation | 20 |
| CSV input | 20 |
| Command architecture | 20 |
| Simple Factory | 20 |
| Validation and CLI | 20 |

Commit and push to your fork. If Actions is disabled, open its Actions tab and enable workflows, then push a new commit or manually run the workflow. Open **Actions → Practice feedback → latest run** for the score summary and download calculator-feedback for the JSON and summary. A green check means the supplied automated rubric reached 100, not that an instructor has completed design review.

## Submission

```bash
git add calculator tests README.md
git commit -m "Implement statistics calculator"
git push origin main
git rev-parse HEAD
```

Submit your fork URL and final commit SHA through the course's normal submission channel before the announced deadline. The instructor grades that commit using their own unchanged tests; edits to a fork's grading files cannot raise the official score. Explain briefly in your README where Command and Simple Factory occur and why both commands share calculation logic. No 100% coverage threshold is required.

## Reference policy

Work individually. Course notes and your own practice code are allowed; AI assistance and communication with others during the timed attempt are prohibited. This is the proposed default resource policy; the instructor must confirm or revise it before the timed attempt. Do not copy another student's implementation.

## After your practice attempt

Review the solution branch only after your timed attempt. Compare responsibilities and tests, then repeat from a clean starter without copying.
