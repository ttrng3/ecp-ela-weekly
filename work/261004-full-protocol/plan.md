# Plan: full-protocol

1. README: one "Public on purpose (Ty, 2026-10-04)" line under the intro (Ty's ruling; spec Conflicts).
2. `tools/verify_live.py`: the verdicts in spec "Design", modelled on Omni-TMDV's script.
3. `verification/weekly.md`: steps 1–4, invariants, adversary, substitutes, evidence, not covered and traps, pointing to the three per-change checks.
4. Test on the branch: step 1 against live now (W39), then both drills in a scratch copy.
5. PR → reviewer → fixes. Ty ships after the Sunday 21:00 Hanoi run (no merge 13:30–15:00 UTC). Steps 1–4 then run on `main` against W40 or the run's quiet outcome, with evidence on the PR.
