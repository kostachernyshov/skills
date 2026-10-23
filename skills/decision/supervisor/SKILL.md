---
name: supervisor
description: Decide in a fresh context if a report can be trusted. A subagent that sees only the files answers 7 fixed yes/no questions. One "no" is a veto. Use after a report is written or changed, and before a release.
---

# Supervisor

The agent that did the analysis knows more than the files show. The reader knows only the files. The supervisor reads only the files. So the supervisor must be a fresh subagent. The same model is acceptable. The context must be new.

The supervisor asks "can the reader trust this?". The skill "reviewer" asks "can the reader understand this?". They are different roles.

## Steps

1. Find the run: `runs/RNN-<slug>/`. It must have `run.yaml`, `out/`, and `out/report.md`.
2. Start a new subagent with the Agent tool. Give it only this prompt, with the paths filled in:

   > You are a supervisor. Read the file `<this skill>/QUESTIONS.md` and follow it. The project root is `<path>`. The run is `runs/RNN-<slug>/`. Read only `run.yaml`, the files in `out/`, `LOG.md`, and the section `## Project rules` in `CLAUDE.md`. Do not read `code/`, the chat, or any other file.

   Do not give the subagent a summary of the work. Do not tell it what you expect.
3. Copy the verdict line that the subagent returns into `run.yaml` as the value of `verdict`. Do not change the words. Add the checksum of the report at the end: ` - report <first 8 characters of sha256sum out/report.md>`. Parse `run.yaml` after the edit.
4. If the verdict is `veto`: tell the person the question number and the reason. Fix the cause in the analysis or in the report. Then start a new subagent. Do not send the old supervisor your answer.
5. After 3 vetoes on the same question, stop. Ask the person what to do.

## Rules

- Only this skill writes `verdict`. Never edit the verdict to `pass` by hand.
- The person cannot turn off the supervisor. The skills "editor" and "publisher" always run it. Without a verdict there is no release.
- Only the person can override a veto, with a reason. The supervisor checks the reason (see "Overrides" in [QUESTIONS.md](QUESTIONS.md)).
- A change to `report.md` or to a number in `out/` after the verdict makes the verdict old. Run the supervisor again. The curator script shows a verdict whose checksum does not match the report as `Open`.
- If you cannot start a subagent, write `verdict: "veto - Q0: no fresh context; supervisor not run"` and tell the person. The skill "publisher" stops on it.

## Done when

- `run.yaml` has `verdict` with `pass`, `pass - override`, or `veto`, a date, the reason for a veto, and the checksum of the report.
- The verdict came from a subagent that did not see the chat.
