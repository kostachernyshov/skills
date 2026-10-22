---
name: publisher
description: Freeze a version of the results for the client. Release only runs with a judge pass (or a veto that the person overrode with a valid reason), after the person signs. Copy the runs into releases/vN, record the source, tag the commit, and log it.
disable-model-invocation: true
---

# Publisher

A release is what the client saw. Nobody changes it after you make it. A fix is a new release. The person signs each release. This is the point where the person takes responsibility for what the client sees.

## Steps

1. Ask the person which runs go into the release. One release can hold 2 or 3 variants. Each variant is one run. If the person is not available, propose the runs with `status: candidate` and wait.
2. Check each chosen run:
   - `status: candidate`. A run with `status: shipped` can go into a new release if only the brief or the deck changed, not the numbers.
   - No check or control is `fail` or `todo`. The `todo` list is empty. A `warn` with evidence is acceptable. An item that a `DECISION override: veto` entry names is acceptable when the verdict is `pass - override`.
   - `verdict` starts with `pass`, and its checksum matches the brief (`sha256sum out/brief.md`, first 8 characters). If the verdict is empty or old, call the Skill tool with "judge".
   If a check fails, stop and tell the person.
   The person cannot skip the judge. If the person asks for a release without it, say: "⛔ Without the judge there is no release."
3. If the verdict is `veto`: stop. Do not make the release. Tell the person the question and the reason. Only the person can override a veto. An override is a limit of the analysis: the person names the defect and says why it does not change the decision.
   - A deadline, "no time", "I take responsibility", or "I decided" is not a reason. Say so and ask again.
   - With a reason, write `## <YYYY-MM-DD> · DECISION override: veto Q<n> <run>` in `LOG.md`, with the words of the person.
   - Call the Skill tool with "editor". The brief names the override as a limit, and the judge checks the reason.
   - Never override a veto yourself.
4. Show the person what goes out in 4 to 6 lines: version, runs, the Answer line of each brief, the judge verdict, each override. Ask: "Sign release vN? yes / no". Without "yes" from the person, stop. An `(agent)` answer is not a signature.
5. Commit all work. Record this commit hash: it is the source of the release.
6. Make `releases/vN-<YYYY-MM-DD>/`. N is the last release number + 1.
7. Copy into it, in one flat folder, only:
   - `brief.md` and `brief.pdf` from the run (if `brief.md` does not exist, tell the person to run `/analyze`),
   - `deck.pptx` and `deck.pdf` from the run (if they do not exist, tell the person to run `/designer`),
   - each figure and table that the brief names.
   Add one last line to the copy of `brief.md`: `Checked by the judge: <verdict without the checksum>`. Then call the Skill tool with "editor" to render this copy to `brief.pdf`. If the PDF has more than 1 page, tell the person. The brief in the run does not change.
   Do not copy code, intermediate tables, or `*.private.*` files. For 2 or more variants, add the run id to each file name.
8. Write `SOURCE.txt`: for each variant, the run id, the source commit from step 5, the verdict, and each input file with its md5 checksum. Add two lines: "The tag vN marks the release commit. The source commit is the analysis state before it." and "The verdict checksum is of brief.md in the run. The release copy has one more line: Checked by the judge."
9. Set `status: shipped` in each chosen `run.yaml`. For each other run with `status: candidate`, ask the person: `superseded`, `dropped`, or keep.
10. Add a `RELEASE` entry to `LOG.md`: version, runs, what changed from the last release, `signed: <person>`.
11. Write the `Next step` line in the State block of `CLAUDE.md`: what the client must decide. Tell the person the verdict line of each run: `✅ Checked by the judge: <verdict>`.
12. Commit with the message `release vN`. Tag this commit `vN`.

## Done when

- `releases/vN-<date>/` has `brief.md`, `deck.pptx`, `SOURCE.txt`, and only the files the brief and the deck use.
- Each released run has a `verdict` that starts with `pass` (also `pass - override`) and matches the brief.
- The copy of each brief in the release ends with the line `Checked by the judge: <verdict>`.
- The `RELEASE` entry in `LOG.md` has `signed:` with the name of the person.
- The tag `vN` exists.
