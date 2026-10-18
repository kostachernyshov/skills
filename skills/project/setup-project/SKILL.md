---
name: setup-project
description: Create the standard folder layout and the two service files for a new analysis project. Run once per project.
disable-model-invocation: true
---

# Setup project

Make one layout that the person and agents can read without help.

## Steps

1. Ask for the project name if you do not know it. Use lowercase and hyphens.
2. Make this layout in the project root:

```
CLAUDE.md      # agent rules + "State" section
LOG.md         # decisions and releases, newest first
data/          # input data, read only, not in git
runs/          # analysis iterations
releases/      # what the client saw, never changed
scratch/       # temporary files, not in git
```

3. Copy the templates from [templates/](templates/):
   - `CLAUDE.md.tmpl` to `CLAUDE.md`. Fill the project name, the data source, and the question if known.
   - `LOG.md.tmpl` to `LOG.md`. Add the first entry: `SETUP`.
   - `gitignore.tmpl` to `.gitignore`.
4. Make a symlink `AGENTS.md` to `CLAUDE.md` so that other agents read the same file.
5. Put each input file in `data/`. Do not change input files. Record in `CLAUDE.md` for each file: the source (accession or URL), the date, the size.
6. Run `git init` if the folder is not a git repository. Make the first commit.
7. Call the Skill tool with "project-order". Apply its rules from now on.

## Done when

- The layout exists.
- `CLAUDE.md` names each input file and its source.
- `LOG.md` has the `SETUP` entry.
- The first commit exists.
