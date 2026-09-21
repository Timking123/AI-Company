# AI-Company: Workflow

This document defines a protocol for one human owner to direct a large project through AI teams.
It provides instructions and templates; it does not supply a hosted service, scheduler, or isolation runtime.
Agents and humans must verify what their host supports. Following the protocol does not guarantee correct execution.
Use [role prompts](docs/ROLES.md) and [task templates](docs/TEMPLATES.md) with this workflow.

## 1. Authority and scope

- **MUST** means a requirement of this protocol. **SHOULD** means a default; record a concrete reason for departing from it.
- Agents MUST follow their host's instruction hierarchy, permissions, the owner's current instructions, and applicable project rules.
- Reading or copying this repository grants no authority to create tasks, edit a project, change user-wide settings, send messages, or deploy.
- The owner MUST appoint the project CTO or confirm an existing appointment before the CTO directs a team.
- Agents MUST reuse explicit current or continuing authorization. Reporting an authorized decision does not add another approval step.
- Research-only and review-first requests end at reviewable findings. Implementation requests continue through the authorized delivery boundary.
- Production, deployment, live providers, paid usage, credentials, real user data, and recurring execution require their own applicable scope.
- If a rule or permission conflicts, identify its source and pause only the affected action. Continue independent, authorized work.
- Small fixes and short questions SHOULD use one responsible agent when additional management would add no useful coordination.

## 2. One chain of responsibility

| Role | Owns | Direct relationship |
| --- | --- | --- |
| Human owner | Goals, consequential tradeoffs, acceptance expectations, authorization | Works with the CTO and leads |
| Project CTO | Project plan, direction ownership, shared design, priorities, integration order, project status | Manages leads; reports to the owner |
| Direction or team lead | A bounded direction, worker briefs, dependencies, review, delivery | Manages its workers; reports to the CTO |
| Worker | One verifiable assignment and its evidence | Reports to its creating lead or registered successor |

- A project MUST have exactly one active CTO and each worker MUST have exactly one direct dispatcher.
- The worker's creating lead remains its manager until a formal transfer takes effect under section 10.
- The owner SHOULD interact with the CTO and leads. Leads MUST relay relevant owner decisions to their workers.
- The CTO MAY inspect worker evidence read-only. It MUST route worker assignments and changes through the responsible lead.
- Workers MUST route dependencies and disagreements through their lead, without dispatching another team's workers.
- A reviewer or integrator is a worker role within this chain, not an additional management layer.
- A lead remains accountable for delivery after a worker submits a candidate; a submitted patch alone does not close the direction.

## 3. Bootstrap or resume

1. **Establish intent and authority.** Read the owner's request and applicable project rules. Identify the delivery boundary, required gates, and existing authorization. Separate missing permission from an ordinary implementation choice.
2. **Inspect the host.** Verify the capabilities below using available, authorized read operations. Record supported, unsupported, or unknown with the evidence and check time. Do not infer support from a tool name in a prompt.
3. **Find existing work.** List and read relevant tasks, ownership records, workspaces, branches, and deliverables. Reuse an existing CTO, lead, or worker where the same objective already has an owner. Resolve ambiguous appointments before conflicting dispatch.
4. **Choose one status source.** Reuse the project's existing authoritative registry. If none exists and project-file writing is authorized, the CTO SHOULD create `.ai-company/STATE.md`. Do not create a parallel status table elsewhere.
5. **Agree on the charter.** Record the goal, acceptance boundary, CTO and leads, exclusions, authorization, model policy, dependencies, and review/integration capacity. Link project contracts and required commands instead of copying them.
6. **Verify the baseline.** For Git work, inspect repository root, branch, status, and exact commit. The coordinator MUST assign a verified base and check any required governance or CI prerequisites at that commit. Preserve existing dirty work and its owner.
7. **Assign bounded work.** Leads check reuse, provide worker briefs, and reserve files and conflicting resources. New writable workers require separate worktrees and branches from the assigned base. Verify a clean starting tree unless an explicit preservation brief covers an existing dirty candidate.
8. **Create only authorized tasks.** Check existing task/request IDs before creating or retrying. Record asynchronous creation as `pending`. Read back the durable task and workspace before marking it `active`; a returned request ID alone is insufficient.
9. **Begin and observe.** Send the brief through an authorized channel, verify that the worker has its context, and track event-based updates. Before resuming, read the registry, applicable handoff, candidate identity, and actual task configuration again.

