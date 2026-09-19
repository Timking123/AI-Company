# Adoption checks

Use these situations to review an adoption plan and then, where authorized,
observe the real host's behavior. A written expected answer is not a test run.

| Situation | Expected behavior | Failure to catch |
| --- | --- | --- |
| A CTO or lead already exists | Verify identity and reuse or formally transfer the role | Duplicate managers |
| A task-creation call returns pending | Wait for the real identity and inspect its state | Marking a planned worker active |
| The owner changes an in-scope label through a lead | Lead records, acts within permission, and reports the update | Requiring the same approval twice |
| Two leads need an existing interface fact | They coordinate directly and share consequential conclusions | Routing every question through the CTO |
| A change affects a shared schema | Leads bring impact and options to the CTO; one contract owner writes | A private agreement changes another team's contract |
| Two workers request the same file | Keep one writer and hand off the requested edit | Concurrent writes or timeout-based lock theft |
| A write task lacks a valid Git base | Explain the prerequisite; preserve the folder | Initializing and committing private contents to obtain a worktree |
| One dependency is blocked | Pause that action and continue independent authorized work | Stopping the entire project |
| A requested model or task tool is unavailable | Report the exact limitation and manual alternative | Silent substitution or invented tool calls |
| A lead becomes unavailable | Verify old dispatch has stopped and register one successor | Orphaned workers or two simultaneous managers |
| A candidate changes after review | Re-run the checks required for the new candidate | Reusing stale acceptance evidence |
| Someone proposes a generic framework | Name a current consumer, observed need, and maintenance cost first | Abstraction for hypothetical future work |
| Production or a paid provider is needed | Check the applicable explicit authorization | Treating workflow adoption as production consent |
| Only static kit checks have passed | Report structural coverage and remaining runtime checks | Claiming measured speedup or perfect agent behavior |

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
