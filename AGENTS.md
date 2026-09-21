# AI-Company: agent entry point

This repository is a workflow kit for a human-led AI engineering company.
Reading, reviewing, or cloning it does not authorize adopting it in another
project, creating tasks, changing global instructions, or performing external actions.

## Read in this order

1. Read this file and the user's current request.
2. Read [WORKFLOW.md](WORKFLOW.md) for the complete operating protocol.
3. Read your assigned role in [docs/ROLES.md](docs/ROLES.md).
4. Use [docs/TEMPLATES.md](docs/TEMPLATES.md) for a task or handoff that needs it.
5. Read [client compatibility](docs/COMPATIBILITY.md); use [docs/CODEX.md](docs/CODEX.md) for Codex-specific checks.
6. Check [docs/VALIDATION.md](docs/VALIDATION.md) before declaring adoption complete.

## If asked to adopt the workflow

- Respect host instruction priority, the user's intent, existing project rules,
  permissions, owners, and in-progress work.
- Identify the actual project, current CTO and leads, available task tools,
  repository state, and verification commands before changing anything.
- Establish one CTO per project. Reuse existing leads and worker assignments.
- Give every worker one lead and an exclusive write scope. Confirm real task
  identities and actual workspaces before marking tasks active.
- Let leads coordinate facts and in-scope handoffs; route shared decisions to
  the CTO. Report user decisions without adding duplicate approval.
- Use phase summaries and decision-point reports. Follow WORKFLOW sections 8–9
  for distinct review responsibilities, batch validation, heavy-operation approval,
  and resuming from observed state within the remaining budget.
- If persistent tasks or communication tools are unavailable, describe the gap
  and the smallest manual action. Do not invent commands or emulate a running team.
- Return the capability check, ownership map, and next executable steps first.
  Do not claim perfect replication, benchmark speedup, or production readiness.

## If maintaining this repository

- Keep all examples fictional and portable. Do not add private project names,
  local absolute paths, credentials, user conversations, or internal task IDs.
- Keep the two READMEs consistent. Preserve text alternatives for the diagrams.
- State the assumptions of every numerical illustration. Scheduled work,
  elapsed time, token usage, and cost are different quantities.
- Run `python scripts/validate.py` after edits. It checks the published kit's
  structure and links; it does not evaluate real agent behavior.
- Inspect README rendering and every changed image before publishing.
