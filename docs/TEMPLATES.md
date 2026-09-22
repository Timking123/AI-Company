# Coordination templates

Use these fields with [WORKFLOW.md](../WORKFLOW.md) and the [role prompts](ROLES.md).
Fill only relevant fields; a short task can use a few lines. These are copyable briefs, not a requirement to open six documents.
Keep one authoritative project registry, preferably the existing one or `.ai-company/STATE.md` with authorized creation.
The CTO alone writes that registry. Leads submit phase summaries and keep detailed notes only in their assigned locations.
Link existing decisions, contracts, and evidence instead of maintaining duplicate status tables. Keep private operational details out of public examples.

## Project charter and registry entry

- Project and owner: [project name; human owner]
- Objective and completion boundary: [observable outcome; where authorized delivery ends]
- Acceptance and required gates: [criteria; project rule/contract links; evidence required]
- Delivery batch: [one approval of objective, allowed changes, necessary validation, budget and stops; included tasks/interactions; next-batch backlog link]
- Coverage in this record: [all known requirements -> owner and acceptance evidence; applicable user capabilities, producers/consumers, persistence/failures, measurements, integration, validation, deliverables, external dependencies]
- Excluded scope: [work and external effects outside this assignment]
- Authorization: [source; allowed edits, task creation, messages, Git delivery; separately scoped deployment, providers, spending, data, recurrence]
- CTO and appointment: [one responsible task; authority; effective time]
- Directions and leads: [bounded objective and accountable lead for each direction]
- Authoritative registry: [one existing entry point or approved project-local file]
- Host capability check: [time; visible durable tasks/list/read/send/wait; filesystem/Git/configuration; supported, unsupported, or unknown with evidence]
- Manual steps: [unsupported operations; human action or authorized serial alternative]
- Model policy: [owner choice or default; actual models/reasoning; verification time; authorized fallback]
- Existing work and reuse: [tasks/artifacts to continue; duplicate work avoided; unresolved ownership]
- Baseline: [verified repository and exact assigned commit; required base checks; or explicit non-Git artifact snapshot]
- Ownership and capacity: [shared-file/resource owners; integration writer; review capacity and WIP limit]
- Dependencies and next action: [producer; deliverable/version; release condition; receiving owner]
- Decisions and stop conditions: [open issue; decision owner; experiment cap or external condition]

For each registered task, keep one row or short entry with:

| Task | Manager | Brief / ownership | Status | Next action / resolver | Candidate / evidence |
| --- | --- | --- | --- | --- | --- |
| [readable name and private task reference] | [one lead] | [brief; worktree/branch/file/resource allocation] | [planned/pending/active/blocked/ready/done/stopped] | [action and owner; release condition if blocked] | [commit or snapshot; evidence link] |

Add milestone fields to that same entry: implementation, verification, integration, deployment.
For each, give its status, owner, and evidence; use `out of scope` when the charter excludes it.
For `pending`, retain the creation reference and readback status so a retry does not create a duplicate task.
Leads decide compatible fixes within the approved batch. Reopen approval only for material changes to goals, shared contracts or ownership,
permissions, risk, or budget, while preserving hard thresholds and required external authorization. Do not seek approval for each command.
Use a few lines for short tasks; do not add a questionnaire or shrink the agreed goal to fit a minimal solution. Complete goal alignment permits
small implementation steps and targeted feedback. Reassess new requirements within authorization rather than silently changing the batch.

## Worker brief

