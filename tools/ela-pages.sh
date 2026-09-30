#!/bin/bash
# Renders pages 1-30 of any new weekly-report PDF over 10 MB in the Drive inbox
# to small JPEGs in _pages/<stem>-<bytes>/p-NN.jpg, so the cloud routine (10 MB
# download cap on the Drive connector) can read them. Never deletes, moves or
# renames a report; it only overwrites its own unfinished page files on retry.
# Needs the inbox folder set to "Available offline" in Google Drive: a launchd
# job cannot make Drive for Desktop download a cloud-only file.
# Runs hourly from launchd (tools/com.ty.ela-pages.plist).
# Install (first time), from the repo root:
#   mkdir -p ~/.local/bin && cp tools/ela-pages.sh ~/.local/bin/ela-pages.sh
#   ~/.local/bin/ela-pages.sh --seed      # skip reports of already-published weeks
#   cp tools/com.ty.ela-pages.plist ~/Library/LaunchAgents/
#   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.ty.ela-pages.plist
# Update after a merge: cp tools/ela-pages.sh ~/.local/bin/ela-pages.sh
set -u
LIMIT=10485760
LOG="$HOME/Library/Logs/ela-pages.log"
log(){ echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" >> "$LOG"; }
log "run (script sha256 $(shasum -a 256 "$0" | cut -c1-12))"

# The Drive for Desktop mount folder is named after the Google account, so it is
# found at run time rather than written here (this repo is public).
INBOX=""
for d in "$HOME"/Library/CloudStorage/GoogleDrive-*/"My Drive/Claude Workspace/00 Inbox/Weekly Reports ECP-ELA"; do
  [ -d "$d" ] && { INBOX="$d"; break; }
done
[ -n "$INBOX" ] || { log "inbox not mounted, skip"; exit 0; }

# Keys already handled ("<stem> <bytes>"). `--seed` records, without rendering,
# only PDFs whose week is already published on the live page (week <= `current`
# in data/index.json); anything newer, or any name it cannot parse, is left to
# render. So a report filed just before an install is still rendered.
SEEN="$HOME/.local/state/ela-pages.seen"
mkdir -p "$(dirname "$SEEN")"; touch "$SEEN"

shopt -s nullglob nocaseglob
if [ "${1:-}" = "--seed" ]; then
  cur=$(curl -fsS https://ttrng3.github.io/ecp-ela-weekly/data/index.json | python3 -c '
import json,sys,re
c=json.load(sys.stdin)["current"]; m=re.match(r"(?:(\d{4})-)?W(\d+)$",c)
print(int(m.group(1) or 2026)*100+int(m.group(2)))') || { log "seed: cannot read published week, nothing seeded"; exit 1; }
  for pdf in "$INBOX"/*.pdf; do
    b=$(basename "$pdf"); stem="${b%.*}"
    wk=$(echo "$stem" | sed -nE 's/^(ECP|ELA)-([0-9]{4})-W([0-9]{2})$/\2\3/p')
    [ -n "$wk" ] && [ "$wk" -le "$cur" ] && echo "$stem $(stat -f %z "$pdf")" >> "$SEEN"
  done
  log "seeded up to week $cur: $(wc -l < "$SEEN" | tr -d ' ') keys"; exit 0
fi
for pdf in "$INBOX"/*.pdf; do
  size=$(stat -f %z "$pdf" 2>/dev/null) || continue
  [ "$size" -gt "$LIMIT" ] || continue
  b=$(basename "$pdf"); stem="${b%.*}"
  key="$stem $size"
  grep -qxF -e "$key" "$SEEN" && continue
  # A re-filed report with the same name but new bytes gets a new folder.
  out="$INBOX/_pages/$stem-$size"
  [ -f "$out/done" ] && { echo "$key" >> "$SEEN"; continue; }
  tmp=$(mktemp -d)
  # Stream with cat into a temp file and check the size. From launchd neither cp
  # nor cat can read a cloud-only file ("Resource deadlock avoided"), which is
  # why the inbox must stay Available offline (verification/ela-page-images.md).
  if ! cat "$pdf" > "$tmp/src.pdf" 2>>"$LOG" || [ "$(stat -f %z "$tmp/src.pdf" 2>/dev/null)" != "$size" ]; then
    log "copy of source failed or incomplete: $stem (retry next hour)"; rm -rf "$tmp"; continue
  fi
  pages=$(pdfinfo "$tmp/src.pdf" 2>/dev/null | awk '/^Pages:/{print $2}')
  if ! pdftoppm -r 60 -jpeg -jpegopt quality=80 -f 1 -l 30 "$tmp/src.pdf" "$tmp/p" 2>>"$LOG"; then
    log "render failed: $stem (retry next hour)"; rm -rf "$tmp"; continue
  fi
  # pdftoppm pads page numbers to the document's page count (p-001 for 100+
  # pages); normalise to p-NN so the routine's lookups are stable.
  for f in "$tmp"/p-*.jpg; do
    num=$(basename "$f" .jpg); num=$((10#${num#p-}))
    mv "$f" "$tmp/p-$(printf %02d "$num").tmp"
  done
  for f in "$tmp"/p-*.tmp; do mv "$f" "${f%.tmp}.jpg"; done
  mkdir -p "$out" || { log "cannot create $out"; rm -rf "$tmp"; continue; }
  ok=1; n=0
  for f in "$tmp"/p-*.jpg; do
    dst="$out/$(basename "$f")"
    cp "$f" "$dst" || { ok=0; break; }
    [ "$(stat -f %z "$f")" = "$(stat -f %z "$dst" 2>/dev/null)" ] || { ok=0; break; }
    n=$((n+1))
  done
  if [ "$ok" = 1 ] && [ "$n" -gt 0 ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) pages_rendered=$n source_pages=${pages:-?} source_bytes=$size" > "$out/done"
    log "rendered $stem: $n of ${pages:-?} pages"; echo "$key" >> "$SEEN"
  else
    log "copy check failed for $stem after $n pages (no done marker; retry next hour)"
  fi
  rm -rf "$tmp"
done
