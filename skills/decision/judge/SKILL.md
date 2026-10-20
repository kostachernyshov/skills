---
name: judge
description: Decide in a fresh context if a brief can be trusted. A subagent that sees only the files answers 5 fixed yes/no questions. One "no" is a veto. Use after a brief is written or changed, and before a release.
---

# Judge

The agent that did the analysis knows more than the files show. The reader knows only the files. The judge reads only the files. So the judge must be a fresh subagent. The same model is acceptable. The context must be new.

The judge asks "can the reader trust this?". The skill "reviewer" asks "can the reader understand this?". They are different roles.

## Steps

1. Find the run: `runs/RNN-<slug>/`. It must have `run.yaml`, `out/`, and `out/brief.md`.
2. Start a new subagent with the Agent tool. Give it only this prompt, with the paths filled in:

   > You are a judge. Read the file `<this skill>/QUESTIONS.md` and follow it. The project root is `<path>`. The run is `runs/RNN-<slug>/`. Read only `run.yaml`, the files in `out/`, and `LOG.md`. Do not read `code/`, the chat, or any other file.

   Do not give the subagent a summary of the work. Do not tell it what you expect.
3. Copy the verdict line that the subagent returns into `run.yaml` as the value of `verdict`. Do not change the words. Add the checksum of the brief at the end: ` - brief <first 8 characters of sha256sum out/brief.md>`. Parse `run.yaml` after the edit.
4. If the verdict is `veto`: tell the person the question number and the reason. Fix the cause in the analysis or in the brief. Then start a new subagent. Do not send the old judge your answer.
5. After 3 vetoes on the same question, stop. Ask the person what to do.

## Rules

- Only this skill writes `verdict`. Never edit the verdict to `pass` by hand.
- A change to `brief.md` or to a number in `out/` after the verdict makes the verdict old. Run the judge again. The curator script shows a verdict whose checksum does not match the brief as `Open`.
- If you cannot start a subagent, write `verdict: "veto - Q0: no fresh context; judge not run"` and tell the person. The skill "publisher" stops on it.

## Done when

- `run.yaml` has `verdict` with `pass` or `veto`, a date, the reason for a veto, and the checksum of the brief.
- The verdict came from a subagent that did not see the chat.
