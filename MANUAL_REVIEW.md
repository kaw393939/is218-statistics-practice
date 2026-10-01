# Manual review: 40 points beyond automated feedback

The automated grader verifies twelve published behavior checks worth 60 points. Passing all checks is not a 100-point grade. Review the student's submitted commit and `REFLECTION.md` for the two evidence groups below. Grade clarity and correctness rather than length, vocabulary density, or matching reference prose.

## Student tests: 20 points

| Evidence | Points | Full-credit standard |
| --- | ---: | --- |
| Calibration test choices | 5 | Cases distinguish add-then-scale from scale-then-add, and cover a useful default or boundary without simply duplicating a provided assertion. |
| Variable inputs and invalid requests | 5 | Tests exercise meaningful span or option cases and assert the appropriate outcome/error. |
| State and execution ordering | 5 | A test demonstrates no failed record or no recalculation on last; its assertions would catch a real regression. |
| Test explanation | 5 | Student identifies the behavior each chosen case establishes, including what a flawed implementation would do. |

For each row: 5 = meets the stated standard; 3 = partly correct with a material gap; 1 = minimal evidence; 0 = absent or incorrect. Tests must run and avoid hardcoding repository internals unrelated to the published contract. A student's justified alternative case can earn full credit. Quantity of tests and exact coverage percentage are not grading criteria.

## Request traces and design: 20 points

| Evidence | Points | Full-credit standard |
| --- | ---: | --- |
| Successful trace | 5 | Follows supplied text parsing, factory configuration/finite conversion, unexecuted Calculation, CalculateCommand/session execution, static adjustment, actual saved result, and display. |
| Failed trace | 5 | Locates span's minimum-count error during execution, explains propagation to CLI recovery and why the earlier saved entry remains last. |
| Component and argument reasoning | 5 | Explains static versus instance state; positional `*args` and named `**kwargs`; factory construction versus command action; why LastCommand uses a saved result. |
| Error-policy reasoning and attribution | 5 | Justifies one EAFP/LBYL choice using a real operation, safe failure, or reliable cheap check; accurately identifies reused course/prior code. |

Use the same 5/3/1/0 anchors. A correct concise trace can earn full credit. Screenshots alone are not a trace, and pattern names without responsibility explanations are insufficient. Undisclosed source-code shape or instructor-preferred syntax must not become a hidden criterion.

Final grade = automated score (0–60) + these manual scores (0–40). Integrity matters are handled under the announced course policy, separately from inventing additional behavioral requirements.
