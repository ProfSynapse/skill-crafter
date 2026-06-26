# Progressive disclosure

The organizing idea behind a skill. Only the SKILL.md description sits in context
permanently. Everything else loads when the agent actually walks that path. A
good skill front-loads almost nothing and reveals detail on demand.

## The router contract
SKILL.md answers three questions and nothing more:
1. What is this skill?
2. When should it trigger? (the `description` frontmatter is the real trigger)
3. Where is the detail? (links into the folders)

If a reader has to scroll the router to find the actual procedure, the router has
absorbed detail that belongs in a `protocols/` or `references/` file.

## When to modularize
Watch for these signals that a file has stopped being a router:
- It explains *how* to do something rather than *where* the how lives.
- A single section could stand alone as its own document.
- You scroll to navigate it.
- Two unrelated concerns share the file.

The `scripts/validate_skill.py` length check turns the first signal into a
mechanical threshold so the decision is not left to taste alone.

## How to modularize (SOLID/DRY for prose)
1. Name each distinct responsibility in the bloated file.
2. Give each its own file in the right folder (one responsibility per file).
3. Replace the lifted content with a one-line pointer to the new file.
4. Map dependencies: confirm every pointer resolves and nothing references a
   section that moved. Run the validator.
5. Re-read the router. It should now read as a table of contents, not a manual.

See `protocols/modularize.md` for the step-by-step version.

## Depth, not breadth
Prefer a shallow router that points to focused files over a deep router that
inlines everything. The cost of an extra file is near zero; the cost of a context
window full of detail the agent did not need is real.
