# Plan: ela-page-images (revision 2)

1. `tools/ela-pages.sh`: find inbox PDFs > 10 MB without `_pages/<stem>-<bytes>/done`; render p.1–30 to a temp folder; copy to `_pages/<stem>-<bytes>/`; size-check each copy; write `done` last. Log to `~/Library/Logs/ela-pages.log`. Never deletes, moves or renames a report.
2. `tools/com.ty.ela-pages.plist`: launchd agent, hourly, PATH includes /opt/homebrew/bin.
3. Install: copy the script to `~/.local/bin/ela-pages.sh` (a fixed path, so branch switches in the repo checkout don't affect it), run it once with `--seed`, copy the plist to `~/Library/LaunchAgents`, load it; set the inbox Available offline → Promise 1.
4. `docs/weekly-refresh.md` step 4: the "large or image-only PDF" sub-step.
5. Promise 2 with the disabled test routine (updated prompt, fired once).
6. Reviewer, PR, Ty's ship phrase; then the routine prompt STEP 4 points to the new sub-step.
