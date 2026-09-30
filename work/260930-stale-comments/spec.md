# Spec: stale-comments

**Approved:** 2026-09-30

**Intent:** accepted 2026-09-30 · **Status:** approved

## Requirements
1. `.pages-allow` header lines 8–9 say Pages runs from Actions since 2026-09-29 and when a run would be a dry run (intent Problem 1).
2. `tools/ela-pages.sh` copy comment says cat-to-temp-plus-size-check, and that from launchd neither cp nor cat reads a cloud-only file (intent Problem 2).

## Design
Two comment edits. `bash -n` on the script; no path line in `.pages-allow` touched.

## Conflicts
None found (loaded: REVIEW.md "Don't widen what is published" — no path added).

## Security
Public repo; no personal data, id or path value added.

## Promise
After merge: the next Pages run on main is green and the live site is unchanged; `shasum` of `~/.local/bin/ela-pages.sh` equals main's after re-copy. Checked the same day.

## Out of scope
Any behaviour change to the workflow or the helper.
