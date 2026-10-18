---
name: grilling
description: Interview the person in rounds until the analysis question, the data, and the decision are clear. Use before any analysis starts, when a request is vague, or when a new fact changes the question.
---

# Grilling

Find what the person must decide. Ask only what you cannot find yourself.

## Process

1. Read what exists: the request, the data files, `CLAUDE.md`, `LOG.md`. Find facts yourself. Do not ask the person for a fact that the data can show.
2. Make the **frontier**: the list of open questions that block the analysis. Use the topics in [TOPICS.md](TOPICS.md).
3. Ask one round: 3 to 6 questions. Give each question:
   - options on short lines,
   - your recommended option, marked,
   - one line: why the answer changes the analysis.
4. Read the answers. The word "yes" accepts all recommendations. Remove answered questions from the frontier. Add new questions that the answers open.
5. Do step 3 again until the frontier is empty.
6. Write the result in `LOG.md` as one `DECISION` entry: the question, the decision it serves, the key choices.

## Rules

- The person makes decisions. You find facts.
- When the person is not available, use the recommended option. Write `assumed:` before it in `LOG.md`. Continue.
- Stop when the frontier is empty. Do not ask questions that do not change the analysis.

## Done when

- One sentence states the question.
- One sentence states the decision that the answer serves and who makes it.
- Each blocking topic has an answer or an `assumed:` line.
