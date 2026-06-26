# Folder taxonomy

The five component kinds a skill decomposes into. Each folder holds one kind of
thing. Use only the folders the skill needs; an empty folder is noise.

## agents/
Subagent prompt files for work worth delegating to a fresh context: design,
drafting, adversarial review, anything that benefits from isolation or parallel
fan-out. Each file follows the prompt structure (see `prompt-structure.md`).
Reach for an agent when the work has a clean input and output and does not need
the main thread's full history.

## scripts/
CLI tools the agent runs instead of writing ad hoc code. Generally Python,
stdlib-only, with argparse and meaningful exit codes. One script, one job. This
is where every programmatically checkable rule lives. See `validation-pattern.md`.

## templates/
Files to copy into the artifact being produced and then fill in. A template is
inert: it is not run and not read for knowledge, only duplicated and edited.
Keep placeholders obvious.

## references/
Background knowledge the agent reads on demand: concepts, rules, rationale, lookup
tables. References are read, not run. This is where detail lifted out of the
router lands. Loaded only when the relevant path is taken.

## protocols/
Step-by-step workflows: the ordered procedures that tie everything together. A
protocol names the steps, points at the references for the why, the scripts for
the checks, and the agents for delegated work. Protocols are the spine.

## Deciding where something goes
- Is it run? -> `scripts/`.
- Is it delegated to a subagent? -> `agents/`.
- Is it copied and filled? -> `templates/`.
- Is it read to learn? -> `references/`.
- Is it an ordered procedure? -> `protocols/`.

If a piece seems to fit two folders, split it: the runnable part is a script, the
explanation is a reference, the procedure that uses both is a protocol.
