# Spec: full-protocol

**Approved:** 2026-10-04

**Intent:** accepted 2026-10-04 · **Status:** approved

## Requirements
1. `verification/weekly.md` and `tools/verify_live.py` on `main`, in the shape of the 7 pipeline protocols (Promise, Clean state, Steps, Invariants, Adversary, Sanctioned substitutes, Evidence, Not covered, Traps). (Intent, Outcome)
2. Step 1 is one script that exits 0 only when every verdict is true, printing one JSON object. (Outcome)
3. The served files match `main`, and the private files answer 404. (Outcome, first bullet)
4. The manifest holds together: `current` is in `weeks`, every week listed has its file, weeks are in (year, week) order, and the `W37`/`W38` keys are kept. (Outcome, second bullet)
5. Every published week has both ECP and ELA. (Outcome, third bullet)
6. The heartbeat is fresh against the 9-day watchdog, the data is fresh, and the heartbeat line has nothing after its value. (Outcome, fourth bullet)
7. No personal traces, Drive ids, mount path or forbidden words in any served or tracked file. (Outcome, fifth bullet)
8. A browser step and a preview step. (Outcome)
9. The protocol passes once on the live site after merge, first after the 2026-10-04 21:00 Hanoi run, and is drilled with at least one deliberate breakage. (Outcome; open question 1, chosen yes)
10. The three per-change checks stay; the protocol points to them. (Open question 2, chosen yes)

## Changes from the intent
- **No week picker.** The intent said the browser step checks "the week picker". The page has none: `index.html` renders only `IDX.current`. The browser step checks the current week instead.
- **"Sourced or marked ⚠" is not machine-checkable.** Whether a figure came from the deck can't be read from the JSON. The script checks that both sides are present (requirement 5); sourcing goes under Not covered.

