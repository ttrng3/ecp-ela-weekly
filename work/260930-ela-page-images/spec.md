# Spec: ela-page-images

**Approved:** 2026-09-30 (original design; superseded below)
**Revision 2:** 2026-09-30, after the feasibility test — **pending Ty's approval**.

**Intent:** accepted 2026-09-30 (constraint amended, pending) · **Status:** draft (revision 2)

## What the test showed
Test routine run 2026-09-29 17:09 UTC: `download_file_content` on ELA-2026-W39.pdf → "File too large for download, over limit of 10 MB". `pdftoppm` is already installed in the cloud sandbox. So the cloud run can render and read images, but cannot fetch a 126–165 MB PDF.

## Options checked (every path, before asking Ty)
| Path | Human step | Result |
|---|---|---|
| Drive connector download | none | ✗ 10 MB cap (tested) |
| Drive connector text read | none | ✗ empty (no text layer) |
| Cloud run calls the Drive API directly (no cap) | **one-time**: Ty creates a Google Cloud credential (only his login can) | ✓ fully cloud; held as the upgrade path |
| GitHub Action with the same credential | same one-time step; public repo logs | ✗ worse than the row above |
| ELA sends a text-layer PDF | a request to Long An each week | ✗ depends on another team |
| Ty saves screenshots | weekly human step | ✗ what Ty asked to avoid |
| **Mac helper renders pages into Drive; cloud run reads the images** | **none** | ✓ chosen: works this week, no credential, no weekly step |

## Requirements
1. A Mac background job (launchd, hourly) finds any PDF in the inbox over 10 MB that has no rendered pages yet, renders pages 1–30 to JPEG (`pdftoppm -r 60 -jpeg -jpegopt quality=80`), and writes them to `00 Inbox/Weekly Reports ECP-ELA/_pages/<file stem>/p-NN.jpg`, then a `done` marker last. Measured on W39: 30 pages, 5,4 s, 4,2 MB total, ~140 KB each.
2. It writes to a local temp folder first, copies to the Drive mount, and checks each copy's size before writing `done` ("File operation safety"). It never deletes, moves or renames anything.
3. The routine, when a source PDF is over 10 MB or returns no text, reads `_pages/<stem>/` through the Drive connector (each image is under 10 MB), finds the 5 known slides by title ("Thông tin chung", "Eco Bazaar – cập nhật tiến độ", "Công tác nghiệm thu bàn giao", "Công tác bàn giao nhà", "Khảo sát và đánh giá tiến độ xây dựng"), and reads the figures.
4. Figures read this way are labelled "đọc từ ảnh trang" with page numbers; contradictions inside the deck get ⚠ with both values; a slide not found gets ⚠. No `_pages/<stem>/done` yet → ⚠ with the reason "Mac render job has not run", as today.
5. Nothing changes for ECP (text PDFs).

## Design
- `tools/ela-pages.sh` (repo, no secrets: it names only the inbox path on the mount) + `tools/com.ty.ela-pages.plist` (launchd agent, StartInterval 3600, installed to `~/Library/LaunchAgents`).
- `docs/weekly-refresh.md` step 4 gains "Large or image-only PDF: read `_pages/<stem>/`".
- Routine prompt STEP 4 points to that sub-step.

## Conflicts
Loaded: kernel `CLAUDE.md` ("Strategic objective", "File operation safety", "Drift detection"), artifact mirror contract, entity separation, repo `REVIEW.md`, secure-pages.

| Rule (by name) | What in the design breaks it | Resolution |
|---|---|---|
| "Strategic objective" — no dependency on the Mac | The render step runs on the Mac: if it is off or asleep all weekend, ELA falls back to ⚠. | Flagged as debt. The fully cloud upgrade (Drive API credential, one-time Ty login) is recorded above; the rest of the design does not change when it lands. |
| "File operation safety" | The job writes new files onto the Drive mount. | Write-new-only, temp → copy → size check → `done` marker; no move/rename/delete. |
| "Report, don't fake" | Image reading can misread. | Label + page numbers + ⚠, as PR #6; checked against the hand-read W39. |
| Public repo | The script is public. | It holds no id, token or personal data; the folder id stays in the private prompt. |

## Security
Secrets: none added. The script holds a mount path only. Pages allowlist unchanged (`tools/` not served). Rendered images live in Drive, never in the repo. Verdict: safe to ship.

## Promise
1. **Mac job:** after install, within one hour `_pages/ELA-2026-W39/` exists with 30 images and `done`; sizes match the local render. Pass line: `30/30 + done`.
2. **Cloud read:** a hand-fired run of the test routine downloads `_pages/ELA-2026-W39/p-03.jpg` via the connector and reads the six "Thông tin chung" values. Pass line: `2.408 · 160 · 21 · 54/66 · 57 · 1.430`.
3. **Scheduled:** the Sun 2026-10-04 run publishes W40 with ELA read from images (or, if W40 is not filed on both sides, reports that and writes only the heartbeat).

## Out of scope
The Drive API credential (recorded as the upgrade path); ECP; asking Long An for text-layer PDFs.
