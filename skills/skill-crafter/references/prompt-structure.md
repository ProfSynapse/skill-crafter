# Prompt structure

Every agent prompt and reusable prompt uses the same five headings, in order.
Consistency lets a reader (and the model) find each part fast, and keeps authors
from forgetting a part. The template is `templates/agent.template.md`.

## Context
The situation the agent is walking into: the project, the prior phase, what is
already known, what artifacts it can read. State facts, not backstory. The agent
should finish this section knowing where it stands.

## Mission
The single outcome the agent owns, in one sentence. One agent, one job. If you
need the word "and" to state the mission, consider two agents.

## Instructions
The ordered steps to carry out the mission, ending with a clear stop condition:
what "done" looks like and what to hand back. Number them. Keep each step an
action, not an explanation.

## Format (optional)
Include only when the output must follow a fixed shape: a schema, a heading
layout, a table, a return contract. Show the exact structure. Omit this section
entirely when output is free-form, rather than writing "no particular format".

## Guidelines
Patterns and anti-patterns, as a list:
- Pattern: a behavior that produces good results here.
- Anti-pattern: a tempting mistake and what to do instead.
Guidelines tune behavior; they are not new instructions. Anything mandatory
belongs in Instructions.

## Why this order
Context grounds the agent, Mission gives it the target, Instructions give the
path, Format constrains the output, Guidelines shape the judgment calls along the
way. Each section assumes the ones before it.
