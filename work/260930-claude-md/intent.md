# Intent — CLAUDE.md for this repo (accepted)

**Status:** accepted 2026-09-30 (covered by the umbrella spec below)
**Source:** claude-config `work/260930-claude-md-per-repo/spec.md` (branch `work/260930-claude-md-per-repo`), approved by Ty 2026-09-30 in chat. Its scope names this repo and routes it to this repo's owner session.

**Problem.** This repo's traps (image-only ELA decks, the Drive download limit, the offline requirement, contradictory slides, legacy week keys, the blank-preview trap) live in session memory, not in the repo, so a new session starts without them.

**Outcome.** A `CLAUDE.md` at the repo root, at most 45 lines, in the umbrella spec's shape: header, routine line, commands, layout, rules, dated known mistakes with in-repo sources.

**Who and what is affected.** Sessions working in this repo. The weekly routine loads the file but is told it adds no step; its runbook and README outrank it.

**Constraints.** No run step that isn't already in the runbook. Every listed command run once before the PR. No folder id, mount path, preview URL, artifact id or personal data (public repo). OMNI only.

**Open questions.** none known
