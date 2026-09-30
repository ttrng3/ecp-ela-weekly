# Intent: heartbeat line carries nothing after its value

**Status:** accepted 2026-09-30 (Ty, "approve for all four", follow-up 4 of the heartbeat-notes spec)
**Source:** chat, 2026-09-30. Spec 6 ("and the routines too") made every routine's heartbeat status-only; this repo's routine was left to this loop because its prompt reserves edits to it.

**Problem.** The 2026-09-30 run wrote `data/.last-check` with a long explanation after `newest-source=…`, including the inbox's Drive folder id and file counts. The repo is public; CLAUDE.md forbids a Drive folder id in it. The runbook's step 1 says what the value is but not that nothing may follow it.

**Outcome.** Step 1 says the line is exactly `<UTC> newest-source=<value>`, nothing appended. The heartbeat on main no longer carries the appended text.

**Who and what is affected.** The weekly routine (it follows runbook steps 1–3 "EXACTLY" and "THE FILES WIN"), `freshness.py` (reads the timestamp and the first token after `newest-source=`, so unaffected).

**Constraints.** The values `ECP-<YYYY>-W<NN>/ELA-<YYYY>-W<NN>`, `inbox-unreachable`, `inbox-empty`, `ECP-none/ELA-none` are unchanged. Git history is not rewritten (Ty, 30/09, same ruling as Ops-Dashboard).

**Open questions.** none known
