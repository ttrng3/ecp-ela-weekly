# Spec: inbox-weekly-folder

**Approved:** 2026-09-29
**Amended:** 2026-09-29, review fixes with no change of scope: week ≤ 2 in December → next year (req 4); `REVIEW.md` week-file lines updated to the year form (Design).

**Intent:** accepted 2026-09-29 · **Status:** approved

## Requirements

1. The routine reads weekly source PDFs from one Drive folder, `00 Inbox/Weekly Reports ECP-ELA/`, by folder id held in the private routine prompt, never the repo. It never searches Drive-wide. *(intent: Outcome 1; Constraints, public repo)*
2. Standard name: `ECP-<YYYY>-W<NN>.pdf` / `ELA-<YYYY>-W<NN>.pdf`, week zero-padded (`ECP-2026-W39.pdf`). The 33 source PDFs moved on 2026-09-29 (Drive API listing of the inbox, 2026-09-29 03:13 UTC) are renamed to this form. *(Outcome 1)*
3. Newest is decided by (year, week), so `2027-W01` is newer than `2026-W52`. *(Outcome 1)*
4. A file with a Zalo name is still read: project from `ECP` / `Eco Vinh` / `Eco Central Park` / `Central Park` or `ELA` / `Long An` / `Eco Retreat`; week from `W`, `Week`, `Tuần`, `Tuan`; year from the name, else the file's Drive `createdTime` year (a week ≥ 50 created in January counts as the previous year; a week ≤ 2 created in December counts as the next). Every such file is listed in the report so Ty can rename it. A PDF with no project, both projects or no readable week is listed and not used. *(Outcome 2)*
5. A new week N is published only when **both** ECP and ELA have a file for (year, N), and (year, N) is newer than `current`. If several such weeks exist, the newest one is published. A week only one project filed is never published. *(Outcome 3)*
6. WoW compares week N with the currently published week, read from `data/weeks/<current>.json`, not with a second PDF. If they are not consecutive, the page's `prev` says which week it compares with and the report names the gap. *(Outcome 3, "Report, don't fake")*
7. The heartbeat is written once per run as the first write. `newest-source` is `ECP-<YYYY>-W<NN>/ELA-<YYYY>-W<NN>` (a side with no file is `none`), `inbox-unreachable` or `inbox-empty`. The last two, and `ECP-none/ELA-none`, raise the stale-data issue. *(Outcome 4; "The heartbeat stays")*
8. When no week is newer on both sides, the heartbeat is the only write, and the report names which project the page is waiting for. *(Outcome 3)*

## Design

**Drive (done by API, verified by re-listing, per "File operation safety"):** rename the 33 PDFs `ECP-W19.pdf` → `ECP-2026-W19.pdf` etc. All current files are 2026 (Verified: Drive API listing of the inbox, 2026-09-29 03:13 UTC; the history runs W18–W38 with createdTime May–Sep 2026).

**Repo, `docs/weekly-refresh.md` steps 1–3:** rewrite to requirements 1–8. This replaces the earlier draft of this PR's "publish when either side files" and "one side filing nothing is normal" rules.

**Repo, week files:** new weeks are written `data/weeks/2026-W39.json` with `data/index.json` → `"current": "2026-W39"` and `"weeks": {…, "2026-W39": "2026-W39"}`. The renderer already resolves `IDX.weeks[IDX.current]` to a file name (`index.html:268`) and shows the label from the file's own `week` field ("Tuần 39"), so `index.html` does not change. The existing `W37`/`W38` keys stay and are read as 2026. `.pages-allow` already covers `data/weeks/*.json`. Without this, `W37.json` would be overwritten in September 2027.

**Repo, `.github/scripts/freshness.py` + `test_freshness.py`:** as in PR #4 (alarm on `inbox-unreachable`, `inbox-empty`, `ECP-none/ELA-none`; six-case test including a year-form case).

**Routine prompt (private):** it holds the folder id and points to runbook steps 1–3. Its heartbeat example changes to the year form.

**Repo, `REVIEW.md`:** "What a refresh writes" and "The manifest stays consistent" name the year-form week files.

**Mirror (artifact mirror contract):** step 7 is unchanged. It publishes the changed `data/` paths, now `data/weeks/2026-W<NN>.json`, to the one existing preview. No new artifact.

## Conflicts

