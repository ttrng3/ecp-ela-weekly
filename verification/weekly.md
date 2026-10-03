# Verification: the weekly briefing

## Promise

Every file https://ttrng3.github.io/ecp-ela-weekly/ serves (the page, `data/index.json`, every week file the manifest lists) is byte-identical to `main`, and the listed private files and one `work/` file answer 404. The manifest holds together: `current` is the last week listed, every week has its file, weeks run in (year, week) order, and the legacy `W37`/`W38` keys are kept. Every published week carries KPIs for both ECP and ELA, and every section exists for both (it may be empty) (wait-for-both, runbook step 3). The routine ran within its 9-day watchdog, its heartbeat line carries nothing after its value, and the data is under 24 days old. No storage link, email address, handle, Drive mount name or inbox folder id is served or tracked, and the other entity's name is not served. In the browser the current week renders both projects with no error. The Cowork preview carries the page fragment and either `main`'s data or the last run's. The repo and the site are public on purpose (README, Ty 2026-10-04).

## Clean state

```bash
cd ~/Projects/ecp-ela-weekly && git checkout main && git pull --ff-only
```
Run after a Sunday run (`0 14 * * 0` UTC = 21:00 Hanoi, per pipeline-wiring's `collect_status.py`) or after any merge, never during the run. Wait for a merge's Pages run to go green first (`gh run list -w "Pages (allowlist)" -L1`).

## Steps

1. **Repo and live site.** `python3 tools/verify_live.py --forbid "<entity name>" --forbid-anywhere "<inbox folder id>"` (quote each word: an unquoted multi-word name becomes several words) → exit 0 and `"pass": true`. The session that runs or launches this protocol reads the folder id from the routine prompt with `RemoteTrigger get` on the ECP × ELA routine. A runner without `RemoteTrigger` (the verifier agent) gets both words in its instructions from that session. Never write either word here. Without both flags, `no_forbidden_words` fails on purpose.
2. **Live page in Chrome.** Open https://ttrng3.github.io/ecp-ela-weekly/ and run the script under Invariants. Expected: all values true.
3. **Console.** Reload, then read errors for `TypeError|ReferenceError|Uncaught|SyntaxError`. Expected: none.
4. **Preview.** Find the preview by its title, **Điều Hành Vận Hành ECP × ELA** (exactly one artifact has it), with `Artifact list` (the runner may not have `RemoteTrigger get`; never write its id here). `Artifact list` its files, and `Artifact read` `index.html` (into the session's scratch folder, outside the repo, under a neutral name, byte for byte: no trailing newline added, no line-ending conversion, or the exact-tail check fails on a correct preview) and `data/index.json`. First `python3 tools/build-fragment.py && git diff --exit-code build/artifact.html; s=$?; git checkout -- build/artifact.html; echo "fragment-current=$s"` — only `fragment-current=0` passes: the committed fragment is current (CLAUDE.md: it is rebuilt and committed with any `index.html` change). The checkout leaves the tree clean either way. Then `python3 tools/preview_matches.py <saved index.html> build/artifact.html` → exit 0 and `"match": true`. If it fails on `main`'s copy, use `$c`'s (below): first `[ -n "$c" ] || echo "no routine commit found"` (stop the step if so), then `git show $c:build/artifact.html > <scratch>/frag.html` and `python3 tools/preview_matches.py <saved index.html> <scratch>/frag.html`. Expected files: `index.html` plus the data files `main` or the last run's commit holds, nothing else. Find that commit with `c=$(git log --first-parent --format='%h %s' -- data/index.json | /usr/bin/grep -v ' (#[0-9]*)$' | /usr/bin/grep -v '^[0-9a-f]* Merge ' | head -1 | cut -d' ' -f1)`. Each data file read (`data/index.json` and any week file; `index.html` is checked only by `tools/preview_matches.py`) has the sha256 of `main`'s copy (`shasum -a 256 <path>`) or `$c`'s (`git show $c:<path> | shasum -a 256`). If `$c` is empty (`[ -n "$c" ] || echo "no routine commit found"`), stop the step and report it; an empty `$c` would hash the index copy instead. Matching `$c` and not `main` means PRs changed data since the run: behind by design until the next run.

The run-time checks of each change stay where they are, and this protocol doesn't repeat them:
- `verification/inbox-weekly-folder.md`: the inbox, year names, wait-for-both at run time, and the preview mirror;
- `verification/ela-page-images.md`: ELA read from rendered page images;
- `verification/260930-heartbeat-rule.md`: the heartbeat line's shape.

## Invariants

Step 1 prints these verdicts, all of which must be true:
- `manifest_consistent`
- `weeks_ordered`
- `legacy_keys_kept`
- `both_projects_every_week`
- `served_equals_main`
- `private_not_served`
- `heartbeat_fresh` (≤ 9 days)
- `heartbeat_bare`
- `data_fresh` (≤ 24 days)
- `all_tracked_read`
- `no_personal_traces`
- `no_forbidden_words`

Step 2, in the page:
```js
window.confirm=()=>true; window.alert=()=>{};
await new Promise(r=>setTimeout(r,3000));
const idx=await fetch('data/index.json?v='+Date.now()).then(r=>r.json());
const w=await fetch(`data/weeks/${idx.weeks[idx.current]}.json?v=`+Date.now()).then(r=>r.json());
const kpis=[...document.querySelectorAll('#sections .kpi')].length;
JSON.stringify({loaded:!document.getElementById('sub').innerText.includes('Không nạp được'),
  current_week_shown:[...document.querySelectorAll('#sections h2')].some(h=>h.textContent.includes(w.week)),
  both_projects:!!document.querySelector('.ph.ecp')&&!!document.querySelector('.ph.ela'),
  kpis_match:kpis===w.kpis.ecp.length+w.kpis.ela.length,
  sections_rendered:document.querySelectorAll('#sections h2').length===4})
```
All of them must be true. The page has no week picker: it renders only `current`.

## Adversary

- **A stranger on the public page.** The page is public on purpose; nothing beyond the page and its data is. `private_not_served`: README, CLAUDE.md, REVIEW.md, the heartbeat, the runbook, the `tools/` files, every protocol in `verification/`, the preview build, the retired archive page, `freshness.py`, `.pages-allow` and one `work/` file found at run time all exist on `main` and answer 404. `no_personal_traces` reads every served and tracked file for storage links, email addresses, bare handles and the Drive mount folder name, which contains a personal account (CLAUDE.md, 30/09). `no_forbidden_words` keeps the other entity's name off what is served and the inbox folder id off every served and tracked file.
- **A week published with one project missing** (the rule is wait-for-both). `both_projects_every_week`: both sides carry KPIs, and every other section exists for both (it may be empty, as when one project has nothing to decide). In the page, `both_projects` and `kpis_match`.
- **A rename of the legacy keys, or a week out of order.** `legacy_keys_kept`, `weeks_ordered`.
- **A manifest pointing at a file that isn't there, or a `current` that isn't the newest.** `manifest_consistent`.
- **A routine that stopped running.** `heartbeat_fresh`. **A routine that runs but publishes nothing:** `data_fresh`.
- **A heartbeat that carries a folder-id fragment again** (a 30/09 run appended one). `heartbeat_bare` accepts only the stamp and the three value shapes of runbook step 1, so text glued on without a space fails too.
- **A preview a generation behind.** Step 4.

## Sanctioned substitutes

- The forbidden words are passed on the command line, so the list changes without a PR and the repo never names them. This proves those words are absent; it can't catch one nobody listed. Docs may name the other entity's label (REVIEW.md allows it), so `--forbid` reads served files only; `--forbid-anywhere` and the trace check read every tracked text file too (the script excepted from the trace check: it spells out the patterns).
- The preview can't be fetched by a script, so step 4 is done by the runner with `Artifact list` and `Artifact read`.

## Evidence

- The JSON from step 1 and the JSON from step 2.
- A screenshot (`save_to_disk: true`) of the page.
- For step 4: file names and hashes, and the JSON `tools/preview_matches.py` printed; never the preview's id, URL or raw `Artifact list` output (the PR is public).

## Not covered

- Whether a figure matches the deck it came from, or carries ⚠ where the deck contradicts itself (runbook 4a.3). That is read by eye against the PDFs.
- Whether a week that should have been published was (both projects filed but the run skipped it). The heartbeat's `newest-source` names what the run saw; compare it with the inbox by hand.
- The Mac helper and the inbox setting (`verification/ela-page-images.md` covers them).

## Traps

- The preview is published wrapped in the publisher's skeleton (`<!doctype html>` … `<body>` and `</body></html>`), so its bytes never equal the build's; a raw hash comparison failed on a correct preview on 2026-10-04 (as gdsh's did on 2026-10-02). `tools/preview_matches.py` removes exactly that skeleton: the head must hash to one of the two pinned known heads (537 and 355 bytes, both seen 2026-10-04), the tail must be exact. A new skeleton fails step 4 until it is pinned on purpose.
- Pages answers `cache-control: max-age=600` (`curl -sI`, 2026-10-04). A `served_equals_main` failure straight after a merge or a run is the cache: wait for the Pages run, then re-run.
- On a Sunday with only one project filed, the run publishes nothing new and writes only the heartbeat. `data_fresh` still passes for 24 days; that is by design.
- `W37` and `W38` have no year. Don't "fix" them; they mean 2026.
- On the Mac, `grep` is a wrapper around ugrep; use `/usr/bin/grep` for the step 4 commands.
