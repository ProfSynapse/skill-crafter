# Protocol: package

Context: the terminal phase of every skill-crafter job. A skill that validates
clean but was never packaged is not delivered -- it is a directory on someone's
disk. This protocol turns the validated source tree into a `.skill` artifact and
proves the shipped bytes match the source.

## Mission
Produce a verified `.skill` archive of the finished skill and hand the user the
artifact, so the work leaves the session as something installable.

## Steps
1. Confirm `validate.md` exited clean on the source tree. You MUST NOT package a
   skill with unresolved validator errors -- packaging a broken skill only makes
   the breakage portable.
2. Decide the artifact name and version with the user if this is a re-release;
   otherwise take the name from SKILL.md frontmatter and skip the version.
3. Build the archive:
   `python ../scripts/package_skill.py PATH_TO_SKILL --out dist [--version X.Y.Z]`
   Run the script; do not hand-roll a `zip` command. Ad-hoc zips sweep in `.git`,
   `__pycache__`, and the previous artifact, and they drift from the ignore rules
   the verifier uses.
4. Verify the artifact against the source:
   `python ../scripts/verify_package.py --source PATH_TO_SKILL --package dist/NAME.skill`
   This round-trips every shipped member against a source hash and re-runs the
   completeness heuristics on the packaged bytes. A file truncated by a
   divergence between the editor and the shell passes every source-side check and
   fails only here.
5. Resolve every ERROR, then delete the archive and repeat from step 3. Never
   patch an archive in place; rebuild it, so the artifact always corresponds to a
   source tree that passed.
6. Report to the user: the artifact path, its size, the file count, and the
   verifier's `INTACT` line. Name the artifact path explicitly -- "packaged
   successfully" without a path leaves them hunting for it.
7. If the skill lives in a repository, commit the source. Whether the `dist/`
   artifact is committed or ignored is the user's call; ask rather than assuming.

## Guidelines
- Pattern: package as soon as the validator is green, in the same turn. Packaging
  deferred to "after one more fix" is packaging that never happens.
- Pattern: treat `verify_package.py` as the definition of done. `package_skill.py`
  exiting 0 only means a zip was written, not that its contents are right.
- Anti-pattern: reporting a skill as finished because the validator passed. The
  validator reads the source; the user installs the artifact.
- Anti-pattern: skipping packaging because the skill "is already in the right
  folder". A local directory is a working copy; the artifact is the deliverable,
  and the spec's Delivery field says which the user asked for.

## Next
Nothing follows this protocol -- it is the terminal step. Confirm delivery with
the user, then, for a skill that ships its own self-refine protocol, offer to run
`self-refine.md` on the session that just produced it.
