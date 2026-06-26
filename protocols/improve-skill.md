# Protocol: improve-skill

Context: the workflow for improving an existing skill a user points skill-crafter
at. Distinct from a skill's own self-refine loop: this is user-initiated and
operates on a target skill from the outside.

## Mission
Raise a target skill to the bar in `../references/best-practices.md` through the
smallest set of changes, and prove the result with the validator.

## Steps

### 1. Interview the user
Before assessing anything, interview the user about the target skill. Their lived
experience is the primary guide; the static assessment that follows is the
secondary lens. Capture, in their words:
- What prompted this. What is not working, where it falls short, and any concrete
  recent failures or friction.
- What is working well and must be preserved. These become do-not-break
  constraints.
- The desired outcome, and any scope limits or parts to leave untouched.
Use AskUserQuestion for the discrete choices and open questions for the rest.
Carry these notes into every step that follows.

### 2. Assess
Dispatch `../agents/skill-improver.md` with the interview notes and the target
skill. It runs `../scripts/validate_skill.py`, reads the skill against the seven
practices, and returns a prioritized plan that weighs the user's reported pain
above theoretical gaps and separates structural problems from local edits. Review
the plan with the user before changing anything.

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
the friction the user named in the interview, not just the validator's findings.
Loop back to Apply on any failure.

## Guidelines
- Pattern: lead with the interview. A skill can pass every static check and still
  fail the user; their reported pain is the truest signal of what to fix.
- Pattern: treat the user's "what works" list as a constraint. Improving one thing
  must not regress what they rely on.
- Pattern: change the least that closes the gap. An improvement pass is not a
  rewrite.
- Pattern: get the assessment approved before applying, so the user steers the
  scope.
- Anti-pattern: improving a skill into skill-crafter's image when its domain calls
  for something different. The practices are about structure, not sameness.
- Anti-pattern: declaring done before the Test step exits clean.
