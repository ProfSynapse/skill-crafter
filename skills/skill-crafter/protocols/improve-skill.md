# Protocol: improve-skill

Context: the workflow for improving an existing skill a user points skill-crafter
at. Distinct from a skill's own self-refine loop: this is user-initiated and
operates on a target skill from the outside.

## Mission
Raise a target skill to the bar in `../references/best-practices.md` through the
smallest set of changes, prove the result with the validator, and ship the
repackaged artifact.

## Steps

### 1. Align
Run `align.md`, adapted to an existing skill: the spec you fill in describes the
change, not the skill from scratch. Capture, in the user's words:
- What prompted this. What is not working, where it falls short, and any concrete
  recent failures or friction.
- What is working well and must be preserved. These become do-not-break
  constraints and go in the spec's Constraints field.
- The desired outcome, and any scope limits or parts to leave untouched.
- Delivery: whether the improved skill is repackaged, and where the artifact goes.
**Gate:** you MUST NOT run the validator on the target, dispatch the improver, or
edit a file until the user has approved the spec. Diagnosing before agreeing on
the problem produces a plan that answers a question they did not ask.

### 2. Assess
Dispatch `../agents/skill-improver.md` with the approved spec and the target
skill. It runs `../scripts/validate_skill.py`, reads the skill against the
practices, and returns a prioritized plan that weighs the user's reported pain
above theoretical gaps and separates structural problems from local edits.
**Gate:** review the plan with the user before changing anything.

### 3. Re-architect (only if structural)
If the plan flags structural problems (a bloated router, a misplaced concern, a
missing validation layer), dispatch `../agents/skill-architect.md` to design the
target state and the moves to reach it. Skip this step for purely local fixes.

### 4. Apply
Dispatch `../agents/skill-creator.md` to apply the plan: modularize per
`modularize.md` where the router is too long, add the missing scripts per
`../references/validation-pattern.md`, and align prompts to
`../references/prompt-structure.md`. If self-refinement is missing, install it
from `../templates/self-refine.template.md` and `../templates/refinement-log.template.md`.

### 5. Test
Run `validate.md`: dispatch `../agents/skill-tester.md` and confirm the generic
validator and the skill's own validators exit clean. Confirm the changes resolved
the friction the user named in step 1, not just the validator's findings. Loop
back to Apply on any failure.

### 6. Package
Run `package.md` to rebuild and verify the artifact. An improved skill that was
never repackaged leaves the user running the old one; you MUST NOT report the
improvement as delivered until `../scripts/verify_package.py` prints `INTACT`.

## Guidelines
- Pattern: lead with alignment. A skill can pass every static check and still
  fail the user; their reported pain is the truest signal of what to fix.
- Pattern: treat the user's "what works" list as a constraint. Improving one thing
  must not regress what they rely on.
- Pattern: change the least that closes the gap. An improvement pass is not a
  rewrite.
- Anti-pattern: improving a skill into skill-crafter's image when its domain calls
  for something different. The practices are about structure, not sameness.
- Anti-pattern: declaring done before step 5 exits clean and step 6 has shipped.

## Next
Step 6 hands off to `package.md`, which is terminal. When the rebuilt artifact is
verified and delivered, this protocol is complete.
