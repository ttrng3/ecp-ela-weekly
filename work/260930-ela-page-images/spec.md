# Spec: ela-page-images

**Intent:** accepted 2026-09-30 · **Status:** draft

## Requirements
1. In runbook step 4, when a source PDF returns empty text, the run downloads it through the Drive connector and renders pages to images (`pdftoppm`, installed with `apt-get install -y poppler-utils` if missing). *(Outcome)*
2. It finds the needed slides by their titles and reads the figures from the images: "Thông tin chung" (6 KPIs), "Eco Bazaar – cập nhật tiến độ" (BQL→BKD), "Công tác nghiệm thu bàn giao" (PK1/PK3), "Công tác bàn giao nhà" (khách nhận), "Khảo sát và đánh giá tiến độ xây dựng" (PK4). *(Outcome; open question 3)*
3. Figures read this way are labelled "đọc từ ảnh trang" in the legend, and `sourceNote` names the page numbers. A slide it cannot find or read falls back to ⚠, as today. The report lists the pages read. *(Outcome; "Report, don't fake")*
4. If the download fails or the renderer can't be installed, the run falls back to ⚠ and says which step failed. It never searches Drive-wide or mounts a machine. *(Constraints)*
5. Contradictions inside a deck (e.g. summary vs detail slide) are flagged ⚠ with both values, never resolved by the run. *(Constraints)*

## Design
`docs/weekly-refresh.md` step 4 gains a sub-step "No text layer: read the page images" with the slide list above, the render command (`pdftoppm -r 50 -jpeg`), a scan limit, and the fallback. The routine prompt's STEP 4 line about ELA being "the real blocker" changes to point to that sub-step. No change to data shape, renderer or stylesheet.

## Conflicts
Loaded: kernel `CLAUDE.md` ("Strategic objective" — cloud-only, "Drift detection"), artifact mirror contract, entity separation, repo `REVIEW.md`, secure-pages. Not loaded: ty-report-standard / apple-design (no visual change).

| Rule (by name) | What in the design breaks it | Resolution, or question for Ty |
|---|---|---|
| "Strategic objective" — unattended, Drive connector only | A 140 MB download and a package install inside the cloud run are unproven. | **Feasibility test before building** (Promise 1). If either fails, the fallback stays ⚠ and this spec is revised. |
| "Report, don't fake" | Image reading can misread. | Label + page numbers + ⚠ on anything unread; checked against a known week (Promise 2). |
| Scope: known slides vs whole deck | **Ty's call (open question from the intent):** known slides (search the first 25 pages for the 5 titles; recommended: fast, and a missing slide is reported, not guessed) or scan every page each week. | — |
| Run time / cost | Rendering and reading ~10 images adds minutes to a weekly run. | Acceptable at one run a week; stated in the runbook. |

## Security
Same repo, same result as 2026-09-30: secrets 0 (tree and history), PUBLIC — PASS, Pages allowlist unchanged, Supabase N/A. The downloaded PDF stays in the run's `/tmp` and is never committed. Verdict: safe to ship.

## Promise
1. **Feasibility, before building:** a one-off test routine (or a hand-fired run with a test prompt) downloads `ELA-2026-W39.pdf` via the Drive connector and runs `pdftoppm` on page 3. Pass line: `downloaded 141917085 B, rendered p.3`.
2. **Accuracy:** a hand-fired run against W39 produces ELA values equal to the hand-read W39 (2.408 · 1.430 · 58 · 57 · 160 · 21 · PK1 90/198 & 59 · PK3 66/68 & 21 · PK4 31). Pass line: `11/11 match`.
3. **Scheduled:** the Sun 2026-10-04 run reports the pages it read and writes no ⚠ except the flagged contradictions.

## Out of scope
Asking ELA for a text-layer export (a separate human request); ECP (its PDF has text); any page redesign.
