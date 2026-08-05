# Protocol: align

Context: phase 1 of every skill-crafter job, before research, before design,
before a single file of the target skill is written. It turns a rough request
into a written spec the user has explicitly approved. Every later phase reads
that spec as ground truth, so a guess made here is a defect shipped later.

## Mission
Reach documented, user-approved agreement on what the skill is and is not,
recorded in a spec file, before any other work begins.

## Steps

1. Create the spec file at `skill-spec.md` beside where the skill will live,
   copied from `../templates/skill-spec.template.md`. Fill in only what the
   user's opening request actually tells you and write `UNRESOLVED` in every
   other field. Do this first: alignment without a written artifact is a feeling,
   not a state, and a feeling cannot be approved or checked.
2. Interview the user until no field reads `UNRESOLVED`. Ask in small batches --
   two to four questions per turn, AskUserQuestion for discrete choices, open
   questions for the rest -- and write each answer into the spec as it arrives.
   You MUST resolve every field below before moving on:
   - **Trigger.** The situations that should invoke the skill, plus at least two
     nearby situations that must NOT invoke it.
   - **Workflow.** The steps a competent human takes today, in order.
   - **Inputs and outputs.** What the skill can count on receiving, what it must
     produce, and where the output lands.
   - **Good and bad.** One concrete example of good output and one of bad, in the
     user's own words. Ask for a real past example rather than inventing one.
   - **Constraints.** What it must never do; required or forbidden tools,
     formats, and conventions.
   - **Out of scope.** What this version deliberately does not cover.
   - **Done.** How the user will judge that the skill works.
   - **Delivery.** Where the skill lives and whether it ships as a packaged
     `.skill` artifact. This decides the final phase, so settle it now.
3. Resolve contradictions out loud. When two answers conflict, or an answer
   contradicts the workflow the user described, name the conflict and ask which
   wins. Never resolve it silently by picking the one you prefer.
4. Restate the whole spec back in your own words -- purpose, trigger, workflow,
   boundaries -- rather than pasting the file. A restatement the user corrects is
   the point of this step; a paste they skim proves nothing.
5. Present the spec and ask for explicit approval. Then STOP and wait for the
   user's reply. Until they approve in words, you MUST NOT dispatch an agent,
   run `scaffold.py`, create a directory, or write any file other than
   `skill-spec.md` itself. Research and scaffolding are building; starting them is
   how alignment gets skipped.
6. On requested changes, edit the spec, present it again, and STOP again. Repeat
   until the user approves. There is no change small enough to apply and proceed
   in the same turn.
7. On approval, note the approval in the spec's status line and hand the spec
   forward. It is now the contract every later phase is measured against; a
   change to it mid-build requires the user's say-so, not yours.

## Guidelines
- Pattern: ask about failures, not features. "What did the last bad version of
  this get wrong?" surfaces more of the real spec than "what should it do?"
- Pattern: batch questions. Twenty asked one at a time reads as an interrogation;
  the same twenty in batches of three reads as a conversation.
- Pattern: when the user says "you decide", write your decision into the spec as
  a decision and show it to them. A default they saw and let stand is alignment;
  a default they never saw is a guess.
- Anti-pattern: doing research to inform your questions. Research is the Prepare
  phase and it runs after approval. Reading the domain first anchors the
  interview on your framing instead of the user's.
- Anti-pattern: delegating this to a subagent. Alignment is a conversation with
  the user; a subagent cannot have it, and a subagent's summary of it is not
  agreement.
- Anti-pattern: treating a few answered questions as alignment. The gate is the
  spec with zero `UNRESOLVED` fields and the user's explicit approval, not the
  point where you feel you know enough to start.
- Anti-pattern: "I'll start the scaffolding while you think about it." The
  scaffolding encodes the design, and the design is what is not yet agreed.

## Next
When the user has approved the spec, return to `create-skill.md` step 2
(Prepare), or to `improve-skill.md` step 2 (Assess) if you are improving an
existing skill. Carry the approved spec into every phase that follows.
