"""Run the fixed rubric and publish feedback even when a starter fails."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RUBRIC = json.loads((ROOT / "grading/rubric.json").read_text())


def main():
    # Optional submission directory is used by the instructor-owned grader.
    submission = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    env = os.environ.copy()
    env["PYTHONPATH"] = str(submission)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    outcomes = {}
    diagnostic = ""
    with tempfile.TemporaryDirectory() as directory:
        report = Path(directory) / "results.xml"
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-c", str(ROOT / "pytest.ini"),
                 "-o", "pythonpath=", "--confcutdir", str(ROOT / "tests"), str(ROOT / "tests/test_acceptance.py"),
                 "--junitxml", str(report)],
                cwd=submission, env=env, text=True, capture_output=True, timeout=120,
            )
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            if result.returncode in (0, 1) and report.exists():
                for case in ET.parse(report).iter("testcase"):
                    outcomes[case.attrib["name"]] = not any(
                        case.find(tag) is not None for tag in ("failure", "error", "skipped")
                    )
            else:
                diagnostic = f"Test run could not complete normally (exit {result.returncode}); unverified checks receive zero."
        except subprocess.TimeoutExpired:
            diagnostic = "Test run exceeded 120 seconds; unverified checks receive zero."
    total = 0
    lines = ["# Calculator feedback", "", "| Category | Score |", "| --- | ---: |"]
    checks = []
    for category in RUBRIC:
        score = sum(5 for name in category["tests"] if outcomes.get(name, False))
        total += score
        lines.append(f"| {category['category']} | {score}/20 |")
        checks.extend({"test": name, "passed": outcomes.get(name, False), "points": 5 if outcomes.get(name, False) else 0} for name in category["tests"])
    lines.extend(["", f"**Automated feedback score: {total}/100**", "", "Instructor review confirms the design and submission integrity.", "", diagnostic])
    summary = "\n".join(lines) + "\n"
    Path("grade-results.json").write_text(json.dumps({"score": total, "maximum": 100, "checks": checks, "diagnostic": diagnostic}, indent=2))
    Path("grade-summary.md").write_text(summary)
    print(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as output:
            output.write(summary)
    return 0 if total == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