Loaded: kernel `standing-instructions.md` (session protocol, change discipline) and root `CLAUDE.md` (rules incl. "Weekly reports → `00 Inbox/Weekly Reports ECP-ELA/`", "File operation safety", "Drift detection"); the artifact mirror contract (memory); entity separation; secure-pages. Not loaded: ty-report-standard and apple-design, because the page and its visual output do not change. No repo `CLAUDE.md` exists.

| Rule (by name) | What in the design breaks it | Resolution, or question for Ty |
|---|---|---|
| "Weekly reports → `00 Inbox/Weekly Reports ECP-ELA/`" (root `CLAUDE.md`) | The rule you changed today says the files are named `ECP-W<N>.pdf` / `ELA-W<N>.pdf`. This spec names them `ECP-<YYYY>-W<NN>.pdf`. Kernel and repo would disagree, which is drift. | **Ty:** update that rule's naming line from a non-project chat (kernel + account memory, per "Two copies of the rules"). Replacement text: "…saved as `ECP-<YYYY>-W<NN>.pdf` / `ELA-<YYYY>-W<NN>.pdf` (e.g. `ECP-2026-W39.pdf`)". I don't rename the Drive files until you confirm it has landed. |
| File naming standard `YYMMDD_PROJ_Type_Desc` (root `CLAUDE.md`, Reference) | The source PDFs don't follow it. | Already excepted by the weekly-reports rule above. No action. |
| "File operation safety" (root `CLAUDE.md`) | The 33 renames are a bulk rename. | Done by Drive API (metadata only, no bytes copied), with your word from this spec's approval. Verified by re-listing: count 33, sizes unchanged, 2 PDFs sample-opened. |
| Artifact mirror contract (memory) | New week-file names reach the preview. | Step 7 already publishes changed `data/` paths to the existing preview. Nothing is created or deleted. |
| Entity separation (OMNI / ECOPM) | None. The inbox holds ECP and ELA reports only, both on the same side as this repo today. | none |
| "The heartbeat stays" / "Report, don't fake" (repo REVIEW.md) | "Wait for both" can leave the page on an old week for a while. | Every run still writes the heartbeat and names who is missing. The 24-day stale-data alarm fires if a side stops filing. |

## Security

```
## Security (secure-pages, 2026-09-29)
1 Secrets ........ PASS (tree 0 hits, history 0 hits, no JWTs)
2 Visibility ..... PUBLIC — PASS. data/ holds the operating figures the dashboard publishes today; this change adds none. The Drive folder id stays out of the repo.
3 Pages .......... PASS. Workflow deploy from main, allowlist .pages-allow: index.html, data/index.json, data/weeks/*.json. work/, docs/, .github/ are not served.
4 Supabase ....... N/A (no Supabase)
Verdict: safe to ship
```

## Promise

`verification/inbox-weekly-folder.md`, run on 2026-09-30 and again after the first real run on Sun 2026-10-04 (21:00 Hanoi):

1. **Drive:** the inbox lists 33 PDFs, all matching `^(ECP|ELA)-2026-W\d{2}\.pdf$`, sizes equal to the pre-rename listing. Pass line: `33/33 renamed, 0 size changes`.
2. **Freshness alarm:** `python3 .github/scripts/test_freshness.py` passes all cases. Pass line: `6/6 ok`.
3. **Routine, fired by hand:** with the inbox as it is (both sides at 2026-W38), the run writes one heartbeat `newest-source=ECP-2026-W38/ELA-2026-W38`, writes nothing under `data/weeks/`, and reports no new week. Pass line: one commit touching only `data/.last-check`.
4. **Wait-for-both, dry fixture:** a copy of the runbook logic run by hand against a listing with `ECP-2026-W39` and no ELA W39 publishes nothing and reports "waiting for ELA". The same listing plus `ELA-2026-W39` selects `2026-W39`. Pass line: both verdicts as stated.

## Out of scope

- Renaming the `.docx` analysis files in the folder (they already follow `YYMMDD_PROJ_Type_Desc`).
- Renaming the existing `data/weeks/W37.json` / `W38.json`.
- Any change to `index.html`, the stylesheet or the page's look.
- Reading the large ELA PDFs (a separate, known extraction problem; ELA-W38 is 164,495,308 bytes per the Drive listing of 2026-09-29).
