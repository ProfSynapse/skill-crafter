# Protocol: create-skill

Context: the end-to-end workflow for building a new skill. It runs the PACT cycle
(Prepare, Architect, Create, Test) and ends by wiring the skill to refine itself.

## Mission
Turn a rough skill idea into a complete skill that satisfies every best practice
in `../references/best-practices.md`.

## Steps

### 1. Prepare
Dispatch the `../agents/skill-preparer.md` agent. It researches the domain and
returns a brief: purpose, in/out of scope, domain facts, checkable rules, and
decomposition notes. Resolve its open questions with the user before continuing.

### 2. Architect
Dispatch the `../agents/skill-architect.md` agent with the brief. It returns the
file tree, per-file responsibilities, dependency map, and the scripts to build.
Review the design against `../references/folder-taxonomy.md` and
`../references/progressive-disclosure.md`. Seed the tree with
`../scripts/scaffold.py`.

### 3. Create
Dispatch the `../agents/skill-creator.md` agent with the architecture. It builds
every file from the templates: prompts follow `../references/prompt-structure.md`,
scripts follow `../references/validation-pattern.md`, the router stays slim.

### 4. Test
Dispatch the `../agents/skill-tester.md` agent. It runs `../scripts/validate_skill.py`
and the skill's own validators, walks the skill end to end, and returns PASS or
FAIL with defects. Loop back to Create on FAIL until it passes.

### 5. Wire self-refinement
Confirm the new skill ships its own self-refine protocol and refinement log.
scaffold.py seeds both from `templates/self-refine.template.md` and
`templates/refinement-log.template.md`, so the new skill can improve itself. This
capability is baked into the skills skill-crafter produces; skill-crafter itself
is author-controlled and does not refine itself.

## Guidelines
- Pattern: keep the phases distinct. Research before design, design before build,
  build before test. Skipping a phase pushes its cost into a later one.
- Pattern: for a small skill, run the phases inline rather than dispatching four
  agents. The cycle is the same; the agents are for when isolation helps.
- Anti-pattern: writing files during Prepare or Architect. Decisions first, files
  in Create.
- Anti-pattern: declaring done before the Test phase exits clean.
