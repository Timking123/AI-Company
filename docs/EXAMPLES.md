# Two fictional walkthroughs

All projects, tasks, and participants below are invented. These examples show
expected coordination, not recorded model runs or measured results.
Use them alongside the [workflow](../WORKFLOW.md) and [blank templates](TEMPLATES.md).

## 1. A booking portal with parallel work

**Goal:** add searchable bookings, a booking-detail view, and audit events to an
existing portal. Preserve its existing authentication and release process.

The owner approves the outcome. The CTO reads the existing project rules and
finds an active API lead and an active Web lead. It reuses both and asks one lead
to arrange independent acceptance review. It does not start another UI team.

The API lead identifies the existing booking service. The Web lead confirms
the response fields it already consumes. A new shared status field needs a
contract decision, so both leads send the CTO the alternatives and impact.
The CTO records the decision; the contract owner updates the contract first.

| Task | Manager | Exclusive write scope | Dependency |
| --- | --- | --- | --- |
| Search endpoint | API lead | Booking-search module and its tests | Approved response contract |
| Audit event | API lead | Booking-audit module and its tests | Approved event schema |
| Search interface | Web lead | Search-view module and its tests | Approved response contract |
| Detail interface | Web lead | Detail-view module and its tests | Approved response contract |

Each write task gets its own checkout and branch. The API lead owns the shared
API export file; workers return requested additions rather than editing it
concurrently. Work can now proceed in parallel against the approved contract.

The owner asks the Web lead to rename a filter. The lead records the request,
updates its own task brief, and reports the decision to the CTO without waiting
for a second approval. A separate request to change the shared status meaning
goes back to the CTO because it affects both teams.

Workers return exact candidates, test results, and remaining limitations. The
leads arrange independent review and return ready candidates. The integration
owner combines them in order and runs the project's required checks on the
resulting candidate. A failed integration check returns to the relevant lead;
it does not reopen unrelated research or trigger more workers.

The owner receives a delivery summary that distinguishes verified code from
deployment. Production remains subject to the project's existing authorization.

### A filled first checkpoint

Here are the blanks filled in. This separate rehearsal covers **booking search
only**, a first milestone within the larger portal idea. Detail views and audit
events remain future work; finishing this milestone would not finish that portal.
Two workers are plenty. The spare chairs can wait.

**Synthetic sample throughout:** the host, task states, candidates, messages, and evidence are invented. No client was tested and no commands ran.
Candidate names stand in for exact commits; a real adoption must record real
identities and observations instead of copying these labels into its evidence.

#### Owner brief: what “done” means this time

> Appoint Portal CTO to coordinate this milestone with API Lead and Web Lead.
> Let a signed-in user search by booking reference on the existing bookings page.
> Show matching bookings, an empty result, and a recoverable error state. Preserve
> authentication and keyboard access. Reuse the booking service and search component.
> You may create visible tasks, exchange manager messages, edit assigned files,
> run the existing checks, and deliver through branches, review, CI, and integration.
> Use synthetic fixtures. No deployment, live providers, paid services, credentials,
> real customer data, global configuration changes, or recurring execution.

The fictional project requires search tests, authentication regression, a build,
keyboard-flow acceptance, independent review, and its existing CI before integration.
There is capacity for two workers, one review at a time, and one integration writer.

#### Host check: assumed capable, never client-certified

This is what a filled report could look like on an **assumed capable host**.
“Sample checkpoint 1” is a story marker, not a recorded check time.

| Capability | Synthetic report at sample checkpoint 1 |
| --- | --- |
| Visible durable tasks; list/read | Assumed available; Portal CTO and both leads appear on a fresh read; existing work checked before creation |
| Send and wait/status | Assumed available; lead brief receipt and status events can be inspected through authorized channels |
| Filesystem and Git | Assumed available; existing repository, clean assigned checkouts, and `sample-base (fictional)` including the approved search contract |
| Model/configuration inspection | Assumed available; `sample-frontier-model (fictional)` with supported high reasoning for managers; product/evaluation settings unchanged |
| Missing capabilities | None assumed in this rehearsal; a real missing capability would be recorded as a manual step, not a fabricated success |

