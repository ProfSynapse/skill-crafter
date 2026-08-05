# Protocol: validate

Context: run this whenever a skill is built or changed, and as the core of the
PACT Test phase. It turns the validation scripts into a pass/fail gate, and hands
a clean skill to packaging.

## Mission
Confirm a skill satisfies the generic best practices and its own domain rules,
and leave it in a known-good state ready to package.

## Steps
1. Run the generic validator:
   `python ../scripts/validate_skill.py PATH_TO_SKILL`
   Resolve every ERROR (this includes markdown-completeness: empty file,
   unclosed code fence, mid-sentence end). Decide on each WARN -- the name/dir
   mismatch and non-standard-folder warnings are sometimes intentional; an
   imperative-outside-the-workflow warning usually means a mandatory rule needs to
   move into the numbered steps (see best-practices principle 8); a missing-`## Next`
   warning means a protocol dead-ends where the agent needs to be told what follows.
2. Run each domain validator the skill ships in its own `scripts/`. Confirm it
   exits non-zero on bad input and zero on good input, so the check is real.
3. If the router failed the length check, run `modularize.md`, then revalidate.
4. If any reference dangled, fix the link or restore the target, then revalidate.
5. Run the skill once end to end against its own protocols. If it dispatches
   subagents under common conditions, actually dispatch one on a realistic input
   and watch what it does -- a delegated step that is never exercised is untested.
6. Package and verify: this protocol is not finished at a green validator. When
   the validator exits 0 it prints the packaging command; run `package.md` now.
   You MUST NOT report a skill as validated-and-done before
   `../scripts/verify_package.py` prints `INTACT`, because every check above reads
   the source tree and none of them can see what actually shipped.

## Guidelines
- Pattern: treat a non-zero exit as a stop, not a note. A skill that ships failing
  checks teaches the agent to ignore checks.
- Pattern: read the printed `path:line: message` lines; they are written to be
  acted on directly.
- Pattern: read the validator's `NEXT:` line as an instruction, not a sign-off.
  It exists because "validated" is routinely mistaken for "delivered".
- Anti-pattern: a validator that exists but is never wired into a protocol. An
  unrun check is documentation, not validation.
- Anti-pattern: stopping at `VALID: 0 errors`. That is the midpoint of this
  protocol, not its end.

## Next
Go to `package.md` and build the verified artifact. If this run was the Test
phase of `create-skill.md`, report the verdict at that phase's gate first, then
package.
