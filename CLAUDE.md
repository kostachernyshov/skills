# Rules for agents that change this repository

- Write SKILL.md files in ASD-STE100 Simplified Technical English: short sentences, active voice, one instruction per sentence.
- Each skill has a "Done when" section with checks that can be verified.
- A person skill can call an agent skill. A person skill never calls another person skill.
- Write a dependency as: Call the Skill tool with "<name>". Do not link to files of another skill.
- When you add, remove, or rename a person skill, update `skills/ask-kosta/SKILL.md` in the same commit.
- Add a skill only for a failure that was seen in a real test (see `SCOPE.md` and `tests/`).
- Record each change in `CHANGELOG.md`.