#### The CTO's first return: ownership, state, and the next move

All paths in this rehearsal are relative to an imaginary common parent:
`./AI-Company/` contains the playbook, `./booking-demo/` is the business repository,
and `./booking-worktrees/` contains that business repository's isolated checkouts.
The sole registry is `./booking-demo/.ai-company/STATE.md`, written by Portal CTO.
Below, owned files are relative to the business repository; checkout names are
relative to `./booking-worktrees/` except for the CTO's `./booking-demo/` checkout.

| Task label | Manager | Exclusive business-file ownership | Checkout / branch | Synthetic state and evidence |
| --- | --- | --- | --- | --- |
| Portal CTO | Human owner | `.ai-company/STATE.md` | `./booking-demo/` / `sample/coordination` | `active`: owner appointment and registry read assumed |
| API Lead | Portal CTO | `docs/contracts/booking-search.md`, `.ai-company/notes/api.md`; sole integration writer | `api-lead/` / `sample/integration` | `active`: contract approval and assigned scope assumed |
| Web Lead | Portal CTO | `.ai-company/notes/web.md` | `web-lead/` / `sample/web-lead` | `active`: scope receipt and read-only review assignment assumed |
| API Search | API Lead | `src/api/booking-search.ts`, `tests/api/booking-search.test.ts` | `api-search/` / `sample/api-search` | `active`: accepted brief and clean-base readback assumed |
| Web Search | Web Lead | `src/web/booking-search.tsx`, `tests/web/booking-search.test.tsx` | `web-search/` / `sample/web-search` | `pending`: `Web Search request (fictional)` exists; task/workspace readback still needed |

This is an excerpt of the one registry, not a second live status table.
Each lead writes its notes in its own checkout and sends status changes to the CTO.
API Lead owns the shared contract; workers request contract changes through their lead.
Their tests use separate in-memory fixtures. Web Search alone owns the local preview session.
Next: Web Lead reads the pending task and checkout, then reports readiness to the CTO.
It checks the existing creation request before any retry. `pending` earns no “running” badge.

#### One complete worker brief: API Search

- Manager and outcome: API Lead; implement reference search using the existing booking service.
- Context: business `AGENTS.md`, the sole registry, and `docs/contracts/booking-search.md`; all are fictional inputs here.
- Contract: a signed-in request supplies `reference`; the existing response contains `id`, `reference`, and `status`. No schema or authentication changes.
- Scope and baseline: only the two API Search files above, in `api-search/` on `sample/api-search`, from `sample-base (fictional)`; clean start assumed.
- Acceptance: a reference returns the expected synthetic booking, an unknown reference returns an empty list, and an unauthenticated request stays rejected.
- Dependencies/resources: approved contract already included in the assigned base; isolated in-memory fixtures; no shared database or preview session.
- Model: `sample-coding-model (fictional)` with supported high reasoning; no subagents or new persistent tasks.
- Planned checks: `npm run test:booking-search` and `npm run test:auth`, fictional project commands to run in a real implementation, **not executed here**.
- Stop/report: report start, a contract mismatch, failure, or ready candidate to API Lead; pause the affected part at a mismatch and preserve independent work. No open-ended experiment.
- Return to API Lead: exact candidate, changed files, command output and exit codes, test artifacts, limitations, and a proposed dependency handoff. Exclude other files and external effects beyond the owner's brief.

Web Search receives its own brief after readback and becomes `active` in the
synthetic registry. It can build the UI with approved fixtures while the API work
proceeds; connecting it to the API waits for the handoff below.

#### The owner changes a label; the lead keeps everyone informed

**Synthetic event, sample checkpoint 2: Web Lead -> Portal CTO, “Search label.”**
Owner intent: “Call the button ‘Find a booking’ instead of ‘Search’.”
Interpretation: copy-only change; query behavior, response fields, and scope stay the same.
Action: Web Lead updates Web Search's brief and expected UI assertion; its worker applies the change.
Impact: Web Lead shares the new label with API Lead for acceptance review; no shared design decision is needed.
Decision needed: none; continue under the owner's authorization. Delivery: CTO receipt is assumed in this sample.
The CTO records the conclusion. Nobody asks the owner to approve the same label twice.

