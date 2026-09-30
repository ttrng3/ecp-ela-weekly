# Intent: correct two stale comments

**Status:** draft
**Source:** chat (peer session tytr3-ff for `.pages-allow`; this session's handoff debt for `tools/ela-pages.sh`), 2026-09-30

**Problem.** (1) `.pages-allow`'s header says every run is a dry run until Pages is set to GitHub Actions. Pages has built from Actions since 2026-09-29 (`build_type: workflow`; the last 3 runs on 2026-09-30 deployed green). (2) The comment above the `cat` copy in `tools/ela-pages.sh` says a plain byte stream hydrates a cold Drive placeholder. `verification/ela-page-images.md` records that from launchd `cat` fails too.

**Outcome.** Both comments state what is true. No line that the workflow or the script executes changes.

**Who and what is affected.** Readers of the two files. The Mac helper's installed copy is re-copied after merge so its sha matches main.

**Constraints.** Comments only. No `.pages-allow` path line changes. Wording of (1) matches the other 7 Pages repos.

**Open questions.** none known
