---
name: {{NAME}}
description: {{DESCRIPTION}}
---

# {{TITLE}}

Context: one or two sentences naming what this skill does. The `description`
frontmatter above is the trigger, so do not repeat a "when to use" list here.
Keep this file a slim router. Detail lives in the folders and loads only when the
relevant path is taken.

## Workflow
1. Step one. Follow `protocols/<name>.md`.
2. Step two.
3. Validate with `scripts/`, then refine.

## Map
- `references/` background knowledge, read on demand.
- `protocols/` step-by-step workflows.
- `scripts/` CLI validators and helpers. Run them, do not reimplement.
- `templates/` files to copy and fill.
- `agents/` subagent prompts for delegated work.

## Refine
At the end of a session that used this skill, run `protocols/self-refine.md`.