| Capability to check | Required evidence | If unavailable or unknown |
| --- | --- | --- |
| Durable tasks visible to the owner | A task survives a later read and appears in the host's task view | Use a declared manual workflow; do not claim a visible team exists |
| Task list and read | Existing task identity, owner, and current state can be inspected | Ask the owner for the missing record before duplicate-prone dispatch |
| Task send and wait/status | Authorized messages and completion/state events can be observed | Prepare a brief for human relay and record delivery as unconfirmed |
| Filesystem and workspace isolation | Allowed paths and separate working locations can be verified | Keep work read-only or serial in an authorized workspace |
| Git and a valid HEAD | Repository identity and an existing commit can be read | Use the non-Git rule below; do not invent a commit |
| Model/configuration inspection | Selected model, supported reasoning, and actual task settings | State what cannot be verified; do not claim a configuration change |

A manual workflow uses the same roles and evidence, with the human relaying briefs or opening tasks through supported UI.
Agents MUST label which steps need human action. They MUST NOT fabricate tool calls, successful sends, task IDs, or background execution.
Internal subagents MAY perform short, bounded assistance inside one visible task when authorized; disclose their lack of separate visibility.
They MUST NOT replace durable team tasks or create a hidden, persistent management tree.

When no Git repository or valid HEAD exists, agents MUST NOT initialize Git or manufacture a commit to satisfy this protocol.
Continue authorized read-only work or serial edits with explicit file ownership and a versioned artifact snapshot.
If parallel Git work is necessary, ask for the missing repository/baseline or explicit setup scope before proceeding with it.
Read-only tasks require neither empty branches nor artificial worktrees; their brief MUST still prohibit external side effects.

Ask the owner only when a missing fact changes scope, acceptance, consequential effects, or authority.
Examples include an ambiguous incumbent CTO, a required unavailable host capability, or an unprovided valid baseline needed for writable parallel work.
State the missing fact, the affected action, and the smallest decision needed. Reuse authorization already given and continue unaffected work.

## 4. Keep one project registry

The CTO MUST be the sole writer of the authoritative project registry, including task status and ownership allocations.
Leads include routine progress in delivery or necessary handoff summaries and MAY maintain detailed notes in their exclusively assigned paths. Workers return evidence to their lead.
Notes link to the registry; they MUST NOT become competing project-wide status sources.
Record material decisions and ownership changes when they take effect. Routine local steps do not require a message or registry transition each time.

The registry MUST contain, or link to, the following information:

- Project goal, completion boundary, acceptance requirements, authorization, and the current CTO.
- Lead ownership, worker/task identity, direct dispatcher, assigned objective, and a link to the brief.
- Allowed and prohibited paths, worktree, branch, assigned base, and current candidate or artifact identity.
- Shared-file and resource owners, including contracts, lockfiles, generated artifacts, ports, databases, and test slots where relevant.
- Dependencies as named deliverables with a producer, release condition, and consumer.
- Task status, delivery milestones, the next actionable step, evidence locations, and unresolved decisions.
- Configuration checks and transfers with timestamps, plus pending communication that affects commitments.

Keep sensitive operational records in the target project's approved private location.
Do not publish credentials, real user conversations, private task identifiers, or confidential paths in public examples.

| Task status | Responsible party | Evidence required before the CTO records it |
| --- | --- | --- |
| `planned` | Lead | Unique objective, owner, scope, acceptance, dependencies; no claim that a worker is running |
| `pending` | Creating lead | Authorized creation request and traceable request/task reference; readiness remains unverified |
| `active` | Worker under its lead | Readable task, accepted brief, manager, verified workspace/baseline and ownership; manual execution confirmed when applicable |
| `blocked` | Lead, with a named resolver | Observed blocker, affected actions, release condition, evidence, and independent work that can continue |
| `ready` | Lead | Identified candidate, completed agreed worker checks, risks, and explicit next review or integration owner |
| `done` | Lead accountable; CTO closes | Acceptance and all authorized delivery steps fulfilled, evidence read back, required handoff/archive completed |
| `stopped` | Lead accountable; CTO records | Explicit stop, cancellation, or experiment exit; preserved work and remaining scope; no claim of completion |

