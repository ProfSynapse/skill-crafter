# Skill Crafter

A meta-skill for building and improving Claude Code skills the right way. It
encodes a set of authoring best practices and demonstrates every one of them in
its own structure, so it is also a worked example of a well-formed skill.

Version 0.1.1.

## What it does
- **Create** a new skill from a rough idea, through a gated PACT cycle
  (Prepare, Architect, Create, Test).
- **Improve** an existing skill: interview the user, assess it against the
  practices, apply the smallest fixes, and re-test.
- **Validate** any skill against the universal structural rules with one CLI.

You reason through the work; the scripts verify what is checkable. Every phase is
gated on user feedback, so the build stays steerable.

## The practices it encodes
1. SKILL.md is a slim router; detail lives in folders and loads on demand.
2. Modularize when a file grows past a router (SOLID/DRY, map dependencies).
3. Decompose into the standard folders: agents, scripts, templates, references,
   protocols.
4. Validate what is mechanical and stable with a script; for judgment, the model
   emits a label against a rubric and the script checks the label.
5. Scripts are CLI-first (Python, stdlib, argparse, exit codes).
6. Prompts follow Context, Mission, Instructions, Format, Guidelines.
7. Created skills are self-refining.
8. Mandatory behavior lives in the numbered workflow, not a side section.
9. Verify the packaged artifact, not just the source, and run it end to end.

The canonical statement lives in [references/best-practices.md](references/best-practices.md).

## Structure
```
skill-crafter/
├── SKILL.md          slim router
├── protocols/        create-skill, improve-skill, modularize, validate
├── references/       best-practices, progressive-disclosure, folder-taxonomy,
│                     prompt-structure, validation-pattern
├── agents/           skill-preparer, skill-architect, skill-creator,
│                     skill-tester, skill-improver
├── scripts/          scaffold.py, validate_skill.py, verify_package.py
└── templates/        SKILL, agent, protocol, reference, script,
                      self-refine, refinement-log
```

## Usage
Inside Claude Code, invoke the skill and describe what you want:
- "Build a skill that ..." runs [protocols/create-skill.md](protocols/create-skill.md).
- "Improve this skill: ..." runs [protocols/improve-skill.md](protocols/improve-skill.md).

### Scripts (CLI)
```bash
# Generate a new skill's structure from the templates
python scripts/scaffold.py my-skill --description "Do X when Y." --path ../skills

# Validate any skill directory against the universal rules
python scripts/validate_skill.py path/to/skill

# Verify a packaged artifact against its source (run after packaging)
python scripts/verify_package.py --source path/to/skill --package dist/skill.skill
```
`validate_skill.py` checks frontmatter (kebab-case name, description), keeps the
router under the length threshold, confirms every local reference resolves, and
flags truncated files and imperatives stranded outside the workflow.
`verify_package.py` round-trips the shipped `.skill` against source hashes so a
truncated member cannot pass silently. Per-skill domain checks are written by each
skill; see [references/validation-pattern.md](references/validation-pattern.md).

## Install
Unpack the release artifact so the `skill-crafter/` directory sits in your skills
location (for example `~/.claude/skills/skill-crafter/`):
```bash
unzip skill-crafter-0.1.1.skill -d ~/.claude/skills/
```
Then start a session and the skill is available.

## Self-refinement
skill-crafter is author-controlled and does not refine itself. The skills it
produces are born self-refining: each ships a `self-refine` protocol and a
`refinement-log`, so it improves from use. See
[templates/self-refine.template.md](templates/self-refine.template.md).
