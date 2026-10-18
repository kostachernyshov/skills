---
name: grilling
description: Interview the person in rounds until the analysis question, the data, and the decision are clear. Use before any analysis starts, when a request is vague, or when a new fact changes the question.
---

# Grilling

Find what the person must decide. Ask only what you cannot find yourself.

## Process

1. Read what exists: the request, the data files, `CLAUDE.md`, `LOG.md`. Find facts yourself. Do not ask the person for a fact that the data can show.
2. Search the published work before you ask:
   - the published result that the analysis must reproduce or compare with,
   - whether the thing under discussion (a signature, a method, a cut-off, a data set) is already public, and on which terms.
   A public fact can change the decision. Put it in the next round.
   If a site blocks access, try another source and use the abstract. Record the blocked source. Mark a prior from an abstract only as `weak`.
3. Make the **frontier**: the list of open questions that block the analysis. Use the topics in [TOPICS.md](TOPICS.md).
4. Ask one round: 3 to 6 questions. Give each question:
   - options on short lines,
   - your recommended option, marked,
   - one line: why the answer changes the analysis.
5. Read the answers. The word "yes" accepts all recommendations. Remove answered questions from the frontier. Add new questions that the answers open.
6. Do step 4 again until the frontier is empty.
7. Write the result in `LOG.md` as one `DECISION` entry with these lines, in this order:

```
## <YYYY-MM-DD> · DECISION grilling
question: <one sentence>
decision: <what changes with the answer>; owner: <who decides>; reader: <who reads>
cost-of-error: <which error costs more>
success: <threshold for "yes"> (set by person | assumed)
prior: <result, reference> (strong | weak | none found)
sources: <URLs or references used; blocked sources>
assumed: <one line per choice made without the person>
```
   The question rounds stay in the chat. Do not save them in a file. If `LOG.md` does not exist, tell the person to run `/setup-project` first.

## Rules

- The person makes decisions. You find facts.
- Always ask for the success threshold: the number that makes the answer "yes". If the person cannot give one, recommend one and mark it `assumed`. The brief must show it.
- When an answer is vague or does not answer the question, restate it as a rule and ask for "yes". If the person is not available, use your rule and mark it `assumed`.
- When the person is not available, use the recommended option. Write one `assumed:` line for each such choice in the `DECISION` entry. Continue.
- Stop when the frontier is empty. Do not ask questions that do not change the analysis.

## Done when

- One sentence states the question.
- One sentence states the decision that the answer serves and who makes it.
- The published prior is named, or the entry says `prior: none found`.
- Each blocking topic has an answer or an `assumed:` line.