Normal progression is `planned` -> `pending` -> `active` -> `ready` -> `done`; reuse of a verified existing task may skip `pending`.
An active or ready task may become blocked. Resume it only after observing its release condition and rechecking the candidate and ownership.
If a candidate changes after `ready`, return it to `active` for applicable revalidation. Keep transition history sufficient to explain invalidated evidence.
Creation failures remain pending only while creation is unresolved; a confirmed obstacle requires a scoped blocked record.
The lead MUST NOT equate a sent message, elapsed time, or a child's completion with fulfilled project acceptance.

Track delivery as separate milestones in that same record: implementation, verification, integration, and deployment.
For each applicable milestone, record `not started`, `in progress`, `passed`, or `blocked`, its responsible party, and evidence.
Use `out of scope` only when the agreed charter excludes a milestone. A required step awaiting authorization remains `blocked`; it cannot be removed from acceptance by relabeling it.

## 5. Scope, reuse, and concurrency

- Before dispatch, leads MUST inspect relevant existing tasks, implementations, accepted designs, and known failed approaches.
- Assign one accountable execution owner per acceptance objective. Explain why an existing task cannot cover a proposed new task.
- Prefer extending an appropriate implementation. Parallel alternatives require a stated difference, owner, and retention or removal condition.
- A new framework, service, or abstraction MUST have a current consumer and evidence of a current need; document maintenance and rollback costs.
- An experiment MUST name the hypothesis, minimum test, time or usage cap, success/failure criteria, and exit condition before it starts.
- At the cap or hard stop, preserve findings and stop that experiment. More work requires a justified next step within authorization.
- A refactor or redesign MUST address an observed defect, acceptance requirement, or measured cost. Reopen settled choices only with new evidence.
- Parallel writable workers MUST have non-overlapping file ownership, independent worktrees and branches, satisfied prerequisites, and verifiable outputs.
- Leads that write or integrate need their own assigned writable workspace. Read-only managers do not need ceremonial development branches.
- Shared contracts and mainline integration MUST each have one writer. Agree on a contract before dependent implementation when the project requires it.
- Git worktrees do not isolate ports, databases, credentials, browser sessions, or generated outputs; reserve those resources as needed.
- The CTO MUST limit work in progress by review and integration capacity as well as independent work, machine resources, and host limits.
- Stop adding parallel tasks when review backlogs, rate limits, repeated failures, or integration congestion prevent useful progress.
- Preserve outputs before retiring redundant work. Never remove another task's workspace or overwrite its changes to simplify integration.

## 6. Communicate at decision points

Leads MAY contact other leads to confirm facts and negotiate handoffs within allocated scope.
They MUST record the responsible party and delivery condition, and inform the CTO of conclusions that affect the project.
Shared design, public contracts, ownership, cross-direction priorities, acceptance changes, and new shared capabilities require CTO resolution.
The CTO applies an explicit owner decision without requiring the owner or lead to approve it again.
Leads MUST continue to direct only their own workers after a cross-team agreement.

Workers report only to their direct lead: on completion, when a problem needs action above their authority,
or before they expect to exceed scope, budget, or a stop condition. They fix ordinary errors locally and retain the evidence in their task record.
Leads arrange independent review when risk or project requirements call for it, resolve matters within their direction, and report direction deliveries, matters requiring CTO decisions,
or requests for heavy operations under section 9. Reports include the observed result, evidence, affected scope, and any specific action needed.
Keep owner intent distinct from interpretation when reporting a decision. Required ownership and dependency handoffs still need confirmation.

Leads MUST report owner interactions that affect scope, priority, acceptance, authority, shared interfaces, or material risk to the CTO promptly and before closing the affected delivery.
Routine preferences, questions, and progress belong in delivery or necessary handoff summaries, not scheduled status messages. Preserve enough source context to avoid changing the owner's meaning.
Authorized work continues while the lead reports it. Unsettled cross-direction allocation pauses only affected actions.
A successful send proves delivery at most; it does not prove agreement, acceptance, or completed work.
Keep undelivered updates pending and check prior delivery before retrying. Do not send routine acknowledgments, relay unchanged reports,
or poll frequently for unchanged status. Prefer completion events and inspect status when an actual dependency or decision needs it.

