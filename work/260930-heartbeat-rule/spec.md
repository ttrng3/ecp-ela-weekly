# Spec: heartbeat-rule

**Approved:** 2026-09-30 (Ty, "approve for all four")

**Intent:** accepted 2026-09-30 · **Status:** approved

## Requirements
1. `docs/weekly-refresh.md` step 1: the line is exactly `<UTC> newest-source=<value>`; nothing after the value; observations go in the step 7 report.
2. `data/.last-check` on main: the text after `newest-source=ECP-2026-W39/ELA-2026-W39` is removed; timestamp and value kept byte for byte.

## Design
One runbook paragraph, one data line. No code change. The routine prompt is **not** changed: it has no heartbeat wording of its own ("STEPS 1–3 … follow the runbook's steps 1–3 EXACTLY"; "If anything disagrees with those files … THE FILES WIN"), so the runbook line governs the next run. Prompt diff: none (checked by a same-turn `get` of the weekly routine (trigger id held in the routine prompt), 30/09, updated_at 2026-09-30T03:32:20Z).

## Conflicts
None found. REVIEW.md: no published path added (`data/.last-check` stays `!` in `.pages-allow`).

## Security
Removes a Drive folder id from the current tree of a public repo. History keeps it (Ty's ruling, not rewritten).

## Promise
- `python3 .github/scripts/test_freshness.py` all ok and `python3 .github/scripts/freshness.py` gives `stale=false` on the edited heartbeat (checked 30/09 on the branch).
- `git grep -n -F "$INBOX_ID"` on main after merge prints nothing, with the inbox folder id passed in at run time from the routine prompt (never written here). Run on the branch 30/09: no output.
- The next run (Sun 2026-10-04 14:00 UTC) writes a heartbeat with nothing after the value; checked on 4 Oct.

## Out of scope
The routine prompt; git history; other repos' heartbeats.
