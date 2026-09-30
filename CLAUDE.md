# CLAUDE.md — ecp-ela-weekly

Weekly ops briefing for Eco Central Park (Vinh) and Eco Retreat (Long An), entity **OMNI**. Live: https://ttrng3.github.io/ecp-ela-weekly/

**If you are the scheduled routine:** follow the files your prompt names, `docs/weekly-refresh.md` and `README.md`. They outrank this file. This file adds no step to a run.

## Commands
- Check `current` is in the `weeks` manifest: `python3 -c "import json;d=json.load(open('data/index.json'));assert d['current'] in d['weeks']"`
- Build the Cowork preview page, only when `index.html` changed: `python3 tools/build-fragment.py` (rewrites the tracked `build/artifact.html`; commit it with the renderer change)
- Compare two `data/` trees: `python3 tools/reconcile.py <dir-a> <dir-b>` (exit 0 = same)
- Freshness check, as the daily Action runs it: `python3 .github/scripts/freshness.py`; its tests: `python3 .github/scripts/test_freshness.py`
- Mac render helper, after editing it: `bash -n tools/ela-pages.sh` and `plutil -lint tools/com.ty.ela-pages.plist`; install and update steps are in the script's header

## Layout
- `index.html` is a renderer holding no data. A refresh never touches it or its stylesheet.
- Data: `data/index.json` (`generatedUtc`, `current`, `weeks` manifest), `data/weeks/<YYYY>-W<NN>.json` (one briefing per week), `data/.last-check` (heartbeat, not published).
- `.pages-allow` lists what Pages publishes; `.github/workflows/pages.yml` deploys only that. A new kind of file under `data/` needs Ty's say-so and its own `.pages-allow` line in its own PR first.
- `tools/ela-pages.sh` + `tools/com.ty.ela-pages.plist`: the Mac helper that renders ELA's image-only decks into `_pages/` on Drive (runbook step 4a).
- `README.md` explains the data model; `REVIEW.md` holds the reviewer's rules; `verification/` records each change's checks.

## Rules
- Changes reach `main` through a PR and Ty's ship. The routine's data writes are the only direct writes.
- The runbook and README win over this file and any memory note.
- Never write a Drive folder id, the Drive mount path, a Cowork preview URL or artifact id, a person's details or a secret into this public repo.
- Entity separation: this is OMNI (Ty ruled 29/09). No EcoPM data, names or numbers.
- A week is published only when both ECP and ELA have filed it (runbook step 3). Never infer a figure or carry one forward unmarked (runbook 4b).

## Known mistakes
- ELA's decks are slides saved as images, with no text layer (100–165 MB for W33–W39; W24–W25 were 660–690 MB, README "Data caveats") and the Drive connector refuses downloads over 10 MB. They are read from rendered page images, not skipped (runbook 4a, 30/09).
- A background job cannot make Drive for Desktop download a cloud-only file: from launchd, `cp` and `cat` both fail with "Resource deadlock avoided". So the inbox stays "Available offline" (`verification/ela-page-images.md`, 30/09).
- On a file that is already local, scripts read it with `cat` into a temp file and size-check it, not `cp`: `cp` also hit the deadlock on a cold placeholder (`tools/ela-pages.sh`, 30/09).
- The local Drive mount path contains a personal account name; `tools/ela-pages.sh` finds it with a `GoogleDrive-*` glob. Never spell the path out in code, docs or a branch (30/09).
- ELA's own slides can contradict each other (Eco Bazaar summary 54/66 vs detail 58; W38 visitors identical to W37). Show both and mark ⚠; never pick one (runbook 4a.3, `data/weeks/W38.json`, 30/09).
- ECP's weekly file can be a copy of the previous week with only the figures block updated (W38's cover still said "BÁO CÁO TUẦN 37"). Its events text may repeat last week's word for word (`data/weeks/W38.json`, Sep 2026).
- The two oldest week keys, `W37` and `W38`, carry no year and mean 2026. Don't rename them; new weeks use `<YYYY>-W<NN>` (runbook steps 2 and 5, 29/09).
- Publishing `index.html` as the Cowork preview nests one document inside another and renders blank. Build the fragment, and send data files and the page in separate calls (`tools/build-fragment.py`, 23/09).