## 7. Handle dependencies and blockers

- Name the producer, exact artifact or contract, expected version, release condition, and consumer; avoid “wait for the other team.”
- The receiving lead MUST inspect the artifact and acceptance evidence before releasing dependent work.
- Leads SHOULD resolve factual mismatches within existing scope, then escalate unresolved design or ownership conflicts to the CTO with options.
- For circular waits, the CTO assigns an initial contract or minimum shared deliverable and revises the dependency order.
- A blocked worker reports through its lead and continues independent authorized work. It MUST NOT widen scope or bypass a required gate.
- Retry only when new evidence or changed conditions justify it and the agreed limit permits it. Repeated failure is not evidence of success.
- If all remaining work needs an external condition, preserve results and report the exact blocker, resolver, and resume condition.

## 8. Verify, integrate, and close

1. The CTO defines the current delivery batch, its included tasks, acceptance, and closing stop condition. New requirements go into the next batch. If closure would exceed the stop condition, the CTO MUST explicitly defer affected work or adjust the batch within existing authorization; it cannot silently drop accepted scope or weaken a required gate.
2. Workers first run local unit tests and necessary targeted checks, then return their artifact, candidate identity, commands/results, evidence, and limitations. Leads check requirements and evidence and arrange independent review when complexity, risk, or project rules require it; a small fix does not automatically create a reviewer task.
3. The CTO reviews necessity, duplicate work, cross-direction effects, and delivery readiness during dispatch and candidate acceptance. Extra inspection responds to scope growth, duplication, repeated failures, or expected budget overruns. Do not create a periodic inspection timer or repeat the same review at each layer.
4. The CTO assigns one integration queue and one integration writer through the responsible lead. Combine all included tasks into one candidate, then run the batch's final full validation covering those tasks and their interactions under the approval in section 9. Do not run the entire project suite separately for each direction or wait for every future backlog item. Preserve project-required gates and repetitions.
5. Bind tests, review, and CI to the candidate and relevant configuration. For uncommitted work, record a reproducible snapshot. Before reusing evidence after a change, inspect code, dependencies, environment, configuration, tested scope, and mandatory gates. Record what remains applicable; satisfy required same-commit checks on the resulting candidate.
6. On failure, diagnose and fix with targeted checks first, then determine which final full checks need repeating and whether the approved budget covers them. Passing old evidence does not approve changed behavior.
7. Perform authorized delivery steps only after required tests, independent review, and CI pass. Report implementation, verification, integration, deployment, and observed product behavior separately.
8. The lead checks the completion boundary and handoff; the CTO closes the batch after reading the necessary evidence. Unrelated future work does not keep an accepted batch open.

For UI acceptance, evidence MUST identify the environment, page, candidate, and flow observed. Report visual, keyboard, accessibility, build, and business-flow coverage as applicable.
Use files, logs, and unit tests when they answer the acceptance question. Browser or desktop control and screenshots require a concrete visual or interaction need.
Collect traces, hashes, or additional encryption only for an identified diagnostic, integrity, or protection purpose. Preserve TLS, required security controls, and project quality gates.
Required live evaluations remain required when a provider or budget is unavailable; continue deterministic preparation and leave the gate open.
Agents MUST NOT substitute smoke tests, relax thresholds, conceal failures, or claim a blocked mandatory gate passed.
After suitable checks pass, repeat testing only for changed candidates, failures, project-required repetitions, or an unresolved concern.
Finish when the agreed acceptance, required review, applicable gates, authorized delivery, and necessary records are complete.
Stop at an explicit user stop or defined experimental limit; a blocker or stopped experiment does not mean the project is done.
Record optional improvements for later consideration instead of extending a completed scope without need.

## 9. Model and execution policy

The default policy is a frontier general-purpose or coding model with high supported reasoning for the CTO and leads.
The owner's explicit choice takes precedence. A lead selects worker models according to task difficulty, error impact, and required capabilities.
An optional quality-first policy uses the latest available flagship and highest supported reasoning after verifying the host and account.
Use a literal `ultra` setting only if the host supports it and the owner requests it; never invent a reasoning option.
At creation, transfer, or resume, check model availability and actual task configuration; record the model, reasoning setting, time, and any unverifiable part.
If a requested setting is unavailable, report the discrepancy and seek a decision only when no authorized fallback exists.
A policy file or requested setting does not prove a running task changed. Preserve work and use a supported handoff when changing execution settings.
This policy concerns development agents. It grants no authority to change product models, evaluation models, providers, or service channels.
Background recurrence requires explicit scope and supported scheduling; reading this workflow creates no timer or automatic continuation.