#### Dependency handoff: something the receiver can inspect

- Producer -> consumer: API Lead's API Search -> Web Lead's Web Search.
- Artifact: `sample-candidate-A (fictional)` containing the API change against the approved contract.
- Release condition: Web Lead checks field names, match/empty/error fixtures, and authentication regression evidence before connecting the interface.
- Synthetic evidence: `sample-api-report-A (fictional)` assumes those checks passed; Web Lead's read-only review assumes no unresolved findings. Neither report exists as a real run.
- Receiver: Web Lead accepts in the rehearsal, tells its own worker to connect the interface, and reports the released dependency to Portal CTO.
- Ownership: the API files and contract keep their owners. A mismatch would block connection, with API Lead responsible for resolution; fixture-based UI work could continue.

#### Final acceptance record: a closed milestone, with receipts

**Synthetic ending, sample checkpoint 3. These are illustrative outcomes, not test results.**
The leads mark both workers `ready` with A and `sample-candidate-B (fictional)`.
API Lead reviews the Web change read-only and combines both in its assigned checkout
as `sample-candidate-C (fictional)`. Mainline still waits: earlier reports do not approve C.

| Acceptance item | Synthetic disposition for candidate C | Fictional evidence label |
| --- | --- | --- |
| Matching/empty search, recoverable error, unchanged authentication | Assumed passed on combined candidate C | `sample-search-auth-C (fictional)` |
| “Find a booking” label, keyboard flow, and build | Assumed passed on the local bookings page with synthetic fixtures | `sample-ui-build-C (fictional)` |
| Independent review and required CI | Assumed passed; Web Lead reviews the combined result; existing CI checks C | `sample-review-C (fictional)`, `sample-ci-C (fictional)` |

After these checks, API Lead advances the approved mainline to C in this rehearsal.
Milestones in the same registry: **implementation passed** (workers), **verification
passed** (leads), **integration passed** (API Lead), all synthetic and bound to C.
**Deployment is out of scope**, as the owner specified. No production outcome is claimed.
Portal CTO assumes artifact readback and records both worker assignments and the
search milestone as `done`; the candidates and reports form the sample handoff.
No mandatory gate remains open in this fictional ending. A real failure would
keep it open; a changed candidate would require the applicable checks again.
The detail-view and audit-event goals remain unimplemented. They cannot borrow this milestone's “done.”

## 2. A lead needs to hand over

**Situation:** the Web lead's task must be replaced while two workers are active.

1. The CTO records the reason and identifies the proposed successor. A timeout
   alone is not proof that the old lead or its writers have stopped.
2. The old lead stops dispatching and provides goals, user decisions, worker
   identities, file ownership, candidates, dependencies, and unclosed findings.
   If it is unavailable, the CTO verifies the actual running and file state.
3. The successor reads and accepts the handoff through the host's authorized
   management channel. The CTO then records the effective ownership transfer.
4. The affected workers receive the registered successor relationship. They keep
   their existing checkouts and task scopes; they do not duplicate the work.
5. The successor continues from the latest verified state. Unclear ownership
   pauses only the potentially conflicting assignment.

**Acceptance:** there is one dispatching lead, the workers recognize that lead,
the owner can inspect the handoff, and no candidate or unresolved issue vanished.

## The schedule illustration

The README's chart uses an independent scheduling example:

| Work | Duration | Dependency |
| --- | --- | --- |
| Planning | 1 unit | None |
| A, B, C, D | 2 units each | Planning; no dependencies on one another |
| Integration and verification | 1 unit | All four tasks |

Serial elapsed time is `1 + 2 + 2 + 2 + 2 + 1 = 10` units.
With four worker slots, ideal parallel elapsed time is `1 + max(2,2,2,2) + 1 = 4`.
Total scheduled work is 10 units in both cases. Extra coordination, latency,
contention, and rework are excluded. No token or monetary cost model is implied.
