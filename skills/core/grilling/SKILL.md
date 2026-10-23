---
name: grilling
description: Interview the person in rounds until the solution model of the project and the task of the next run are clear. Use before each new run, when a request is vague, or when a new fact changes the question.
---

# Grilling

Find what the person wants to do, why, and for whom. Ask only what you cannot find yourself.

Grilling works on two levels:

- The **solution model** of the project. It lives in `CLAUDE.md`. It says why the project exists, how it gets the result, and why that can work.
- The **task of the run**. It lives in one `DECISION grilling` entry in `LOG.md`. Each run has its own task. For example, R01 studies RNA, R02 studies H&E slides, and R03 joins the two.

Each new run starts with grilling. The skill "planner" does not make a run without a grilling entry for that run.

Follow the sections "Who decides" and "Chat style" in `CLAUDE.md`. Mark each answer `(person)` or `(agent)`. Number the questions through the whole session.

## Process

1. Read what exists: the request, the data files, `CLAUDE.md` (the solution model, the project rules, the State), `LOG.md` (grilling entries, `post-hoc`, `deviation`, and `RULE` entries), and the `result` and `notes` of each `run.yaml`. Find facts yourself. Do not ask the person for a fact that the files can show.
2. Find the id of the next run: the newest run without a `plan accepted` entry in `LOG.md`, or the highest run number + 1.
3. Make sure that the solution model is ready:
   - If `CLAUDE.md` has no solution model, or the model is `draft`, build it first. See "Solution model" below. The model questions are the first rounds.
   - If the model is confirmed, show it to the person in 3 to 5 lines. Ask one question: "Is the solution model still valid? yes / change". If the answer is "change", ask only about the parts that changed.
4. Search the published work before you ask about the run:
   - the published result that the analysis must reproduce or compare with,
   - whether the thing under discussion (a signature, a method, a cut-off, a data set) is already public, and on which terms.
   A public fact can change the decision. Put it in the next round.
   If a site blocks access, try another source: the publisher page, an institutional repository PDF, a preprint server, or the abstract. Record the blocked source. Mark a prior from an abstract only as `weak`.
5. Make the **frontier**: the list of open questions that block the run. Use the topics in [TOPICS.md](TOPICS.md). Add each contradiction that you find (see "Contradictions").
6. Ask one round: 3 to 6 questions. Give each question:
   - options on short lines,
   - your recommended option, marked (not for the useful action, see "Solution model"),
   - one line: why the answer changes the analysis.
7. Read the answers. The word "yes" accepts all recommendations as `(person)`. A choice that the person gives to you is `(agent)`. Compare each answer with the project rules (see "Project rules"). Remove answered questions from the frontier. Add new questions that the answers open.
8. Do step 6 again until the frontier is empty.
9. If the solution model is new or changed, write it in `CLAUDE.md` and add one `DECISION model` entry to `LOG.md` (see "Solution model").
10. Write the task of the run in `LOG.md` as one `DECISION` entry with these lines, in this order:

```
## <YYYY-MM-DD> · DECISION grilling
run: <RNN, the run that the planner will make>
question: <one sentence> (person | agent)
decision: <what changes with the answer>; owner: <who decides>; reader: <who reads> (person | agent)
method: <which data, which comparison, which result ends this run> (person | agent)
plausibility: <why this run can answer the question: mechanism, prior, controls> (person | agent)
inputs: <earlier runs that this run uses, or: none>
cost-of-error: <which error costs more> (person | agent)
population: <who is in scope> (person | agent)
reference: <the reference test or variable, if any> (person | agent)
success: <threshold for "yes">, on <assay or platform where the decision applies> (person | agent)
prior: <result, reference> (strong | weak | none found)
rules: <RULE ids that apply to this run, or: none>
sources: <URLs or references used; blocked sources>
context: <N> of 8 (agent)
```
   `context` counts the 8 lines with a `(person | agent)` mark. If more than 4 are `(agent)`, tell the person: "<N> of 8 decisions came from me, not from you. The planner will ask before it starts." Ask again about these lines if the person is available.
   The question rounds stay in the chat. Do not save them in a file. If `LOG.md` does not exist, tell the person to run `/setup-project` first.

