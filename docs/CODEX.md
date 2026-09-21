# Using AI-Company with Codex

Read [the protocol](../WORKFLOW.md) first. These notes describe the capabilities
to verify in your installed client. They do not install tools or change settings.

## Check what your host actually exposes

| Capability | What to establish |
| --- | --- |
| Persistent visible tasks | Can a lead create, identify, reopen, and inspect an independent task? |
| Task communication | Can managers send messages to the exact task and observe delivery or status? |
| Isolated checkouts | Can each independent write task use an appropriate Git worktree or equivalent isolated checkout? |
| Local files and Git | Can the task read its rules, verify its root and revision, and write only its assigned files? |
| Model configuration | Can the requested model and effort be selected and verified for the task? |

Use the actual tool catalog and installed client's documentation. Some clients
expose task-management tools that other clients do not. Do not copy internal
tool names from a screenshot, invent calls, or assume that an API example is a
callable desktop tool.

For large workstreams, prefer durable tasks the owner can inspect. Short-lived
subagents can help with a bounded search, test, or review inside a task. Tell the
owner when they are not separately visible. They do not replace the project's
persistent lead and worker records.

## Keep the existing project intact

Read the effective project rules and inspect current tasks before adopting a
new role. A worktree gives an independent checkout; it does not isolate shared
services, ports, databases, or all Git metadata. Register those resources when
they can conflict.

If a folder has no valid initial commit, do not initialize or commit its contents
just to obtain a worktree. Inspect it read-only, identify the actual code repository,
and explain what is needed before a write task can begin.

Prefer project-scoped adoption. Do not replace a user's global `AGENTS.md`, copy
personal credentials into a new worktree, or change model settings for the
application being developed. Put reusable instructions in the project's existing
rule entry point only when that write is authorized and the owner is known.

## If a capability is missing

List the missing capability and the affected action. The user can create tasks
or relay messages manually if that workflow is acceptable. Until then, keep the
dependent assignment pending and continue independent authorized work. Never
claim that a task, message, model change, or background monitor exists merely
because it appears in a plan.

## Model policy

Respect the user's explicit selection. A quality-first profile uses a current
flagship model and its highest supported reasoning setting for CTOs and leads;
workers use a model suited to their task. `ultra` is an example of a setting on
hosts that expose it, not a universal option. If a requested combination is
unavailable, report the mismatch rather than silently substituting it.

## Bound execution and continuation

Apply [WORKFLOW section 9](../WORKFLOW.md#9-model-and-execution-policy) before
heavy operations, including checks triggered by pushes, pull requests, or hooks.
Use a short CTO decision in the existing brief; do not install an approval app
or background monitor. Completion events and phase summaries normally supply
the coordination needed for a bounded task.

When adopting this policy in an authorized configuration scope, first remove
custom heuristic Stop continuation that retries from final-reply wording.
Natural-language output alone cannot establish which effects already happened,
whether a retry is safe, or whether budget remains. Check actual operations,
state, and authorization before resuming. Inspect the installed host's documented
hook support; do not invent fields, claim a universal Stop interface, or change
built-in safeguards. This note does not authorize global configuration edits.

Prefer file readback, logs, and targeted tests when they establish acceptance.
Use browser/desktop control and screenshots for a real visual or interaction
question; capture traces or hashes for a stated purpose. Keep TLS and required
security and quality gates.

## Authoritative references

- [Codex custom instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)

Consult current documentation when operating the tools. This kit is independent
of OpenAI and does not claim every Codex client implements the same task surface.
