# ECP × ELA weekly refresh runbook

Canonical. If the routine prompt and this file disagree, **this file wins**.

## Runs where?

Any cloud session with the Google Drive connector and the GitHub MCP file
tools. Both are account-level, so this runs with the Mac shut.

**One exception:** ELA's figures come from page images that a Mac helper
renders (step 4a). It needs the Mac awake some time between ELA filing and the
run, and the inbox folder set to "Available offline" in Google Drive (a
background job cannot make Drive download a cloud-only file). Its log is
`~/Library/Logs/ela-pages.log` on the Mac. If the helper has not run, the run
still works, but ELA's figures get ⚠ with that reason.

## The Artifact tool is attached: call it directly

The routine prompt says to call ToolSearch for any tool that isn't in the
immediate tool list "before concluding it is unavailable". **For the Artifact
tool that is wrong, and this file overrides it.** The Artifact tool is
attached to this routine: it's in the routine's allowed tools. An attached tool
never shows up in ToolSearch, which finds only deferred tools, so a ToolSearch
miss is exactly what an attached tool looks like. It is not evidence that the
tool is absent. Call it directly for the mirror step. Only an error returned by
the tool itself means it is unavailable, and then the mirror step reports that
error and stops, as the prompt says. (2026-09-27: the TMDV routine searched,
missed, reported "no Artifact tool" and skipped its mirror. The routines whose
prompts say "call it directly" keep their previews in sync.)

## Steps

### 1. Heartbeat, every run, as the first write

Write `data/.last-check` — one line, current UTC as `%Y-%m-%dT%H:%M:%SZ`, a
space, then `newest-source=<value>` — and commit it, even when there is no new
report. It is the **first write** of the run, and there is **exactly one**
heartbeat commit per run. Do the step 2 search first (it only reads), then
commit the heartbeat before any `data/weeks/` or `data/index.json` write. If
the Drive call errors or has not returned after 5 minutes, **do not
retry**: commit the heartbeat as `inbox-unreachable` at once and stop (step 3).
The next scheduled run tries again. This keeps one heartbeat per run and
leaves a heartbeat even when the Drive step hangs.

`newest-source` is one of:

- `ECP-<YYYY>-W<NN>/ELA-<YYYY>-W<NN>` — the newest file found on each side, e.g.
  `ECP-2026-W39/ELA-2026-W38`. A side with no file at all is `none`.
- `inbox-unreachable` — the Drive call failed (wrong id, access revoked, connector error).
- `inbox-empty` — the call worked but no PDF matched either project.

`freshness.py` raises the stale-data issue on `inbox-unreachable`,
`inbox-empty` and `ECP-none/ELA-none`.

This matters more here than on the other dashboards, because a quiet week is
**normal**: ECP and ELA file on their own cadence and some weeks are missing
outright. Without the heartbeat, "no new report" and "the routine died" look
identical from outside. It also exercises the GitHub write path every week.

### 2. Find the newest weekly reports

Since 2026-09-29 both projects' reports live in **one** Drive folder:
`Claude Workspace/00 Inbox/Weekly Reports ECP-ELA/`. Search it by its folder
id, which the routine prompt holds (this repo is public, so the id is not
written here). The old per-project `07 Weekly Reports/` folders no longer
exist. Never search Drive-wide.

**Standard name:** `ECP-<YYYY>-W<NN>.pdf` / `ELA-<YYYY>-W<NN>.pdf`, week
zero-padded, e.g. `ECP-2026-W39.pdf`.

**Zalo names are still read.** Skip `.docx` files and `Layout vận hành` /
`Layout kinh doanh`. A title ending ` (1)` or ` 2` is a duplicate **only if** a
file with the same title minus that suffix is also in the folder (so
"Tuần 2.pdf" is not skipped). **Every skipped PDF is listed in the report.**
Normalise every title to Unicode NFC first. Match the project tokens below as
whole words, case-insensitive. A week token
may be followed directly by its digits (`W38`, `Tuần38`) or by a space or
hyphen (`Tuần 38`, `Tuần-38`). For the rest:

- **Project:** `ECP`, `Eco Vinh`, `Eco Central Park` or `Central Park` → ECP;
  `ELA`, `Long An` or `Eco Retreat` → ELA.
- **Week:** the number after `W`, `Week`, `Tuần` or `Tuan`.
- **Year:** from the name. If the name has none, the year of the file's Drive
  `createdTime`, except: a week ≥ 50 created in January belongs to the year
  before, and a week ≤ 2 created in December belongs to the year after.
- A file matched this way is used, and **listed in the report** so Ty can
  rename it. A PDF with no project, both projects or no readable week is
  listed and not used.

Order every week by (year, week). `current` in `data/index.json` is either
`"2026-W39"` or, for the two older keys, `"W37"` / `"W38"`, which are 2026.

### 3. Publish only a week both projects have filed

The **new week** is the newest (year, week) that has a file on **both** sides
and is newer than `current`. A week only one project has filed is never
published on its own (Ty, 2026-09-29: "wait for both").

- **Drive call fails** → heartbeat `inbox-unreachable`, report it as a failure
  in the first line, stop.
- **No PDF matched either project** → heartbeat `inbox-empty`, list the titles
  seen, stop.
- **No new week** → the heartbeat is the only write. Report "chưa có báo cáo
  tuần mới — đang chờ <ECP|ELA|cả hai> Tuần <NN>", naming the side(s) behind,
  and stop.
