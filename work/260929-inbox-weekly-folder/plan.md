# Plan: inbox-weekly-folder

Spec: approved 2026-09-29.

1. Rewrite `docs/weekly-refresh.md` steps 1–3 to spec requirements 1–8 (year names, wait for both, WoW from the published week file, year-form week files). Also update step 5's file naming.
2. `README.md`: source line uses the year form.
3. `.github/scripts/test_freshness.py`: add a year-form case (6 cases).
4. Routine prompt (private): heartbeat example in year form; it still points to steps 1–3.
5. Reviewer on PR #4 and fix its findings.
6. **Held until Ty confirms the kernel naming line is updated:** rename the 33 Drive PDFs to `ECP-2026-W<NN>.pdf` by API, then re-list (33, sizes unchanged, 2 opened).
7. Write `verification/inbox-weekly-folder.md` and run promise checks 1–4.
8. Ty sends the ship phrase in his own prompt; then merge and check main.