## Solution model

The solution model is a short explanation of the project. It has three parts:

- **Useful action**: who gets the benefit and which decision or action changes. Examples: a narrow group of patients, a team in a pharma company that ordered the project, the bioinformatician and their own business.
- **Method**: which data, which comparison, and which result ends the work.
- **Plausibility**: why the method can work. Give the biological mechanism or the published prior, the controls, and the known limits.

Write it between the markers in `CLAUDE.md`. Only this skill writes this block. The curator script does not change it.

```
<!-- model:begin -->
- Useful action: <who gets the benefit; which decision or action changes>
- Method: <which data; which comparison; which result ends the work>
- Plausibility: <mechanism or prior; controls; known limits>
- Limits: <what the project cannot answer>
- Confirmed: <person> <YYYY-MM-DD>
<!-- model:end -->
```

Rules for the model:

- Ask for the useful action first. Without it, the project is not ready.
- If the person cannot name who gets the benefit, do not leave the person alone with the question. Propose 2 to 4 options from the context: the request, the data, the expected patient group, or the general logic of the task. Give one line per option: why you think so. Do not mark an option as recommended. A "yes" must not choose the useful action for the person. The person chooses an option or writes their own.
- The model has no `(agent)` part. Only the person chooses the useful action.
- You may propose the method and the plausibility. The person confirms each part. The word "yes" to a round with your proposal confirms it. A choice that the person gives to you does not confirm it.
- The model is not ready if it does not answer "why" (useful action) or "how" (method). A vague part is not ready. Ask again.
- If the person is not available, write `Confirmed: draft - not confirmed`. Stop. Tell the person that the model needs their answer. The planner does not start on a draft model.
- Each change of the model gets one entry in `LOG.md`:

```
## <YYYY-MM-DD> · DECISION model
changed: <which part, from what to what>
reason: <why, in the words of the person>
confirmed: <person>
```

## Contradictions

Look for contradictions and vague statements in each round. Each one becomes a question in the next round. Check that these planes agree:

- the useful action and the question of the run,
- the data and the method,
- the resources: time, money, and the due date.

Also check the model against what the data can show. Example: 12 cases in the smallest group cannot support a threshold of 95% sensitivity.

## Project rules

The section `## Project rules` in `CLAUDE.md` holds the lessons of earlier runs. Read it before the first round.

- If an answer of the person goes against a rule, say so before you continue: "In <run> this caused <problem>. Then we decided <rule> (RULE-NN)." Quote the rule. Ask: "Follow RULE-NN? yes / deviate".
- If the person chooses to deviate, add one entry to `LOG.md`. Quote the words of the person.

```
## <YYYY-MM-DD> · DECISION deviation RULE-NN
run: <RNN>
reason: <the words of the person>
```

- Never change or delete a rule. Only the person edits the section, by hand.

## Rules

- The person makes decisions. You find facts.
- Always ask for the success threshold: the number that makes the answer "yes". If the person cannot give one, recommend one and mark it `(agent)`. The report must show it.
- When an answer is vague or does not answer the question, restate it as a rule and ask for "yes".
- When the person does not choose, or is not available, use the recommended option and mark the line `(agent)`. Continue. This does not apply to the solution model.
- Stop when the frontier is empty. Do not ask questions that do not change the analysis.

## Done when

- `CLAUDE.md` has a solution model with all three parts and a `Confirmed` line with the name of the person.
- The person confirmed the model in this grilling, or confirmed that the old model is still valid.
- The `DECISION grilling` entry names the run, the question, the method, the plausibility, and the inputs.
- One sentence states the decision that the answer serves and who makes it.
- The published prior is named, or the entry says `prior: none found`.
- Each project rule that conflicts with an answer has a `follow` answer or a `DECISION deviation` entry.
- Each of the 8 decision lines has `(person)` or `(agent)`, and the entry has the `context` line.