## Design
Two new files plus one README line (Ty's 2026-10-04 ruling: public on purpose). No change to the page, data, runbook, routine prompt, Mac helper or `.pages-allow`. Neither file is under the watched `data/` area, so Pages won't serve them and the allowlist needs no line.

**`tools/verify_live.py`** is modelled on `Omni-TMDV/tools/verify_live.py`: same `get()` with one retry, same `age_days()`, NFC casefold for forbidden words, and matches reported by count and file. Verdicts:

| Verdict | Check |
|---|---|
| `manifest_consistent` | `current` in `weeks`; every value has `data/weeks/<v>.json`; `current` is the last key |
| `weeks_ordered` | keys sort by (year, week), with `W37` and `W38` read as 2026; every other key matches `^\d{4}-W\d{2}$` |
| `legacy_keys_kept` | `W37` and `W38` are present and map to themselves |
| `both_projects_every_week` | in every week file, `kpis`, `done`, `progress` and `actions` each hold a non-empty `ecp` list and a non-empty `ela` list |
| `served_equals_main` | `index.html`, `data/index.json` and every `data/weeks/*.json` return 200 with the sha256 of `main` |
| `private_not_served` | README, CLAUDE.md, REVIEW.md, `data/.last-check`, `docs/weekly-refresh.md`, the `tools/` files, `verification/*.md`, `build/artifact.html`, `archive/status_20260915.html`, `.github/scripts/freshness.py`, `.pages-allow` and one `work/` file found at run time all exist on `main` and answer 404 |
| `heartbeat_fresh` | first field of `data/.last-check` ≤ 9 days (`collect_status.py`, `ecp-ela` row) |
| `heartbeat_bare` | the heartbeat matches `^\S+Z newest-source=\S+$` (the 30/09 rule, PR #12) |
| `data_fresh` | `generatedUtc` ≤ 24 days (`freshness.py` `MAX_DATA_AGE_DAYS`) |
| `all_tracked_read` | every tracked text file was read |
| `no_personal_traces` | no storage link, email address, bare handle, or `GoogleDrive-` mount fragment in any served or tracked file |
| `no_forbidden_words` | none of the `--forbid` words in any served file; fails if none are given |

`--forbid` takes the other entity's name and the inbox folder id, both read by the runner at run time (the id from the routine prompt). Neither is ever written to the repo.

**`verification/weekly.md`:**
- **Step 1:** the script.
- **Step 2:** Chrome on the live page. `#sub` has no "Không nạp được"; `#sections` holds 2 × 6 `.kpi` elements and the ECP and ELA panels; the `h2` names the current week's `W.week`.
- **Step 3:** console errors.
- **Step 4:** the preview, found by title through `Artifact list` (the gdsh precedent: the verifier can't call `RemoteTrigger get`). Its `index.html` must equal a fresh `tools/build-fragment.py` output, and its data files must match `main` or the last run's commit.
- **Points to, doesn't repeat:** `inbox-weekly-folder.md`, `ela-page-images.md` and `260930-heartbeat-rule.md` for run-time behaviour.
- **Drill:** in a scratch copy, delete `kpis.ela` from the current week, and separately append text to the heartbeat. `both_projects_every_week` and `heartbeat_bare` must each turn false; nothing is committed.

## Conflicts
Loaded: kernel `standing-instructions.md` and root `CLAUDE.md` (Read tool), the artifact mirror contract and entity-separation memories, the repo's `CLAUDE.md` and `REVIEW.md`, and secure-pages. ty-report-standard and apple-design don't apply: no page or report changes.

| Rule (by name) | What in the design touches it | Resolution, or question for Ty |
|---|---|---|
| Artifact mirror contract | Step 4 reads the preview | Read-only (`Artifact list`/`read`), found by title; no id or URL written; nothing published or deleted |
| Artifact mirror contract: every pipeline change is also a Pipeline Wiring change | A protocol could count as a change | It changes no run, schedule or preview. The 7 protocols of 1–2 Oct added no wiring entry. Same here |
| OWNERSHIP line (routine prompt; handoff note) | Owner session tytr3-50 is gone | Handoff note: the next session takes ownership by reading it (done 2026-10-04). The prompt isn't touched |
| Entity separation | The forbidden list holds the other entity's name | Passed at run time, never written; the script prints counts, not values |
| Never by value (REVIEW.md) | Traces and folder id | Reported by count and file; the id comes from the prompt at run time |
| Changes reach `main` through a PR and Ty's ship (CLAUDE.md) | Two new files | One PR, the reviewer first, then the ship phrase; not merged 13:30–15:00 UTC Sunday |
| secure-pages check 2 (visibility vs content) | Already true before this change: the page serves OMNI weekly operating figures to anyone, with no `robots.txt` | **Ty ruled 2026-10-04: public on purpose.** This PR records it in README (one "Public on purpose" line, as TMDV and Trade-Journal carry); the protocol asserts nothing more |

## Security
```
## Security (secure-pages, 2026-10-04)
1 Secrets ........ PASS | history: 0 hits
2 Visibility ..... PUBLIC — PASS: public on purpose (Ty, 2026-10-04), recorded in README by this PR
3 Pages .......... PASS: Actions deploy from main /, allowlist live; README, CLAUDE.md, REVIEW.md, data/.last-check, docs/, .pages-allow, a work/ file all 404 (curl, 2026-10-04)
4 Supabase ....... N/A: no Supabase
Verdict: safe to ship
```

## Promise
After merge and after the Sunday 2026-10-04 21:00 Hanoi run, from a clean `main`: `python3 tools/verify_live.py --forbid <words>` prints `"pass": true` and exits 0, and steps 2–4 pass. Measured by 2026-10-05, 12:00 Hanoi. Each drill turns its verdict false. Evidence (the JSON, screenshots, preview hashes) goes in the PR, as the 7 did.

## Out of scope
- Checking figures against the decks.
- Any change to the routine prompt, runbook, Mac helper, page or data.
- The leftover open items in the ECP × ELA handoff: the test routine to delete, the GitHub Support purge, the W37 "khai trương" follow-up, and the `_pages/` leftover.

## Changes during the build
Found in review rounds on PR #13, after approval. The approved text above stands as Ty approved it; Ty's ship phrase accepts these too.
1. **Two forbidden-word flags.** `--forbid` (the other entity's name) reads served files only, because docs may name the entity's label (REVIEW.md). `--forbid-anywhere` (the inbox folder id) reads every served and tracked file, so Requirement 7 holds for the id. Both flags are required. The Promise command is `verify_live.py --forbid <entity> --forbid-anywhere <folder id>`.
2. **Non-KPI sections may be empty.** `both_projects_every_week` requires non-empty `kpis` for both sides; `done`, `progress` and `actions` must exist for both but may be empty. A week where one project has nothing to decide is still filed by both, and runbook step 3 is about filing, not section contents.
3. **No fixed KPI count.** Step 2 compares the page's `.kpi` count with the week file's, so the Design's "2 × 6" is not used.
4. **Stricter heartbeat.** `heartbeat_bare` accepts only runbook step 1's three value shapes.
5. **Every protocol in `verification/` must answer 404**, found at run time.
