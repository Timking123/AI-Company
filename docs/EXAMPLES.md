# Two fictional walkthroughs

All projects, tasks, and participants below are invented. These examples show
expected coordination, not recorded model runs or measured results.

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

## 2. A lead needs to hand over

**Situation:** the Web lead's task must be replaced while two workers are active.

1. The CTO records the reason and identifies the proposed successor. A timeout
   alone is not proof that the old lead or its writers have stopped.
2. The old lead stops dispatching and provides goals, user decisions, worker
   identities, file ownership, candidates, dependencies, and unclosed findings.
   If it is unavailable, the CTO verifies the actual running and file state.
3. The CTO records the ownership transfer. The successor reads the evidence and
   accepts the handoff through the host's authorized management channel.
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
