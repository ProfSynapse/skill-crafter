# Skill best practices

The canonical principles skill-crafter encodes. Every skill it produces should
satisfy these, and skill-crafter itself is the reference implementation. Each
principle links to the reference that expands it.

## 1. SKILL.md is a slim router
The entry file states what the skill is, when to use it, and routes to the
folders. It does not hold the detail. Detail lives in `references/`, `protocols/`,
`agents/`, and loads only when the relevant path is taken. See
`progressive-disclosure.md`.

## 2. Modularize when a file grows too long
When SKILL.md (or any file) stops being scannable, run a SOLID/DRY pass: give
each piece one responsibility, lift it into its own file, replace it with a
pointer, and map the dependencies so nothing dangles. See `progressive-disclosure.md`
and `protocols/modularize.md`.

## 3. Break work into the standard folders
Most skills decompose into five component kinds:
- `agents/` subagent prompts for delegated work.
- `scripts/` CLI tools the agent runs.
- `templates/` files to copy and fill.
- `references/` background knowledge read on demand.
- `protocols/` step-by-step workflows.
Use only the folders a skill needs. See `folder-taxonomy.md`.

## 4. Validate what is mechanical and stable; let the model judge the rest
If a rule is mechanical and stable, write a check for it rather than trusting
prose: structured data shape, required fields, naming, enums, link integrity,
owned-domain math. But do not push judgment into code. The failure mode is
encoding a list of specific real-world things ("bad outlet names", "disallowed
phrases") into a validator -- it cannot generalize and it rots. When a rule needs
judgment, split by what each side is good at: put the rubric in a reference, have
the model apply it and emit a structured label, and let the script validate the
label's shape and tally it. No enumerated list of real-world things in either
direction. The skill ships the checks and the protocol runs them before declaring
done. See `validation-pattern.md`.

## 5. Scripts are CLI-first
Scripts expose a clear command-line interface (argparse, `--help`, exit codes),
generally in Python and stdlib-only so they run anywhere. The agent invokes a
documented command instead of writing fresh code each time. See
`validation-pattern.md` and `templates/script.template.py`.

## 6. Prompts follow a fixed structure
Agent and prompt files use these headings in order: Context, Mission,
Instructions, Format (optional, only when output has a required shape), and
Guidelines (patterns and anti-patterns). See `prompt-structure.md`.

## 7. Created skills are self-refining
A skill that skill-crafter produces can improve itself. At the end of a session
that used it, it analyzes what went well and what caused friction, gathers user
feedback where possible, applies the smallest durable fix, and records it in its
refinement log. This is instilled in produced skills via
`templates/self-refine.template.md`; skill-crafter itself is author-controlled and
does not self-refine.

## 8. Mandatory behavior lives in the numbered workflow
Any behavior that is mandatory under common conditions must live inside the
numbered workflow, phrased imperatively, at the point where the decision is made.
A base agent follows the steps top to bottom; an imperative exiled to a side
section (a Scale, Delegation, or Notes appendix) is read where the agent never
reaches it, and strengthening the wording there changes nothing. "Slim router"
means push *detail* down a level, not banish the critical conditional to a note.
If a skill delegates to subagents under common conditions, the dispatch
imperative goes in the workflow step, not an appendix. `validate_skill.py` warns
when MUST/ALWAYS/NEVER appears only outside the steps. See `prompt-structure.md`.

## 9. Verify the packaged artifact, not just the source
A structure-only pass on the source tree says nothing about whether the bytes
that shipped are intact. Skills are packaged by zipping the filesystem, and if the
authoring channel (editor) and packaging channel (shell) diverge, a file can ship
truncated while every source-side check passes -- worse, a truncated router is
shorter, which a length check reads as healthier. Markdown has no compile step, so
the corruption is silent. Before declaring done: write through one channel and
verify through the channel you package from. Round-trip the produced `.skill`
against source hashes and run completeness heuristics (non-empty, closed fences,
no mid-sentence end) on the shipped members. And run the skill at least once end to
end -- if it dispatches subagents, actually dispatch one and watch it work; valid
structure is not a working skill. See `validation-pattern.md` and `protocols/validate.md`.
