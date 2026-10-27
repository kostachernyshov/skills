# Scope

## In scope
- The path from a question to a decision on processed tabular data.
- Project order, versions, and releases for analysis projects.
- Checks of plausibility before a result.
- Communication of a result to the person who decides.

## Out of scope
- Methods for raw data and pipelines. See `UPSTREAM.md`.
- Wrappers for one tool or one database.

## How a new skill gets in
1. Someone sees a failure in a real project or in a test in `tests/`.
2. The failure is written as an issue with the evidence.
3. The fix goes into an existing skill if possible. A new skill starts in `skills/in-progress/`.
4. The curator moves it into a bucket after it passes a test round.
5. A rejected idea goes into `.out-of-scope/<idea>.md` with the reason.

Pull requests that add checks to `skills/analysis/checker/CHECKS.md` or examples to `tests/` are welcome.
