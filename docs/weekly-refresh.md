# ECP × ELA weekly refresh runbook

Canonical. If the routine prompt and this file disagree, **this file wins**.

## Runs where?

Any cloud session with the Google Drive connector and the GitHub MCP file
tools. Both are account-level, so this runs with the Mac shut.

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

### 1. Heartbeat, always, before anything else

Write `data/.last-check` — one line, current UTC as `%Y-%m-%dT%H:%M:%SZ`, a
space, then `newest-source=<what you found>` — and commit it, even when there is
no new report.

This matters more here than on the other dashboards, because a quiet week is
**normal**: ECP and ELA file on their own cadence and some weeks are missing
outright. Without the heartbeat, "no new report" and "the routine died" look
identical from outside. It also exercises the GitHub write path every week.

### 2. Find the newest weekly reports

Since 2026-09-29 both projects' reports live in **one** Drive folder:
`Claude Workspace/00 Inbox/Weekly Reports ECP-ELA/`. Search it by its folder
id, which the routine prompt holds (this repo is public, so the id is not
written here). The id survives the folder being renamed or moved, and a path
does not. The old `01 Eco Central Park - ECP/07 Weekly Reports/` and
`02 Eco Retreat Long An - ELA/07 Weekly Reports/` folders no longer exist.

Naming, for the source PDFs Ty saves from Zalo:

- ECP — `ECP-W<N>.pdf` (e.g. `ECP-W39.pdf`)
- ELA — `ELA-W<N>.pdf` (e.g. `ELA-W39.pdf`)

Be tolerant when reading **inside that folder only**. A file may still arrive
under its Zalo name. Match the project from `ECP`, `Eco Vinh` or
`Eco Central Park` / `Central Park` (→ ECP), and from `ELA`, `Long An` or
`Eco Retreat` (→ ELA). Match the week from `W<N>`, `Week <N>` or `Tuần <N>`
(with or without a hyphen). Skip `.docx` outputs and anything matching
`Layout vận hành` / `Layout kinh doanh`. A PDF that fits neither project, or
fits both, is listed in the report and not used.

If the folder returns no PDFs at all, **do not search Drive-wide and do not
write `data/weeks/`**. Commit the heartbeat with `newest-source=inbox-empty`,
report the folder as empty or unreachable, and stop.

Ignore duplicates suffixed `(1)` or ` 2`. Find the newest `N` on each side and
the week before it, for the WoW comparison.

### 3. Stop if nothing is new

If `data/index.json`'s `current` already equals the newest week on both sides,
commit just the heartbeat, report "chưa có báo cáo tuần mới", and finish. Do
not touch the week file.

### 4. Extract — and report rather than fake

**ECP's report is usually an image-only PDF with no text layer. ELA's runs
100–130 MB.** If a figure cannot be read this run:

- keep the previous week's value,
- label it `⚠ chưa cập nhật (nguồn ảnh/quá lớn) — cần xác nhận thủ công`,
- and list the exact missing indicators in the notification.

Never infer, never carry a number forward silently.

Indicators — **ECP**: khách tham quan CV, khách khu vui chơi, hộ cư dân về ở,
bàn giao thấp tầng x/1657, Central Park Residences x/620, căn thi công về ở.
**ELA**: khách tham quan KĐT, khách khu vui chơi, nhân sự BQL, nhà thầu thi
công, bàn giao Eco Bazaar x/66, khai trương x/66, nghiệm thu PK1/PK3/PK4.

### 5. Write two files via the GitHub MCP file tools

`get_file_contents` for the current blob sha, then `create_or_update_file` on
`main`. Shell `git push` can be refused by the auto-mode classifier in an
unattended run; the MCP calls are not, so they are the primary path. **No PAT,
no token-in-URL** — the old routine read a PAT from Drive and pushed with it;
that is retired.

- `data/weeks/W<N>.json` — the whole briefing for that week. Recompute every Δ
  in code; do not copy a delta from the report.
- `data/index.json` — set `current` to the new week, add it to `weeks`, set
  `generatedUtc` to now.

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
