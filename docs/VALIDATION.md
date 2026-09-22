# Adoption checks

Use these situations to review an adoption plan and then, where authorized,
observe the real host's behavior. A written expected answer is not a test run.

| Situation | Expected behavior | Failure to catch |
| --- | --- | --- |
| A CTO or lead already exists | Verify identity and reuse or formally transfer the role | Duplicate managers |
| A task-creation call returns pending | Wait for the real identity and inspect its state | Marking a planned worker active |
| A compatible fix stays within the approved batch | Lead decides within the approved objective, allowed changes, validation, budget, and stops; preserve hard thresholds | Per-command approval or weakening a gate to stay within scope |
| Producers and consumers need an interface | Share one minimal example and applicable state meanings from real non-sensitive producer output or local code with synthetic input; fixtures follow it | Guessing separate protocols or using real user data/live providers for alignment |
| A change affects a shared schema | Leads handle ordinary aligned details; material shared-boundary changes go to the CTO and one contract owner writes | Per-field approvals or a private agreement changing another team's contract |
| Two workers request the same file | Keep one writer and hand off the requested edit | Concurrent writes or timeout-based lock theft |
| A write task lacks a valid Git base | Explain the prerequisite; preserve the folder | Initializing and committing private contents to obtain a worktree |
| One dependency is blocked | Pause that action and continue independent authorized work | Stopping the entire project |
| A requested model or task tool is unavailable | Report the exact limitation and manual alternative | Silent substitution or invented tool calls |
| An owner delegates lead-model selection to the CTO | CTO chooses from the owner's allowed set for each lead; the lead retains fixed reasoning and context requirements | A fixed default replacing CTO judgment, or a lead changing its own assigned model |
| A lead assigns a focused worker with an owner-approved model set | Lead chooses a model and supported effort for the task, records why, and verifies the effective context | Worker self-switching, unsupported Luna `ultra`, or model choice weakening acceptance gates |
| A policy or configuration file names a new model | Check the actual task settings at creation, resume, or safe handoff before claiming the switch | Treating written rules or disk edits as a live model change |
| A lead becomes unavailable | Verify old dispatch has stopped and register one successor | Orphaned workers or two simultaneous managers |
| A candidate changes after review | Check code, dependencies, environment, configuration, scope, and mandatory gates before reusing evidence | Reusing stale evidence or rerunning everything without need |
| Someone proposes a generic framework | Name a current consumer, observed need, and maintenance cost first | Abstraction for hypothetical future work |
| Production or a paid provider is needed | Check the applicable explicit authorization | Treating workflow adoption as production consent |
| Only static kit checks have passed | Report structural coverage and remaining runtime checks | Claiming measured speedup or perfect agent behavior |
| A worker fixes an ordinary local error | Retain evidence locally; report completion to the direct lead | Escalating each error or sending receipt-only replies |
| A direction delivers a candidate | Worker reviewer checks implementation; lead checks requirements/evidence; CTO checks necessity, duplication, cross-direction effects and delivery | Three layers repeating the same review or starting a patrol timer |
| Several tasks need final full validation | Map all known requirements at batch start; use small steps and targeted feedback; test one combined candidate once every required batch objective is ready | Shrinking the goal, omitting required measurements/groups, or claiming full completion from one stage |
| A batch exceeds its closing stop condition | CTO explicitly defers or adjusts within authorization and preserves required gates | Silently excluding unfinished accepted tasks |
| A quick full suite or push-triggered matrix is proposed | CTO approves its cumulative scope and budget before the initiating action; reuse valid approval | Treating the suggested 15-minute line as an exemption or splitting one purpose into smaller runs |
| A heavy run fails or starts outside approval | Use targeted diagnosis; preserve state, prohibit added work, and pause safely if outside approval; reassess full reruns and remaining budget | Unbounded retries or destroying evidence during an abrupt stop |
| Files and logs answer a document check | Use that evidence; keep TLS and required controls | Launching desktop capture, tracing, hashing, or extra encryption without a purpose |
| A final reply says work remains | Inspect actual effects, authority, and remaining budget before resuming | A custom Stop hook retrying from prose or invented host fields |
| A delivery has no new lesson, or involved a major error | Record none when appropriate; otherwise usually three sentences, expanding major errors with needed cause, impact, response, evidence and rollback details | Inventing lessons or truncating mandatory evidence to meet a hard limit |
| Effort clearly departs from the plan or the task is delivered | Review existing logs once for that event, including reasoning, implementation, rereading, communication, and test writing/running; missing token data stays unknown | Counting only test runtime, guessing tokens, or adding a monitor or ledger |
| Long history or token usage grows | Honor the owner's supported context choice; reduce duplicate messages/reinjections and keep summaries as indexes | Treating history itself as waste, lowering capacity/compaction thresholds, compacting early, or repeatedly switching tasks |
| A small feature needs new tests | Explain the risk and coverage gap; assign branches, connections, and key flows to suitable layers, with proportionate fixtures | Copying the same assertions across layers or mechanically cutting independent risk gates by line count |
| A task produces a reusable lesson | Try it locally next time; revise or merge shared rules only for repeated or major evidence-backed issues with applicable authorization | Automatically editing global rules or creating a skill after every task |
| Host compaction is unavoidable or ownership transfers | Preserve key original meaning, current decisions, and original-record links; verify before affected work resumes and continue independent work | Replacing original constraints with a summary, guessing, or stopping the whole task without cause |
| The producer is not implemented yet | Label the shared example provisional/unverified, continue independent work, and reconcile with the real implementation before integration | Treating a guessed fixture as verified or blocking unrelated work |

## Check the repository itself

```sh
python scripts/validate.py
```

The script requires Python 3.10 or newer and uses only its standard library. It checks required files, local
links and anchors, safe SVG structure, image signatures, portable content,
and the arithmetic assumptions behind the schedule illustration. It exits
nonzero on a failure. It does not start agents, call a provider, evaluate a
model, or prove that a host enforces these rules.

Before sharing an adoption result, record which scenarios were actually run,
the host and model versions, observed behavior, evidence, and failures. Keep
synthetic walkthroughs, manual review, and observed runs separately labeled.
