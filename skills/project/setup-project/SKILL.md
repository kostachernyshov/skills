---
name: setup-project
description: Create the standard folder layout and the two service files for a new analysis project. Run once per project, before grilling.
disable-model-invocation: true
---

# Setup project

Make one layout that the person and agents can read without help.

## Steps

1. Use the folder name as the project name. Use lowercase and hyphens.
2. Make this layout in the project root:

```
CLAUDE.md      # agent rules + "State" section
LOG.md         # decisions and releases, newest first
data/          # input data, read only, not in git
data/ref/      # small reference files from papers (weights, gene lists), in git
runs/          # analysis iterations
releases/      # what the client saw, never changed
scratch/       # temporary files, not in git
```

3. Put an empty `.gitkeep` file in `runs/`, `releases/`, and `data/ref/`. Git does not keep empty folders.
4. Copy the templates from [templates/](templates/):
   - `CLAUDE.md.tmpl` to `CLAUDE.md`. Fill the project name and the data table.
   - `LOG.md.tmpl` to `LOG.md`. Add the first entry: `SETUP`.
   - `gitignore.tmpl` to `.gitignore`.
5. Make `AGENTS.md` so that other agents read the same rules. Try a symlink to `CLAUDE.md`. If the symlink fails, write one line in `AGENTS.md`: `Read CLAUDE.md. It has all project rules.`
6. Move each input file into `data/`. If the files came in another folder (for example `incoming/`), move them and delete the empty folder. Do not change the content of input files.
7. Record each input file in the `Data` table of `CLAUDE.md`: source, date, size, rows x columns. If the source is not known, write `client file, source not verified`.
8. Run `git init` if the folder is not a git repository. Make the first commit.
9. Call the Skill tool with "project-order". Apply its rules from now on.

## Done when

- The layout exists and is in the first commit.
- `CLAUDE.md` names each input file and its source.
- `LOG.md` has the `SETUP` entry.
