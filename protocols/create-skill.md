# Protocol: create-skill

Context: the end-to-end workflow for building a new skill. It runs the PACT cycle
(Prepare, Architect, Create, Test) and ends by wiring the skill to refine itself.

## Mission
Turn a rough skill idea into a complete skill that satisfies every best practice
in `../references/best-practices.md`.

Every phase ends at a user gate: present the phase's output, get the user's
feedback, and incorporate it before the next phase begins. The user steers; no
phase runs to completion unattended, because a wrong assumption in an early phase
compounds through all the later ones.

## Steps

### 1. Prepare
First interview the user about the skill they want: its purpose and trigger, the
real workflow it should support, what good and bad output look like, the
constraints, and what must or must not be in scope. Use AskUserQuestion for the
discrete choices and open questions for the rest. Then dispatch the
`../agents/skill-preparer.md` agent with those notes; it researches the domain and
returns a brief: purpose, in/out of scope, domain facts, checkable rules, and
decomposition notes.
**Gate:** present the brief, resolve its open questions, and get the user's
confirmation before any design begins.

### 2. Architect
Dispatch the `../agents/skill-architect.md` agent with the approved brief. It
returns the file tree, per-file responsibilities, dependency map, and the scripts
to build. Review the design against `../references/folder-taxonomy.md` and
`../references/progressive-disclosure.md`, then seed the tree with
`../scripts/scaffold.py`.
**Gate:** present the design and get the user's approval before building.

### 3. Create
Dispatch the `../agents/skill-creator.md` agent with the approved design. It builds
every file from the templates: prompts follow `../references/prompt-structure.md`,
scripts follow `../references/validation-pattern.md`, the router stays slim.
**Gate:** show the user what was built and incorporate their feedback before
testing.

### 4. Test
Dispatch the `../agents/skill-tester.md` agent. It runs `../scripts/validate_skill.py`
and the skill's own validators, walks the skill end to end, and returns PASS or
FAIL with defects. Loop back to Create on FAIL until it passes.
**Gate:** share the results and get the user's sign-off that the skill does what
they wanted before declaring it done.

### 5. Wire self-refinement
Confirm the new skill ships its own self-refine protocol and refinement log.
scaffold.py seeds both from `templates/self-refine.template.md` and
`templates/refinement-log.template.md`, so the new skill can improve itself. This
capability is baked into the skills skill-crafter produces; skill-crafter itself
is author-controlled and does not refine itself.

## Guidelines
- Pattern: stop at every gate. A short user check after each phase prevents a wrong
  assumption from being built on; skipping gates is how a skill ends up technically
  complete and useless.
- Pattern: keep the phases distinct. Research before design, design before build,
  build before test. Skipping a phase pushes its cost into a later one.
- Pattern: for a small skill, run the phases inline rather than dispatching four
  agents. The cycle and the gates are the same; the agents are for when isolation
  helps.
- Anti-pattern: passing a gate on your own confidence. The user's confirmation is
  the gate, not your sense that the output looks right.
- Anti-pattern: writing files during Prepare or Architect. Decisions first, files
  in Create.
- Anti-pattern: declaring done before the Test phase exits clean and the user has
  signed off.
