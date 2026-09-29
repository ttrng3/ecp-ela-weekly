# Verification: inbox-weekly-folder

Spec: `work/260929-inbox-weekly-folder/spec.md` (Promise). Folder id: held in the private routine prompt, not here.

## 1. Drive names — PASS 2026-09-29 06:23 UTC

Drive API listing of the inbox (`mimeType = application/pdf`, both pages): **35 PDFs, 35/35 match `^(ECP|ELA)-2026-W\d{2}\.pdf$`.**
- 33 renamed by API 06:21–06:22 UTC; every `fileSize` equals the 03:13 UTC pre-rename listing (e.g. ELA-2026-W38 164,495,308 B; ECP-2026-W24 43,034,568 B).
- 2 more found in the inbox and renamed 06:22 UTC: `ECP-W39.pdf` → `ECP-2026-W39.pdf` (3,515,692 B) and `ELA-W39.pdf` → `ELA-2026-W39.pdf` (141,917,085 B), both created 2026-09-26.
- Sample open earlier the same day: `ECP-W38.pdf`, `ECP-W19.pdf` start with `%PDF-` (same file ids).

Pass line: `35/35 year-form, 0 size changes`.

## 2. Freshness alarm — PASS 2026-09-29

`python3 .github/scripts/test_freshness.py` → 6/6 `ok`.

## 3. Routine, fired by hand — pending (after merge)

Expected now that both projects have W39 in the inbox: the run publishes **2026-W39** (`data/weeks/2026-W39.json`, `current` = `"2026-W39"`), heartbeat `ECP-2026-W39/ELA-2026-W39`. ELA-W39 is 141 MB, so ELA figures may come back as `⚠ chưa cập nhật`.

## 4. Wait-for-both — pending

Checked against the next run where only one project has filed.
