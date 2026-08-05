# Protocol: create-skill

Context: the end-to-end workflow for building a new skill. It opens with
alignment, runs the PACT cycle (Prepare, Architect, Create, Test), wires the
skill to refine itself, and closes by packaging the artifact.

## Mission
Turn a rough skill idea into a complete, validated, packaged skill that satisfies
every best practice in `../references/best-practices.md`.

Every phase ends at a user gate: present the phase's output, get the user's
feedback, and incorporate it before the next phase begins. The user steers; no
phase runs to completion unattended, because a wrong assumption in an early phase
compounds through all the later ones.

## Steps

### 1. Align
Run `align.md` in full. It produces `skill-spec.md` and ends when the user
approves it in words.
**Gate:** you MUST NOT begin step 2 -- or create any directory, dispatch any
agent, or run `scaffold.py` -- until the spec has zero `UNRESOLVED` fields and
the user has approved it. Asking a few questions is not alignment; the approved
spec is.

### 2. Prepare
Dispatch the `../agents/skill-preparer.md` agent with the approved spec. It
researches the domain and returns a brief: domain facts, checkable rules, and
decomposition notes, grounded in the spec rather than in its own framing.
**Gate:** present the brief and resolve any question it raises against the spec.
If research contradicts something the spec asserts, take it back to the user and
amend the spec; NEVER let a phase quietly overrule what was agreed.

### 3. Architect
Dispatch the `../agents/skill-architect.md` agent with the spec and the brief. It
returns the file tree, per-file responsibilities, dependency map, and the scripts
to build. Review the design against `../references/folder-taxonomy.md` and
`../references/progressive-disclosure.md`, then seed the tree with
`../scripts/scaffold.py`.
**Gate:** present the design and get the user's approval before building.

### 4. Create
Dispatch the `../agents/skill-creator.md` agent with the approved design. It builds
every file from the templates: prompts follow `../references/prompt-structure.md`,
scripts follow `../references/validation-pattern.md`, the router stays slim, and
every protocol it writes ends with a `## Next` section naming what follows.
**Gate:** show the user what was built and incorporate their feedback before
testing.

### 5. Test
Dispatch the `../agents/skill-tester.md` agent. It runs `../scripts/validate_skill.py`
and the skill's own validators, walks the skill end to end -- actually dispatching a
subagent if the skill delegates to one -- and returns PASS or FAIL with defects.
Loop back to Create on FAIL until it passes.
**Gate:** share the results and get the user's sign-off that the skill does what
they wanted.

### 6. Wire self-refinement
Confirm the new skill ships its own self-refine protocol and refinement log.
scaffold.py seeds both from `../templates/self-refine.template.md` and
`../templates/refinement-log.template.md`, so the new skill can improve itself.
This capability is baked into the skills skill-crafter produces; skill-crafter
itself is author-controlled and does not refine itself.

### 7. Package
Run `package.md`. Build the `.skill` artifact with `../scripts/package_skill.py`,
round-trip it with `../scripts/verify_package.py`, and report the artifact path to
the user. This step is mandatory whenever the spec's Delivery field asks for an
artifact, and it is the last thing that happens -- you MUST NOT report the skill
as done before the verifier prints `INTACT`.

## Guidelines
- Pattern: stop at every gate. A short user check after each phase prevents a wrong
  assumption from being built on; skipping gates is how a skill ends up technically
  complete and useless.
- Pattern: keep the phases distinct. Align before research, research before design,
  design before build, build before test, test before package. Skipping a phase
  pushes its cost into a later one.
- Pattern: for a small skill, run the phases inline rather than dispatching four
  agents. The cycle, the gates, the alignment step, and the packaging step are all
  the same; the agents are for when isolation helps.
- Anti-pattern: passing a gate on your own confidence. The user's confirmation is
  the gate, not your sense that the output looks right.
- Anti-pattern: treating step 2 as harmless because it is "only research". Research
  is work done on an unagreed premise, and everything downstream inherits it.
- Anti-pattern: writing files during Align, Prepare, or Architect. Decisions first,
  files in Create -- the one exception is `skill-spec.md`, which is the decision.
- Anti-pattern: mixing write channels in Create. Author every file through one
  channel -- the editor or the shell, not both. The two are backed by paths that
  sync, and an editor write can fail to flush to the shell side that packaging zips
  from, shipping a truncated file the editor's own re-read still shows as whole.
- Anti-pattern: declaring done at a green validator. A validator reads the source;
  the user installs the artifact. Done is step 7 finished.

## Next
Step 7 hands off to `package.md`, which is terminal. When the artifact is verified
and delivered, this protocol is complete.
