# Intent: one full verification protocol for the ECP × ELA weekly page

**Status:** accepted 2026-10-04
**Source:** chat, 2026-10-04 (Ty's Gate 3 ruling: "let ECPxELA and pipeline wiring have a full protocol")

**Problem.** Gate 3 of the build loop asks for one full protocol per pipeline. The 7 shipped 1–2 Oct each prove the whole live page with `verification/<page>.md` plus `tools/verify_live.py`. This repo has only per-change checks (`verification/inbox-weekly-folder.md`, `ela-page-images.md`, `260930-heartbeat-rule.md`). Nothing re-runnable proves that what https://ttrng3.github.io/ecp-ela-weekly/ serves today is right. Ty ruled on 2026-10-04 that Gate 3 passes only when this repo and pipeline-wiring have one.

**Outcome.** `verification/weekly.md` and `tools/verify_live.py` exist on `main`, in the same shape as the 7. Step 1 is a script that exits 0 with every verdict true:
- every served file is byte-identical to `main`, and the private files answer 404;
- the manifest holds together: `current` is in `weeks`, every listed week has its file, weeks are in (year, week) order, and the legacy `W37`/`W38` keys are kept;
- every published week has both ECP and ELA (wait-for-both), and a figure is either sourced or marked ⚠;
- the heartbeat is no older than the 9-day watchdog in pipeline-wiring's `collect_status.py`, and the data is fresh;
- no personal traces, Drive ids, mount path or forbidden words appear in any served or tracked file.

A browser step renders the current week and the week picker with no console error. A preview step checks that the Cowork preview matches `main` or the last run. The protocol passes once against the live site after merge, and is drilled with at least one deliberate breakage.

**Who and what is affected.** The `ecp-ela-weekly` repo only, plus one Progress line in the AI-Native Build Loop doc. The routine prompt, the runbook, the Mac helper and the page itself don't change.

**Constraints.**
- OMNI repo: no EcoPM names or data (entity separation).
- Never write the Drive folder id, the Drive mount path, a preview id or a person's details into the repo; the forbidden words are passed at run time.
- The routine prompt is reserved for this repo's build loop (OWNERSHIP line). This change doesn't touch it.
- Don't merge during the Sunday 21:00 Hanoi run.
- Changes reach `main` only through a PR and Ty's ship phrase.

**Open questions.**
1. Should the first passing run be after tonight's 21:00 run (the first W40 on the new setup), so it proves the wait-for-both rule on a real new week? I recommend yes. **Chosen: yes** (Ty accepted with the recommendations, 2026-10-04).
2. Should the three per-change checks stay as they are, with the protocol pointing at them rather than absorbing them? I recommend yes. **Chosen: yes** (Ty accepted with the recommendations, 2026-10-04).
