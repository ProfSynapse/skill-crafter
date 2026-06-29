# Protocol: validate

Context: run this whenever a skill is built or changed, and as the core of the
PACT Test phase. It turns the validation scripts into a pass/fail gate.

## Mission
Confirm a skill satisfies the generic best practices and its own domain rules,
and leave it in a known-good state.

## Steps
1. Run the generic validator:
   `python ../scripts/validate_skill.py PATH_TO_SKILL`
   Resolve every ERROR (this now includes markdown-completeness: empty file,
   unclosed code fence, mid-sentence end). Decide on each WARN -- the name/dir
   mismatch and non-standard-folder warnings are sometimes intentional; an
   imperative-outside-the-workflow warning usually means a mandatory rule needs to
   move into the numbered steps (see best-practices principle 8).
2. Run each domain validator the skill ships in its own `scripts/`. Confirm it
   exits non-zero on bad input and zero on good input, so the check is real.
3. If the router failed the length check, run `modularize.md`, then revalidate.
4. If any reference dangled, fix the link or restore the target, then revalidate.
5. Package the skill, then verify the artifact, not just the source:
   `python ../scripts/verify_package.py --source PATH_TO_SKILL --package PATH_TO.skill`
   This round-trips the shipped bytes against source hashes and re-runs the
   completeness checks on the packaged members. A truncated file passes every
   structure check above but fails here. Resolve every ERROR.
6. Run the skill once end to end against its own protocols. If it dispatches
   subagents under common conditions, actually dispatch one on a realistic input
   and watch what it does -- a delegated step that is never exercised is untested.
7. Declare done only when both validators and `verify_package.py` exit 0 and the
   end-to-end run (including any subagent dispatch) behaved as intended.

## Guidelines
- Pattern: treat a non-zero exit as a stop, not a note. A skill that ships failing
  checks teaches the agent to ignore checks.
- Pattern: read the printed `path:line: message` lines; they are written to be
  acted on directly.
- Anti-pattern: a validator that exists but is never wired into a protocol. An
  unrun check is documentation, not validation.
