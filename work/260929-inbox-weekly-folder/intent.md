# Intent: the weekly routine reads ECP and ELA reports from one Drive inbox folder

**Status:** accepted 2026-09-29
**Source:** chat, 2026-09-29 (Ty: "move and merge these two subfolders under 00 Inbox… so when I save new files from zalo messages it will be quick… update the routine mirror of the new changes so it won't have issues in the future")

**Problem.** Ty saves each week's BQLVH reports from Zalo into two different Drive folders (`01 Eco Central Park - ECP/07 Weekly Reports/` and `02 Eco Retreat Long An - ELA/07 Weekly Reports/`). That is slow. The files arrive under Zalo names ("Ban QLVH Eco Vinh - Tuần 38.pdf", "Ban QLVH Long An Tuần 38.pdf"), which the runbook's `*ECP*Tuần-<N>*` pattern did not match (W38.json records the mismatch). On 2026-09-29 the two folders were merged on Drive into `00 Inbox/Weekly Reports ECP-ELA/`, and the source PDFs were renamed `ECP-W<N>.pdf` / `ELA-W<N>.pdf`. The runbook (`docs/weekly-refresh.md` step 2) still names the old folders, which no longer exist.

**Outcome.**
- Weekly source PDFs live in one Drive folder, `00 Inbox/Weekly Reports ECP-ELA/`, named with the year: `ECP-2026-W39.pdf` / `ELA-2026-W39.pdf` (Ty, 2026-09-29: "have the new year in the name"). The 33 existing PDFs are renamed to this form. Year then week decides "newest", so January's W01 is correctly newer than December's W52.
- A file that still carries its Zalo name is still found (project from ECP / Eco Vinh / Eco Central Park or ELA / Long An / Eco Retreat; week from W / Week / Tuần). It is listed in the report so Ty can rename it.
- ECP and ELA always show the **same week** on the page (Ty: "both ecp and ela should have the same week update"). Week N is published only when **both** projects have filed week N (Ty, 2026-09-29: "wait for both"). A week only one project filed is never published on its own. If one side skips a week entirely, the page waits for the next week both have filed, and the report names who is missing. A long wait is caught by the existing 24-day stale-data alarm.
- The heartbeat distinguishes a normal or quiet week, an unreadable inbox and an inbox where nothing matched. The last two raise the stale-data issue.

**Who and what is affected.** `docs/weekly-refresh.md` steps 1–3, `README.md`, `.github/scripts/freshness.py` (and a test for it), and the private routine prompt "ECP × ELA weekly refresh" (holds the folder id). Ty saves new reports into the inbox. The Pages dashboard, renderer, stylesheet and `data/` shape are unchanged.

**Constraints.** The repo is public: the Drive folder id stays in the private routine prompt, never in the repo. The heartbeat is written on every run ("The heartbeat stays"). "Report, don't fake": no number is guessed or carried over unlabelled. Never search Drive-wide. OMNI and ECOPM never share. The kernel rule for weekly reports was already changed by Ty on 2026-09-29 to point at the inbox; nothing here edits `About me/`.

**Open questions.** none known.
