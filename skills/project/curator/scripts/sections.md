## Who decides

- Mark each decision line in `LOG.md` and `run.yaml` with `(person)` or `(agent)`.
- `(person)`: the person wrote the answer, or saw the exact option and chose it ("yes", "option B").
- `(agent)`: the person gave the choice to the agent, in any words ("ok, your choice", "I rely on you", "I do not know, you decide").
- The solution model is always `(person)`. The agent may propose the method and the plausibility. Only the person gives the useful action.
- An `(agent)` answer never accepts a `todo`, a deviation from a project rule, an override, or a release signature. These need the words of the person.
- Start the analysis of a run only when `LOG.md` has `plan accepted` for that run. A request in plain text ("compute X", "just do it") is not a plan. Tell the person: "Run /grill-with-plan first."

## Chat style

- Number the questions Q1, Q2, Q3 through the whole session. Do not start again at Q1 in a new round.
- Write each question as `❓ **Q7** - **<title>**: <question>`, then `➡️ <recommended answer>`. Word the question so that "yes" accepts the recommendation.
- Mark a status: ✅ pass, ⚠️ warn, ⛔ veto or fail, 🔴 warning about missing context.
- For an explanation with 3 or more linked steps, draw a diagram (ASCII text in the terminal). Do not write long paragraphs.
