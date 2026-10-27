# A skill system for biotech specialists who want to make decisions and delegate the routine work to agents

![How the skills work: from the question to the release](docs/media/how-it-works.webp)

_This animation was made with the skill [`animate`](skills/in-progress/animate/SKILL.md)._

## Install (1 minute)

### 1. Add the marketplace and install the plugin

```bash
claude plugin marketplace add kostachernyshov/skills
claude plugin install kostachernyshov-skills@kostachernyshov
```

### 2. Open your project folder and start

Start a new Claude Code session in the folder with your data. Type:

```
/kostachernyshov-skills:ask-kosta
```

The plugin adds the prefix `kostachernyshov-skills:` to each command. Below, the commands are short: `/ask-kosta` means `/kostachernyshov-skills:ask-kosta`.

### 3. That is all

`/ask-kosta` reads your folder and tells you the next command.

<details>
<summary><strong>Update</strong></summary>

```bash
claude plugin marketplace update kostachernyshov
claude plugin update kostachernyshov-skills@kostachernyshov
```

Restart the session after the update. Read what changed in [CHANGELOG.md](CHANGELOG.md). Each version starts with "What changes for you".

</details>

## Quick examples

**"Does this gene score predict survival?"** You have an expression table and a clinical table.

```
/setup-project         once: folders, LOG.md, your name and role
/grill-with-plan       the agent asks; you answer and approve the plan
/clear
/analyze R01           checks, figures, a one-page report
/designer              4 to 6 slides for the meeting
/publisher             you sign; the release is frozen
```

**"Describe the cohort, compare the responders, and build a predictor."** One request, two types of task. `/grill-with-plan` proposes a split into runs: first the biology without the outcome, then the work with the outcome. Each run gets its own plan and report.

**"I do not understand the task yet."** Type `/grill-me`. The agent asks questions until the task is clear. It does not make a plan.

**"Where am I?"** Type `/ask-kosta` at any time.

**"The reader does not read reports."** After `/analyze`, type `/animate` for a short pixel-art video of the run. The video at the top of this page was made with it.

## Why these skills exist

An agent can write the analysis code in minutes. The risk is not the speed. The risk is a fast answer that nobody can trust. These skills fix five failures that we saw in tests on public data.

### 1. The agent answers a question that you did not ask

The agent starts to compute before it knows who gets the benefit and which decision changes.

**The fix:** [`/grill-with-plan`](skills/core/grill-with-plan/SKILL.md). The agent asks you in short rounds, each with a recommended option. First the useful action: who gets the benefit, and how. Then the method, and why it can work. Each decision line shows who made it: `(person)` or `(agent)`.

### 2. The result fits the data

A threshold or a control that you choose after you see the outcome makes almost any result look good.

**The fix:** the [plan](skills/analysis/planner/SKILL.md) fixes the success threshold and three controls before the data: a known effect, shuffled labels, and nearby thresholds and subgroups. [`/analyze`](skills/analysis/analyze/SKILL.md) does not start without your "yes" to the plan.

### 3. A number looks right, but it is wrong

The analyst remembers things that the files do not show. A wrong count or a wrong subgroup goes into the report.

**The fix:** the [checker](skills/analysis/checker/SKILL.md) runs the checks before each result. A fresh agent writes the report from the files only. A second fresh agent, the [supervisor](skills/decision/supervisor/SKILL.md), answers 7 yes/no questions from the files. One "no" stops the release.

### 4. The client cannot use the result

A notebook with 40 figures is not a decision.

**The fix:** a one-page report with the answer, the confidence, and the limits. A short deck with [`/designer`](skills/decision/designer/SKILL.md). [`/publisher`](skills/project/publisher/SKILL.md) freezes what the client saw, after your signature.

### 5. A large task mixes everything

Description, comparison, and prediction in one run mix their thresholds. The cohort is described after someone saw the outcome.

**The fix:** [grilling](skills/core/grilling/SKILL.md) proposes a split into runs. A later run can use the results of earlier runs.

## Reference

**Person** skills start only when you type them. **Agent** skills start by themselves when the task fits. A person skill can call an agent skill, never another person skill. The full table and the project layout are in [docs/skills.md](docs/skills.md).

### Flow

**Person**

- **[ask-kosta](skills/ask-kosta/SKILL.md)**: The map of the flow. Reads the project and tells you the next command.
- **[setup-project](skills/project/setup-project/SKILL.md)**: Makes the project layout once: `CLAUDE.md`, `LOG.md`, `data/`, `runs/`, `releases/`.
- **[grill-me](skills/core/grill-me/SKILL.md)**: An interview about a vague task. No plan.
- **[grill-with-plan](skills/core/grill-with-plan/SKILL.md)**: The interview, then the plan with its threshold and controls. Ends with your approval. Each run starts here.
- **[analyze](skills/analysis/analyze/SKILL.md)**: Runs the accepted plan in a clean session: code, checks, figures, and the report.
- **[designer](skills/decision/designer/SKILL.md)**: 4 to 6 slides from the report for the decision meeting.
- **[publisher](skills/project/publisher/SKILL.md)**: Freezes a release after your signature. Only with a supervisor pass.
- **[animate](skills/in-progress/animate/SKILL.md)** (experimental): A pixel-art video of 20 to 45 s from the report. Each number on screen comes from a result file. Demo on TCGA SKCM melanoma: [GIF](docs/media/animate-skcm-demo.gif), [project](skills/in-progress/animate/examples/skcm-demo/README.md).

**Agent**

- **[grilling](skills/core/grilling/SKILL.md)**: The interview method. Builds the solution model of the project and the task of each run.
- **[planner](skills/analysis/planner/SKILL.md)**: Writes the plan: the success threshold and the positive, negative, and robustness controls.
- **[curator](skills/project/curator/SKILL.md)**: Keeps the project memory. A script builds the State from the run files after each answer.

### Trust

**Agent**

- **[checker](skills/analysis/checker/SKILL.md)**: Checks the data and the controls before each result. A doubt becomes a `todo`.
- **[editor](skills/decision/editor/SKILL.md)**: A fresh subagent writes the one-page report from the files only.
- **[supervisor](skills/decision/supervisor/SKILL.md)**: A fresh subagent answers 7 yes/no questions from the files. One "no" is a veto.
- **[reviewer](skills/decision/reviewer/SKILL.md)**: Two review rounds of the report or the deck with the eyes of the reader.

## What is not here

These skills work on processed tables: expression, clinical data, mutation calls, survival. For raw data and for one method, use these projects:

- NGS pipelines: [nf-core](https://nf-co.re)
- Skills for many tools and databases: [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- NGS skills (alignment, variants, single-cell, DE): [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills)
- Life science plugins and MCP servers: [anthropics/life-sciences](https://github.com/anthropics/life-sciences)
- Databases and literature: [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse)

## More

- [Tests on public data](tests/README.md)
- [Rules for contributors and their agents](AGENTS.md)
- [Issues and ideas](https://github.com/kostachernyshov/skills/issues)

License: MIT.
