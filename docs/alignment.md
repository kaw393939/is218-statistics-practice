# Alignment with the six-part sequel

Students enter after completing [the OOP calculator](https://github.com/kaw393939/is218-oop-calculator). They have already seen objects, inheritance, abstraction, encapsulated history, exception handling, tests, and a CLI. This practice asks them to adapt familiar infrastructure rather than repeat a reference implementation.

| Teaching part | Practiced idea | Application here | Evidence |
| --- | --- | --- | --- |
| 1. Refactor the existing calculator | Static operations and composed calculation state | Add a calibration operation using supplied formula | Static operation tests; successful trace |
| 2. Create calculations with a factory | Centralize selection/configuration; construction defers execution | Extend existing registries for new calculations | Factory/option/deferred checks |
| 3. Support different operation inputs | Unary, variable positional inputs, named settings | `adjust` and `span`, keyword-only offset/scale | Argument tests; explanation |
| 4. Represent actions as commands | Shared execution contract, controlled session state | LastCommand reads the most recent saved success | Command, saved-result, snapshot checks |
| 5. Add statistics and CSV input | Separate source from operation; shared validation | Route CSV readings to span without a second math implementation | CSV integration/recovery check |
| 6. Integrate, explain, and transfer | Trace failure, repair behavior, justify tests | Repair premature history recording and explain recovery | State check; student tests; two traces |

## Why course copying is insufficient

The teaching calculator lacks adjustment, span, LastCommand, and the new routes. This starter deliberately introduces a history-order defect. Unchanged course code therefore cannot satisfy the published adaptation checks. Reusing the base calculation, factory machinery, history abstraction, and parser is allowed; students must supply the changed behavior and explain it.

Do not turn a check of copying into a blanket plagiarism accusation: failing or passing automated checks alone does not establish authorship. Keep feedback centered on behavior and independently review the written evidence.

## Bounded cognitive scope

Provide formulas, completed base classes, CSV reading, numeric policy, command formatting, and the input loop. Only new operations, registry entries, one small action, two routes, and a visible state-order bug are unfinished. New domain terminology, batch workflows, and unfamiliar pandas APIs are not required for this practice.

The exam must use the same six-part ideas in a changed workflow; it should not be this assessment with renamed operations or one different default. Student-written tests and request explanations contribute 40% of both assessments. Published hidden variations may change data and published edge cases; they must not add undisclosed APIs or rules. Pilot timing with representative students before release.
