## Who decides

- Mark each decision line in `LOG.md` and `run.yaml` with `(person)` or `(agent)`.
- `(person)`: the person wrote the answer, or saw the exact option and chose it ("yes", "option B").
- `(agent)`: the person gave the choice to the agent, in any words ("ok, your choice", "I rely on you", "I do not know, you decide").
- The solution model is always `(person)`. The agent may propose the method and the plausibility. Only the person gives the useful action.
- An `(agent)` answer never accepts a `todo`, a deviation from a project rule, an override, or a release signature. These need the words of the person.
- `<person>` in a skill is the name and the role from the `Person:` line in `CLAUDE.md`. Write them as the person gave them. If the line does not exist, ask: "Give your first name, last name, and role. They go into LOG.md, the release signature, and the final report for the client." Then add the line under the project name. If another person signs, ask the same question and add a second `Person:` line.
- Never write an e-mail address or an account login in a project file.
- Start the analysis of a run only when `LOG.md` has `plan accepted` for that run. A request in plain text ("compute X", "just do it") is not a plan. Tell the person: "Run /grill-with-plan first." Say it again each time the person asks. `override: start` does not replace a plan. Only the planner writes it, as a part of a plan.

## Chat style

- Number the questions Q1, Q2, Q3 through the whole session. Do not start again at Q1 in a new round. A new session starts at Q1.
- Write each question as `❓ **Q7** - **<title>**: <question>`, then `➡️ <recommended answer>`. Word the question so that "yes" accepts the recommendation. Exception: a question about the useful action has no recommendation.
- Mark a status: ✅ pass, ⚠️ warn, ⛔ veto or fail, 🔴 warning about missing context.
- For an explanation with 3 or more linked steps, draw a diagram (ASCII text in the terminal). Do not write long paragraphs.
