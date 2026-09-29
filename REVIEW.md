# REVIEW.md

What the reviewer agent (`agents/reviewer.md` in claude-config) checks on every PR to this repo. The three passes run in order, each in full. The last section holds this repo's own rules.

This file is never served: it is not in `.pages-allow`.

## Severity
- **Critical:** it will break something live or publish something it must not. A secret or token, personal data by value in a public repo, a newly served path that shouldn't be, a broken deploy, data loss, a gate bypass.
- **High:** wrong behaviour that will show up. A bug on a path that runs, a broken reference, a diff that does something other than what the PR says, a house rule broken in a way Ty would have to undo.
- **Medium:** it's wrong but contained. An edge case that isn't hit yet, a doc that disagrees with the code, a missing test for a changed behaviour.
- **Low:** clarity, naming, a stale comment.

When unsure between two levels, pick the higher one and say why.

## Pass 1: Bugs
- [ ] Logic: off-by-one, inverted condition, wrong variable, an unreachable branch, loop bounds.
- [ ] Edge cases: empty input, a missing file, a first run, a name with spaces or accents, a timezone (Hanoi is UTC+7; cron is UTC).
- [ ] References resolve: every path, heading anchor, script flag, workflow job name and file named in the diff exists in `files/` or in the base.
- [ ] Shell: quoting, `set -e` interactions, `$?` after a pipe, BSD vs GNU flags (the Mac runs BSD tools).
- [ ] Syntax: YAML, JSON, Python (3.9 on the Mac: no `match`, no `X | Y` types), HTML.
- [ ] The diff does what the PR description says, and nothing it doesn't say.

## Pass 2: Security
- [ ] Secrets by pattern: `ghp_`, `github_pat_`, `sk-`, `sk-ant-`, `AKIA`, `xox[bp]-`, private-key headers, `eyJ…` JWTs (a Supabase **service_role** JWT is always Critical), passwords in URLs, `?token=`/`?key=` in a link.
- [ ] Personal data **by value** in a public repo: a name with money, a phone number, an email address, an account number, an ID number. Referring to where the value lives is fine; the value itself isn't.
- [ ] Anything newly published: a path added to `.pages-allow`, or any new file in a repo still on legacy Pages.
- [ ] Workflow permissions widened (`permissions:`, `pull_request_target`, `secrets: inherit`), or a new third-party action not pinned to a sha.
- [ ] Test fixtures build fake secrets at run time; a token-shaped string typed into a file is a finding even if it's fake.

## Pass 3: House rules
- [ ] **Never by value:** a sensitive value is referenced, not quoted, in any file of a public repo, including `work/` docs.
- [ ] **Artifact mirror contract:** no Cowork preview URL and no artifact id in anything public or anything Ty is shown. (A registry row that records an id on the private Drive mount is the exception.)
- [ ] **Entity separation:** OMNI and ECOPM data, names and numbers never cross into each other's repo or page.
- [ ] **One change per `work/` folder:** the PR names its `work/<yymmdd>-<slug>/`; `intent.md` says accepted; `spec.md` says approved; the diff matches the spec's promise, with nothing extra.
- [ ] **`gate/` untouched** while it is frozen (until 2026-10-05).
- [ ] **One PR per merge command:** nothing in the diff merges or batches PRs (`gh pr merge` in a loop, the merge API).
- [ ] **Verify before you assert:** every number in a doc or page has a source named beside it or in its section.

## Repo-specific rules
Rules specific to ecp-ela-weekly. **Every standing ruling in the README and in `docs/weekly-refresh.md` (the runbook, which outranks the routine prompt) applies as well; a PR that breaks one is at least High, and Critical where a line below says so.** The lines below are the ones most often at risk.

- **The renderer holds no data.** `index.html` fetches `data/` at load (README, "How this repo is the source of truth"). A number, a week or a KPI typed into `index.html` is High.
- **What a refresh writes.** Only `data/.last-check`, `data/index.json` and `data/weeks/W<N>.json`. A refresh never writes the stylesheet (README, "Visual standard"); mixed into a data change, a style change is High.
- **Deltas are computed, never copied.** Every Δ is recomputed in code from the two weeks' values (runbook, step 5). A delta copied from a report is High.
- **Report, don't fake.** An unreadable figure keeps last week's value, carries the label `⚠ chưa cập nhật (nguồn ảnh/quá lớn) — cần xác nhận thủ công`, and is listed by name (runbook, step 4). An inferred number, or a carried value without that label, is High.
- **The manifest stays consistent.** A new week sets `current` and is added to `weeks` (runbook, step 5), and every listed week needs its `data/weeks/W<N>.json`. A broken manifest is High.
- **The heartbeat stays.** A quiet week is normal here, so `data/.last-check` is what tells a quiet week from a dead routine (README, "Why the heartbeat matters here more than anywhere else"). A diff that stops writing it, or removes `freshness-check.yml`, is High.
- **Retired, do not restore** (runbook, "Retired"): the `archive/status_<date>.html` series, the Drive standalone-HTML handoff, the Drive PAT and token-in-URL pushes, and artifact-first publishing. Bringing any back is High; a token in any file is **Critical**.
- **The Artifact tool is attached: call it directly** (runbook). A routine instruction that makes the mirror step depend on a ToolSearch hit is High.
- **Light only, ruled 2026-09-24 by Ty.** No dark theme; any new colour is a token, never a raw hex (README, "Visual standard").
- **One address, one preview.** `https://ttrng3.github.io/ecp-ela-weekly/` is the only link. A Cowork preview URL or artifact id anywhere in the repo is **Critical** (the repo is public).
- **Don't widen what is published.** A new path in `.pages-allow`, or a new kind of data in `data/`, is High and needs Ty. (Carried from Omni-TMDV's REVIEW.md; not stated in this repo's own files.)
- **Entity separation.** The template rule in Pass 3 applies. This repo's files don't say which entity owns it (it covers Eco Central Park, Vinh, and Eco Retreat, Long An), so until Ty rules, data from another project or entity is at least High and flagged for Ty.
