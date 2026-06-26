# Protocol: modularize

Context: run this when a SKILL.md (or any file) has grown past the point of being
a slim router, flagged by the length check in `../scripts/validate_skill.py` or by
the signals in `../references/progressive-disclosure.md`.

## Mission
Restore the router to a table of contents by lifting detail into focused files,
without breaking any dependency.

## Steps
1. List every distinct responsibility currently living in the bloated file.
2. For each, decide its destination folder using `../references/folder-taxonomy.md`:
   runnable -> scripts, delegated -> agents, copyable -> templates, knowledge ->
   references, procedure -> protocols.
3. Move each responsibility into its own file (one responsibility per file).
4. Replace the moved content in the router with a single pointer to the new file.
5. Map dependencies: update every link that referenced the moved content, and
   confirm nothing now points at a section that no longer exists.
6. Run `../scripts/validate_skill.py` to confirm the router is under threshold and
   no reference dangles.

## Guidelines
- Pattern: split by responsibility, not by length. Cutting a file in half at an
  arbitrary line leaves two half-thoughts.
- Pattern: leave the pointer where the content was, so the router still reads in
  order.
- Anti-pattern: moving content but forgetting the inbound links, which turns a
  long file into a broken one.