- **New week found** → go on to step 4 with that week's two files.

**WoW baseline** is the published week, `data/weeks/<current>.json`, not a
second PDF. If the new week is not the one right after `current` (a side
skipped a week), the new file's `prev` names the week it compares with, and
the report says which weeks were skipped.

### 4. Extract — and report rather than fake

**ECP's report has a text layer (ECP-2026-W39.pdf: 3,515,692 B, Drive listing
2026-09-29); read it as text. ELA's decks are slides exported as images
(100–165 MB for the W33–W39 decks, Drive listing 2026-09-29): no text, and the
Drive connector refuses downloads over 10 MB.**

#### 4a. Image-only PDF: read the pages as images

**Under 10 MB:** download it with the connector and render it in the sandbox
(`pdftoppm -r 60 -jpeg -f 1 -l 30`), open the rendered images with the Read
tool, and go on at the slide list in 2.

**Over 10 MB:** a Mac helper (`tools/ela-pages.sh`, launchd, hourly) renders
pages 1–30 of every new PDF over 10 MB into the inbox subfolder
`_pages/<file stem>-<file bytes>/` as `p-01.jpg` … `p-30.jpg` (~140 KB each, W39
render 2026-09-30)
and writes `done` last (`pages_rendered`, `source_pages`, `source_bytes`). The
byte count in the folder name must equal the PDF's current `fileSize`; a
re-filed report gets a new folder.

1. List `_pages/<stem>-<bytes>/` inside the inbox folder with the Drive
   connector. No folder, or no `done` → the pages are not ready: fall back to
   4b with the reason "Mac render job has not run".
2. Download the images (each is under 10 MB) and open them with the Read tool.
   The connector returns an image as base64 that overflows the tool result and
   is saved to a side file; decode it there
   (`jq -r .content <file> | tr -d '\n' | base64 -d > /tmp/p-NN.jpg`) and check
   the byte size against Drive's `fileSize`. Look pages up by exact title
   (`title = 'p-03.jpg'`): the folder listing's page tokens can overlap.
   Find these slides by title, not page number (it moves week to week):
   - "Thông tin chung": khách tham quan KĐT, nhân sự BQL, nhà thầu thi công,
     báo cáo bàn giao, căn đang hoạt động kinh doanh, khách khu vui chơi
   - "Eco Bazaar – cập nhật tiến độ": bàn giao BQL → BKD
   - "Công tác nghiệm thu bàn giao": PK1 / PK3 (lịch QLXD, lần 1, lần 2,
     chuyển bước, đã nhận)
   - "Công tác bàn giao nhà": thư mời / đã nhận nhà
   - "Khảo sát và đánh giá tiến độ xây dựng": PK4
3. Label every figure read this way "đọc từ ảnh trang" in the legend and name
   the page numbers in `sourceNote`. When two slides disagree (e.g. summary
   54/66 vs detail 58), show both and mark ⚠; don't pick one. A slide not found
   → ⚠ for its figures, saying "not in the first 30 of N pages" (N from
   `done`) when the deck is longer than 30.

#### 4b. When a figure still cannot be read

- keep the previous week's value,
- label it `⚠ chưa cập nhật (nguồn ảnh/quá lớn) — cần xác nhận thủ công`,
- and list the exact missing indicators, and why, in the notification.

Never infer, never carry a number forward silently.

Indicators — **ECP**: khách tham quan CV, khách khu vui chơi, hộ cư dân về ở,
bàn giao thấp tầng x/1657, Central Park Residences x/620, căn thi công về ở.
**ELA**: khách tham quan KĐT, khách khu vui chơi, nhân sự BQL, nhà thầu thi
công, bàn giao Eco Bazaar (BQL→BKD) x/66, căn đang hoạt động kinh doanh,
nghiệm thu PK1/PK3/PK4.

### 5. Write two files via the GitHub MCP file tools

`get_file_contents` for the current blob sha, then `create_or_update_file` on
`main`. Shell `git push` can be refused by the auto-mode classifier in an
unattended run; the MCP calls are not, so they are the primary path. **No PAT,
no token-in-URL** — the old routine read a PAT from Drive and pushed with it;
that is retired.

- `data/weeks/<YYYY>-W<NN>.json` (e.g. `2026-W39.json`) — the whole briefing
  for that week. Its `week` field stays the display label ("Tuần 39"). Recompute
  every Δ in code; do not copy a delta from the report. Never overwrite an
  existing week file.
- `data/index.json` — set `current` to `"<YYYY>-W<NN>"`, add
  `"<YYYY>-W<NN>": "<YYYY>-W<NN>"` to `weeks`, set `generatedUtc` to now. The
  renderer resolves `weeks[current]` to the file name, so `index.html` does not
  change.

### 6. Verify, do not assume

Confirm `main` moved using the sha the write returned. Say plainly if you could
not reach the live site rather than claiming a success you did not observe.

### 7. Report

Three lines: the week updated per project plus 2–3 notable WoW moves; any
indicator that could not be extracted and needs Ty to confirm; and the write
result (commit sha and which path). No unmarked number in a
conclusion.

## Retired — do not restore

- The `archive/status_<date>.html` series.
- The Drive standalone-HTML handoff at `93 Knowledge Base/Claude outputs/Weekly Status/`.
- The PAT at `93 Knowledge Base/_tools/gh_ecpela_pat.txt` and token-in-URL pushes.
- Editing an artifact first and mirroring it to GitHub. The repo leads now.
