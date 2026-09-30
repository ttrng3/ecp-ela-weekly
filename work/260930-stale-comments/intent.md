# Intent: correct two stale comments

**Status:** accepted 2026-09-30
**Source:** chat (peer session tytr3-ff for `.pages-allow`; this session's handoff debt for `tools/ela-pages.sh`), 2026-09-30

**Problem.** (1) `.pages-allow`'s header says every run is a dry run until Pages is set to GitHub Actions. Pages has built from Actions since 2026-09-29 (`gh api repos/ttrng3/ecp-ela-weekly/pages` → `build_type: workflow`; `gh run list --workflow pages.yml`: runs 36664749468, 36667325818, 36695505698 on 2026-09-30, all success). (2) The comment above the `cat` copy in `tools/ela-pages.sh` says a plain byte stream hydrates a cold Drive placeholder. `verification/ela-page-images.md` records that from launchd `cat` fails too.

**Outcome.** Both comments state what is true. No line that the workflow or the script executes changes.

**Who and what is affected.** Readers of the two files. The Mac helper's installed copy is re-copied after merge so its sha matches main.

**Constraints.** Comments only. No `.pages-allow` path line changes. Wording of (1) is the sentence session tytr3-ff proposed for its Pages repos; as of 2026-09-30 it is not yet on any of their `main` branches, so no match is claimed.

**Open questions.** none known
