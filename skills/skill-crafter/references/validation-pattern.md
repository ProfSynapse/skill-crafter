# Validation pattern

Two layers of validation ship with a skill. Generic checks every skill should
pass, and domain checks specific to what the skill produces. This file describes
how to write both, CLI-first.

## Generic checks (provided)
`scripts/validate_skill.py` checks what any skill must satisfy: frontmatter has a
kebab-case `name` and a non-empty `description`, the router stays under the length
threshold, every local file reference resolves (dependency mapping), every source
file is complete (non-empty, closed code fences, not cut mid-sentence), and
imperative keywords are not stranded outside the numbered workflow. Run it on any
skill directory. These are the checks skill-crafter enforces on itself.

`scripts/verify_package.py` is the integrity gate for the *produced* artifact, run
after packaging: it round-trips the `.skill` archive against the source tree by
SHA-256 and runs the same completeness heuristics on the shipped members. A
structure validator reads the source; only this reads what actually shipped.

## Domain checks (you write per skill)
The generic checks cannot know what *your* skill cares about. If the skill emits
data that must be shaped a certain way, or output that must obey a rule, write a
check for it. The em-dash example is just one instance of the general idea: any
constraint a human would otherwise eyeball becomes a script. Examples:
- Output JSON must match a schema.
- A generated file must contain required sections.
- A produced list must be unique and sorted.
- A field must fall within a range.

## Mechanical vs. judgment: do not encode judgment in a script
"Validate anything checkable" over-applies into "encode judgment in code" -- for
example, hardcoding a list of specific "bad" outlet names into a validator. Such a
list cannot generalize and rots as the world changes. Split by what each side is
good at:
- The **script** enforces what is mechanical and stable: shape, presence, enums,
  cross-references, owned-domain math, label validity.
- The **model** applies judgment using a rubric kept in a reference, and emits a
  structured label (an enum, a score, a verdict).
- The script then validates that the label is one of the allowed values and
  aggregates the labels -- it checks the *form* of the judgment, not the judgment.

So instead of `if outlet in BANNED_LIST`, the model reads a credibility rubric,
emits `{"outlet": "...", "rating": "low|medium|high"}`, and the script asserts
`rating` is a valid enum and tallies it. No enumerated list of real-world things
in either direction, because those lists never generalize.

## Package integrity: verify the channel you ship from
A clean structural pass on the source tree can give false confidence while the
artifact is corrupt. If files are authored through one channel (an editor) and
packaged through another (the shell zipping the filesystem), the two views can
diverge and ship a truncated file that every source-side check passes. Round-trip
the produced artifact: open the `.skill`, re-read every member, and compare a hash
or byte count against the source. `verify_package.py` does this and also runs the
completeness heuristics on the shipped bytes. Wire it into the protocol next to the
structure validator -- a structure validator alone cannot see truncation.

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
