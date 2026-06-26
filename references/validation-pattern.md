# Validation pattern

Two layers of validation ship with a skill. Generic checks every skill should
pass, and domain checks specific to what the skill produces. This file describes
how to write both, CLI-first.

## Generic checks (provided)
`scripts/validate_skill.py` checks what any skill must satisfy: frontmatter has a
kebab-case `name` and a non-empty `description`, the router stays under the length
threshold, and every local file reference resolves (dependency mapping). Run it on
any skill directory. These are the checks skill-crafter enforces on itself.

## Domain checks (you write per skill)
The generic checks cannot know what *your* skill cares about. If the skill emits
data that must be shaped a certain way, or output that must obey a rule, write a
check for it. The em-dash example is just one instance of the general idea: any
constraint a human would otherwise eyeball becomes a script. Examples:
- Output JSON must match a schema.
- A generated file must contain required sections.
- A produced list must be unique and sorted.
- A field must fall within a range.

## How to write one
Follow `templates/script.template.py`:
1. One script, one responsibility. Name it for what it checks.
2. Accept the target as a CLI argument; add `--help` via argparse.
3. Print each violation as `path:line: message` so it is actionable.
4. Exit 0 when clean, non-zero when violations exist, 2 on usage error.
5. Stdlib only, so it runs with no install step.

## How the skill uses it
The skill's protocol runs the checks before declaring done and treats a non-zero
exit as a stop. The agent reads the printed violations, fixes them, and re-runs.
A check that is never run is documentation, not validation, so wire it into the
protocol. See `protocols/validate.md`.
