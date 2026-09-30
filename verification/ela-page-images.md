# Verification: ela-page-images (revision 2)

Spec: `work/260930-ela-page-images/spec.md` (Promise).

## 1. Mac job renders — PASS 2026-09-30 02:12 UTC
launchd agent `com.ty.ela-pages` loaded; first attempt failed (`pdftoppm` on the mount → "Couldn't find trailer"), second failed (`cp` → "Resource deadlock avoided" on a Drive placeholder); fixed by streaming the source with `cat` into a temp file and size-checking it. Third run: `rendered ELA-2026-W39: 30 pages`, `done` = `pages=30 source_bytes=141917085`.
Caveat: the source had been hydrated by a manual `cat` minutes earlier, so rendering from a fully cold placeholder under launchd is not yet proven. It will show on the first new ELA file; a failure is logged and retried hourly, and the routine falls back to ⚠ with the reason.

Pass line: `30/30 + done`.

### 1b. Cold file under launchd — FAILS 2026-09-30 02:23 UTC (open)
After the review fixes the job re-ran on W39, which Drive had evicted again (0 KB on disk): `cat` → "Resource deadlock avoided". A one-off launchd test confirmed it: an already-downloaded file (W38) reads fine; a cloud-only one (W39) does not. **A background job cannot make Drive for Desktop download a file.** Setting `com.apple.fileprovider.pinned#PX` on the folder had no effect and was removed. Fix: Ty set the inbox folder to "Available offline" (one-time, 2026-09-30), so the job only reads local files.

### 1c. Job renders with the folder offline — PASS 2026-09-30 02:41 UTC
Drive downloaded the folder (W39 on disk in 120 s, folder ~1,9 GB). launchd run, no manual step: `rendered ELA-2026-W39: 30 of 55 pages`; `done` = `pages_rendered=30 source_pages=55 source_bytes=141917085`; folder `_pages/ELA-2026-W39-141917085/`. Installed script sha256 = repo script sha256 (`14f381094ba3…`).

Pass line: `30/30 + done`, no human step.

## 2. Cloud run reads the images — PASS 2026-09-30 02:17–02:19 UTC
Test routine (read-only): found `_pages/ELA-2026-W39/`, `done` present, 30 images p-01…p-30. Downloaded p-03 (137,274 B, size matches Drive) and p-16 (152,775 B), and read:
- p-03 "Thông tin chung": 2.408 · 160 · 21 · Eco Bazaar 54/66 + PK1 05/198 · 57 · 1.430
- p-16 "Công tác nghiệm thu bàn giao": PK1 lần 1 90/198, PK1 đã nhận 59, PK3 đã nhận 21
All equal the hand-read W39 values published in `data/weeks/2026-W39.json`.

Pass line: all values match.

### 2b. Cloud run follows the byte-keyed lookup — PASS 2026-09-30 02:46–02:47 UTC
Test routine, read-only, runbook 4a as written: `ELA-2026-W39.pdf` fileSize 141917085 → `_pages/ELA-2026-W39-141917085/` found by exact title → `done` read (`pages_rendered=30 source_pages=55 source_bytes=141917085`, bytes match) → `p-03.jpg` (137,274 B) and `p-16.jpg` (152,775 B) looked up by exact title, base64 decoded from the spill file, sizes match Drive. Values: 2.408 · 160 · 21 · Eco Bazaar 54/66 + PK1 05/198 · 57 · 1.430; PK1 lần 1 90/198, PK1 đã nhận 59, PK3 đã nhận 21 — all equal the hand-read W39.

Pass line: all values match.

## 3. Scheduled run — pending, Sun 2026-10-04 21:00 Hanoi
