# Spec: ela-w39-page-read

**Approved:** 2026-09-30

**Intent:** accepted 2026-09-30 · **Status:** approved

## Requirements
1. `data/weeks/W38.json` ELA: 6 KPIs, PK1/PK3/PK4, "done" and the ELA action and KSNB lines carry the W38 deck's figures (19/09), each Δ vs published W37. *(Outcome)*
2. `data/weeks/2026-W39.json` ELA: the same, from the W39 deck (26/09), each Δ vs requirement 1's W38 values. *(Outcome)*
3. Every Δ can be recomputed from the two published week files, except "Căn đang hoạt động kinh doanh" W37 = 30, which has no W37 field; its source (W37 deck p.3) is written beside it. *(Constraints: "Deltas are computed")*
4. The legend labels ELA figures "đọc từ ảnh trang"; ⚠ marks only the two contradictions (W38 visitors = W37; Eco Bazaar 54 vs 58). *(Outcome)*
5. "Khai trương x/66" is replaced by "Căn đang hoạt động kinh doanh"; the definition question stays in the DECIDE item. *(Constraints)*
6. After merge, the Cowork preview gets both files (by hand; the routine mirrors only on its own runs). *(artifact mirror contract)*

## Design
Two JSON files, edited in place, same shape (no new fields). Sources, verified by rendering pages (`pdftoppm -r 50`) and reading them, 2026-09-29/30:
- W37 deck (12/09) p.3: 3.918 · 152 · 30 · 58/66 · 30 căn KD · 240 — matches published W37 6/6.
- W38 deck (19/09) p.3: 3.918 · 160 · 25 · 54/66 · 36 · 170; p.9: 58; p.16: Hội thảo/Trung thu; p.19: PK1 84/198, 70/84, 70, 37; PK3 68/121, 66/68, 53/68, 46, 15.
- W39 deck (26/09) p.3: 2.408 · 160 · 21 · 54/66 + PK1 05/198 · 57 · 1.430; p.9: 58; p.16: PK1 84/198 lịch, 90/198, 70/90, 70, 59; PK3 unchanged, 21; p.19: 24 thư mời, 5/24 nhận; p.21: PK4 31.

## Conflicts
Loaded: kernel `CLAUDE.md` (incl. "Weekly reports → `00 Inbox/Weekly Reports ECP-ELA/`", "File operation safety", "Drift detection"), artifact mirror contract (memory), entity separation, repo `REVIEW.md` rules, secure-pages. Not loaded: ty-report-standard / apple-design (no page or visual change).

| Rule (by name) | What in the design breaks it | Resolution, or question for Ty |
|---|---|---|
| "Report, don't fake" (REVIEW.md) | Image reading can misread a digit. | Method checked on W37 (6/6). Every figure's slide is named in `sourceNote`; the two conflicting figures stay ⚠. |
| "Deltas are computed, never copied" (REVIEW.md) | The "hoạt động KD" W37 value (30) is not in `W37.json`. | Written beside the Δ with its slide; W37.json not edited (out of scope). |
| "What a refresh writes" (REVIEW.md) | A correction to a past week (W38), not a new-week refresh. | Only `data/weeks/*.json`; no manifest change; named here. |
| Artifact mirror contract | The preview shows the old figures until mirrored. | Requirement 6: mirror by hand after merge, read back. |
| Entity separation | none (same ECP/ELA data already on the page) | none |

## Security
```
## Security (secure-pages, 2026-09-30)
1 Secrets ........ PASS (tree 0, history 0)
2 Visibility ..... PUBLIC — PASS; same kind of operating figures the page already publishes
3 Pages .......... PASS; workflow deploy, allowlist index.html, data/index.json, data/weeks/*.json
4 Supabase ....... N/A
Verdict: safe to ship
```

## Promise
Measured on merge day, recorded in `verification/ela-w39-page-read.md`:
1. `python3 -c` recomputes every ELA Δ in W38 (vs W37.json) and W39 (vs W38.json) from the files; pass line `all ELA Δ recompute` (the one sourced exception listed).
2. `grep -c "chưa cập nhật (nguồn ảnh" data/weeks/W38.json data/weeks/2026-W39.json` → `0` and `0`.
3. The preview's `data/weeks/W38.json` and `2026-W39.json` equal `main`'s (sha256 match).

## Out of scope
The routine change (`work/260930-ela-page-images/`); W37.json; any renderer or stylesheet change.