### Approve heavy operations once for their intended scope

Full-suite or multi-environment testing, large changes spanning modules, long scans, and bulk calls, downloads, or retries
MUST receive CTO approval before execution. This includes work triggered automatically by a push, pull request, or hook;
inspect those triggers before launching the initiating action. Count cumulative work for the same purpose across tasks and commands;
splitting it does not avoid approval. Unless an approved budget already covers it, the default escalation threshold is 15 minutes of expected
or actual cumulative operation time, adjustable by the CTO for the project. It is a management default, not a limit on ordinary coding or reading,
and it does not exempt fast full-suite tests or large changes.

Use one short paragraph in the existing brief or decision record: purpose, benefiting batch and tasks, why a smaller approach is insufficient,
expected time and other resources, scope and executors, maximum runs and concurrency, and stop conditions. Link the approval rather than
creating another approval application or status table. The CTO records the same necessity and budget for operations it initiates.
Existing approval remains valid within its scope and limits; seek another decision only for a material change or expected overrun.
CTO approval does not replace the owner's required authorization for spending, deployment, data, or other external effects.
For an authorized solo task with no appointed CTO, the responsible agent records the same necessity and limits within the owner's authority;
do not create a management layer merely to approve it. Ask the owner only for genuinely missing authority or a consequential decision.

If an operation starts outside its approval, preserve outputs and execution state, launch no additional work, and pause the affected operation
at a safe stopping point. Report through the lead with the work already done, remaining impact, and decision needed. Do not destroy evidence
or abruptly interrupt a write that needs a safe stop.

### Resume from observed state

Resume only after checking actual operations, completed effects, remaining scope, authorization, and budget. Keywords in a final reply do not
grant new authority or prove that retrying is safe. A custom Stop hook MUST NOT decide to repeat work from natural-language output alone.
Use only documented host capabilities; do not invent continuation fields or add a monitor to compensate for missing state.

## 10. Transfer ownership without two dispatchers

1. The appointing authority identifies the successor: the owner for a CTO change, or the CTO for a lead change. A worker/file transfer goes through its responsible lead and any shared-ownership decision goes through the CTO.
2. The predecessor preserves objectives, decisions, authorization, workers, workspaces, file/resource ownership, dependencies, candidate evidence, configuration, and next actions.
3. Confirm the predecessor stopped dispatching or writing the transferred scope. An unavailable task requires inspection of its runtime and filesystem state; silence or a timeout does not release ownership.
4. The successor reads the handoff and accepts the precise scope. Record an effective transfer and notify affected workers through authorized channels before dispatch resumes.
5. For a CTO transfer, the predecessor stops registry writes before the successor becomes its sole writer. For lead transfers, the CTO records the new dispatcher for the existing workers.
6. Workers verify the registered successor and preserve existing artifacts. Do not recreate tasks or copy whole workspaces to simulate a transfer.

If cessation or authority cannot be verified, pause conflicting dispatch and writes. Continue read-only preparation without claiming the transfer completed.

## 11. Retain useful knowledge within its scope

Leads and the CTO MAY write task notes or reference skills only within authorized, exclusively owned paths.
Notes SHOULD include scope, owner, date, evidence, open questions, and failed attempts; mark untested ideas as such.
Workers return lessons to their lead. Leads propose reusable methods after checking existing material and validating the applicable procedure.
The CTO decides whether a lesson remains a note, becomes a reference skill, updates project rules, or needs no further record.
Project rules require the project's authorized single writer; global rules and user-wide skills require separate applicable authorization.
Notes and skills grant no permission and do not override the owner's instructions, data contracts, or quality gates.
Keep the authoritative current state in the registry. Date historical snapshots and link to current evidence instead of duplicating status tables.
Respect consent, data minimization, and the target project's privacy rules. Do not convert private conversations into examples or training material without permission.
Document review proves document review only. Host loading, task messaging, configuration changes, and agent behavior each need their own observed evidence.
