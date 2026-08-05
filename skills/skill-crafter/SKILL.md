---
name: skill-crafter
description: Build, improve, modularize, and validate Claude Code skills the right way. Use when creating a new skill, improving or auditing an existing one, refactoring a SKILL.md that grew too long, or adding validation scripts. Encodes a slim-router, progressive-disclosure, PACT-driven approach and is its own reference implementation.
---

# Skill Crafter

Context: a meta-skill for building and improving other skills. It encodes a set
of best practices and demonstrates every one of them in its own structure. You
reason through the work; the scripts verify what is checkable. The principles
every skill should satisfy live in `references/best-practices.md`.

## Workflow
1. Read the protocol for the job before doing anything else, and follow it step
   by step. This router names the protocols; it does not summarize them, and a
   summarized workflow is one you will improvise.
   - New skill: `protocols/create-skill.md`
   - Existing skill to improve: `protocols/improve-skill.md`
   - A SKILL.md that outgrew a slim router: `protocols/modularize.md`
   - A skill to check: `protocols/validate.md`
2. Align first, always. Every job begins at `protocols/align.md`, which ends at a
   written spec the user approves in words. You MUST NOT research, scaffold,
   dispatch an agent, or write a file before that approval.
3. Work the protocol's phases in order, stopping at each user gate.
4. Package last, always. Every job that produced or changed a skill ends at
   `protocols/package.md`. A validated skill that was never packaged is not
   delivered.

## Map
- `protocols/` the how: align, create-skill, improve-skill, modularize, validate,
  package. Each ends by naming the protocol that follows it.
- `references/` the why: best practices, progressive disclosure, folder taxonomy,
  prompt structure, validation pattern. Read on demand.
- `agents/` the workers: PACT (preparer, architect, creator, tester) plus improver.
  Dispatched from within a protocol, never instead of one.
- `scripts/` CLI tools: `scripts/scaffold.py` to generate a skill,
  `scripts/validate_skill.py` to check structure and completeness,
  `scripts/package_skill.py` to build the `.skill` artifact, and
  `scripts/verify_package.py` to round-trip that artifact against source.
  Run them, do not reimplement.
- `templates/` files to copy: skill spec, SKILL, agent, protocol, reference,
  script, plus the self-refine protocol and refinement-log that make a produced
  skill self-refining.
