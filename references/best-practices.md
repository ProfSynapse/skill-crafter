# Skill best practices

The canonical principles skill-crafter encodes. Every skill it produces should
satisfy these, and skill-crafter itself is the reference implementation. Each
principle links to the reference that expands it.

## 1. SKILL.md is a slim router
The entry file states what the skill is, when to use it, and routes to the
folders. It does not hold the detail. Detail lives in `references/`, `protocols/`,
`agents/`, and loads only when the relevant path is taken. See
`progressive-disclosure.md`.

## 2. Modularize when a file grows too long
When SKILL.md (or any file) stops being scannable, run a SOLID/DRY pass: give
each piece one responsibility, lift it into its own file, replace it with a
pointer, and map the dependencies so nothing dangles. See `progressive-disclosure.md`
and `protocols/modularize.md`.

## 3. Break work into the standard folders
Most skills decompose into five component kinds:
- `agents/` subagent prompts for delegated work.
- `scripts/` CLI tools the agent runs.
- `templates/` files to copy and fill.
- `references/` background knowledge read on demand.
- `protocols/` step-by-step workflows.
Use only the folders a skill needs. See `folder-taxonomy.md`.

## 4. Validate anything programmatically checkable
If a rule can be checked by code, write a check rather than trusting prose to
enforce it: structured data shape, required fields, naming, link integrity, or
any domain constraint the skill cares about. The skill ships the checks and the
protocol runs them before declaring done. See `validation-pattern.md`.

## 5. Scripts are CLI-first
Scripts expose a clear command-line interface (argparse, `--help`, exit codes),
generally in Python and stdlib-only so they run anywhere. The agent invokes a
documented command instead of writing fresh code each time. See
`validation-pattern.md` and `templates/script.template.py`.

## 6. Prompts follow a fixed structure
Agent and prompt files use these headings in order: Context, Mission,
Instructions, Format (optional, only when output has a required shape), and
Guidelines (patterns and anti-patterns). See `prompt-structure.md`.

## 7. Created skills are self-refining
A skill that skill-crafter produces can improve itself. At the end of a session
that used it, it analyzes what went well and what caused friction, gathers user
feedback where possible, applies the smallest durable fix, and records it in its
refinement log. This is instilled in produced skills via
`templates/self-refine.template.md`; skill-crafter itself is author-controlled and
does not self-refine.