- Assignment and manager: [one verifiable outcome; creating lead or registered successor]
- Appointment and context: [role; project rules, registry, relevant decisions, existing work]
- Acceptance and deliverables: [what the lead will inspect; artifact location; authorized closure boundary]
- Allowed scope: [exclusive files; permitted reads and writes; permitted external actions]
- Prohibited scope: [other owners' files; protected configuration/data; external side effects]
- Workspace and baseline: [worktree; branch; exact assigned base; clean-start evidence or explicit preservation brief]
- Non-Git or read-only mode: [applicable alternative; content snapshot; no artificial branch or initialization]
- Dependencies and contracts: [producer/consumer; one shared minimal interface example and state meanings; verified or provisional source; artifact/version; release condition; contract owner]
- Resource ownership: [ports, databases, sessions, generated outputs, test slots as relevant]
- Reuse decision: [existing implementation/task; why this assignment is needed]
- Execution limits: [verified model/reasoning; allowed short internal assistance; experiment time/usage cap]
- Validation: [specific risk and existing coverage gap for added tests; suitable unit/integration/browser layer; necessary review; combined validation owner and required CI]
- Heavy operations: [existing approval link and remaining budget, including automatic triggers; or CTO decision needed before execution]
- Reporting and stop conditions: [direct lead; completion, needed higher-level action, or expected scope/budget/stop overrun; unaffected work]
- Return package: [candidate; changes; checks and evidence; risks; remaining work; dependency release; lessons]

For an experiment, include the hypothesis, minimum test, success/failure criteria, cap, and exit condition before starting.
For read-only work, prohibit edits, task creation, provider calls, and other external effects unless separately authorized.

## Phase summary or decision-point update

- Event: [direction delivery, decision needed, heavy-operation request, material owner instruction, or required handoff; time]
- Routing: [sender role; recipient role; related task and decision reference]
- Current decision or requested action: [specific choice; next owner; material impact or deviation]
- Necessary evidence: [links to observed result and full original; candidate and relevant limitations]
- Owner intent, when relevant: [faithful request/source, distinguished from interpretation]
- Delivery: [sent or pending; confirm receipt only when a handoff depends on it; prior-send check before retry]

Leads send material owner interactions to the CTO before the affected delivery closes. Update short handoffs at natural milestones;
use summaries as indexes to original constraints, decisions, and negative results. Honor the owner's context choice; long history or high token use
alone does not justify lower capacity or compaction thresholds, early compaction, or repeated task switching. Reduce duplicate messages and large reinjections.
For unavoidable compaction or formal transfer, preserve and verify key original meaning, current decisions, and original-record links before affected work resumes.
Workers report completion, problems needing higher-level action, or expected scope/budget/stop overruns only to their lead.
Fix ordinary errors locally and retain evidence. Do not send routine acknowledgments or unchanged relays.
Sending this update does not itself request another approval for an authorized owner decision.

## Heavy-operation decision paragraph

Use one paragraph in the existing brief or decision record, with the criteria in [WORKFLOW section 9](../WORKFLOW.md#9-model-and-execution-policy):

> To [purpose] for [batch and tasks], we need [operation] because [why a smaller approach is insufficient]. Expected resources: [time, calls, downloads, compute or cost as applicable]. Scope and executors: [included work and owners], including [automatic push/PR/hook effects]. Limits: [maximum runs, cumulative budget and concurrency]; stop at [failure, budget or safe stopping condition]. CTO decision: [approved scope or pending decision; owner authorization reference where separately required].

Reuse approval within its limits; request a new decision for material changes or expected overruns. The CTO records the same details for its own operations.
If execution starts outside approval, preserve state, start no additional work, pause safely, and report through the lead.

## Dependency handoff

- Producer and consumer: [responsible leads and tasks]
- Required deliverable: [artifact or contract; exact commit/version; approved location]
- Shared example: [actual non-sensitive producer output or local producer code with synthetic input; applicable fields/identity/version, success/error, initial/terminal, empty/not-run, apply semantics; no real user data or live providers]
- Release condition: [observable criteria the receiver must verify before dependent work begins]
- Evidence: [tests, review, relevant limitations; artifact readback]
- Ownership: [current file/resource owner; changes require formal transfer when applicable]
- Receiver result: [accepted or rejected; evidence; mismatch and resolver]
- Next action: [owner; sequencing; unaffected work that can proceed]
- CTO update: [material conclusion; unresolved shared-design, ownership, priority, or acceptance decision]

If the producer is not implemented, mark the example provisional/unverified, continue independent work, and assign reconciliation before integration.
Fixtures follow the shared contract and example. The responsible lead handles ordinary aligned details; material shared-boundary changes go to the CTO.

## Acceptance and delivery record

- Assignment and acceptance boundary: [brief link; accountable lead; authorized endpoint]
- Batch coverage: [each required objective from the initial coverage map and its evidence; included interactions; combined candidate; explicit deferrals or scope changes]
- Candidate identity: [repository/workspace; exact commit or reproducible content snapshot; configuration and time]
- Delivered changes: [artifact paths and observable behavior; deviations from the brief]
- Acceptance evidence: [criterion -> result -> evidence location]
- Validation: [local checks; final combined validation and approval; commands/exit codes; artifact readback; failures and limitations]
- Independent review: [reviewer; candidate reviewed; findings resolved or outstanding; applicable requirement]
- CI and integration: [same-commit checks; result; integration owner; resulting candidate and revalidation]
- Delivery milestones: [implementation / verification / integration / deployment, each with status, owner, evidence, or explicit out-of-scope reason]
- Remaining work and risks: [unfinished scope if this is a stage; mandatory gate still open; blocker and resolver; optional follow-up]
- Dependency release: [deliverable and condition; receiving lead's acknowledgment]
- Closure: [required archives/handoff; lead recommendation; CTO readback and final status]
- Total effort: [existing-log review at delivery or a clear deviation; reasoning, implementation, rereading, communication, test writing/running; token data or unknown]
- Lesson: [usually three sentences: largest avoidable waste; cause; one specific next-task change; or none]

For major errors, repeated failures, or complex handoffs, include the root cause, impact, response, evidence, and rollback details needed for the case.
Do not hard-limit length or omit required evidence. Keep the complete original in one place and link it; no new ledger or monitor is needed.
Apply ordinary lessons locally in the next task. Shared-rule changes need a repeated or major issue with clear evidence and the applicable writing authority.
Before reusing evidence, inspect code, dependencies, environment, configuration, tested scope, and mandatory gates.
After a failure, fix and check the affected path first, then decide which full checks need repeating within the approved budget.
Use unit tests for branches, integration tests for connections, and browser tests for key flows; avoid copying one assertion across layers or oversized fixtures.
Preserve independent risk gates and the agreed validation boundary; line count alone is not a reason to remove tests.
Use files, logs, and tests when sufficient; visual capture, traces, hashes, or additional encryption need an actual purpose.
If a required gate is blocked, keep it open and name the missing condition. Do not write “done” for a partially fulfilled boundary.

## Ownership and dispatcher transfer

- Transfer scope: [CTO, lead, worker, files, or resources; affected existing tasks]
- Authority and reason: [owner or CTO decision, or responsible lead for its bounded allocation; no timeout-based inference]
- Predecessor and successor: [one outgoing and one incoming owner; their verified task identities]
- Preserved context: [objective; decisions; authorization; workers; paths/resources; dependencies; models/configuration]
- Work and evidence: [candidate commits or snapshots; dirty state; tests/review/CI; remaining work]
- Cessation: [evidence the predecessor stopped dispatching and/or writing the transferred scope; unresolved runtime checks]
- Successor acceptance: [handoff readback; exact scope accepted; time]
- Effective record: [registry update and effective time; sole writer after a CTO transfer]
- Worker notice: [authorized delivery channel; affected workers' confirmation of their registered manager]
- Resume action: [new owner's next step; required revalidation; preserved limits]
- Incomplete transfer: [conflicting actions held; missing evidence; independent read-only preparation]

For a CTO transfer, the predecessor stops registry writes before the successor assumes them.
For a lead transfer, the CTO records the successor for existing workers before dispatch resumes.
