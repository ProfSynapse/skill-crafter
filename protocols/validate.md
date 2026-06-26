# Protocol: validate

Context: run this whenever a skill is built or changed, and as the core of the
PACT Test phase. It turns the validation scripts into a pass/fail gate.

## Mission
Confirm a skill satisfies the generic best practices and its own domain rules,
and leave it in a known-good state.

## Steps
1. Run the generic validator:
   `python ../scripts/validate_skill.py PATH_TO_SKILL`
   Resolve every ERROR. Decide on each WARN (the name/dir mismatch and
   non-standard-folder warnings are sometimes intentional).
2. Run each domain validator the skill ships in its own `scripts/`. Confirm it
   exits non-zero on bad input and zero on good input, so the check is real.
3. If the router failed the length check, run `modularize.md`, then revalidate.
4. If any reference dangled, fix the link or restore the target, then revalidate.
5. Declare done only when the generic validator and every domain validator exit 0.

## Guidelines
- Pattern: treat a non-zero exit as a stop, not a note. A skill that ships failing
  checks teaches the agent to ignore checks.
- Pattern: read the printed `path:line: message` lines; they are written to be
  acted on directly.
- Anti-pattern: a validator that exists but is never wired into a protocol. An
  unrun check is documentation, not validation.
