---
name: skill-crafter
description: Build, improve, modularize, and validate Claude Code skills the right way. Use when creating a new skill, improving or auditing an existing one, refactoring a SKILL.md that grew too long, or adding validation scripts. Encodes a slim-router, progressive-disclosure, PACT-driven approach and is its own reference implementation.
---

# Skill Crafter

Context: a meta-skill for building and improving other skills. It encodes a set
of best practices and demonstrates every one of them in its own structure. You
reason through the work; the scripts verify what is checkable. The seven
principles every skill should satisfy live in `references/best-practices.md`.

## Create a new skill
Follow `protocols/create-skill.md`, which runs the PACT cycle:
1. **Prepare** research the domain via `agents/skill-preparer.md`.
2. **Architect** design the tree and dependency map via `agents/skill-architect.md`.
3. **Create** build the files via `agents/skill-creator.md`.
4. **Test** validate via `agents/skill-tester.md` and `protocols/validate.md`.

Every skill it produces is wired to refine itself, using the self-refine and
refinement-log templates.

## Improve an existing skill
Point at the target skill and follow `protocols/improve-skill.md`: assess it
against the practices with `agents/skill-improver.md`, apply the fixes, and
re-test.

## Single tasks
- `protocols/modularize.md` to split a SKILL.md that grew past a slim router.
- `protocols/validate.md` to check a skill against the rules.

## Map
- `references/` the why: best practices, progressive disclosure, folder taxonomy,
  prompt structure, validation pattern. Read on demand.
- `protocols/` the how: create-skill, improve-skill, modularize, validate.
- `agents/` the workers: PACT (preparer, architect, creator, tester) plus improver.
- `scripts/` CLI tools: `scripts/scaffold.py` to generate a skill,
  `scripts/validate_skill.py` to check one. Run them, do not reimplement.
- `templates/` files to copy into a new skill: SKILL, agent, protocol, reference,
  script, plus the self-refine protocol and refinement-log that make a skill
  self-refining.
