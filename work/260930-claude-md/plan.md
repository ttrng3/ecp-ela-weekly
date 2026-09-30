# Plan — CLAUDE.md for this repo

1. Write `CLAUDE.md` from the umbrella spec's shape, using Omni-sitecheck PR 7 as the model.
2. Run every listed command once (results below).
3. Grep the file for the folder id, the preview id and any mount path or email: 0 hits.
4. Reviewer pass on the PR; fix or dispute each finding; Ty ships.

## Commands run 2026-09-30
- manifest check (current in weeks + every week file exists): passes
- `python3 tools/build-fragment.py /tmp/ecp-frag.html`: exit 0, 14,206 bytes; re-run as listed (no argument): writes `build/artifact.html` (tracked), 14,206 bytes, `git status` clean (byte-identical to main)
- `python3 tools/reconcile.py data <copy>`: IN SYNC, exit 0
- `python3 .github/scripts/freshness.py`: exit 0, `stale=false`
- `python3 .github/scripts/test_freshness.py`: 6/6 ok, exit 0
- `bash -n tools/ela-pages.sh`: ok · `plutil -lint tools/com.ty.ela-pages.plist`: OK

## Promise (from the umbrella spec)
The next scheduled run (Sun 2026-10-04, 21:00 Hanoi) behaves as the previous one: same steps, same files written. Recorded in `verification/claude-md.md` after that run.
