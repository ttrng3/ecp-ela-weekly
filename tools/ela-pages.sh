#!/bin/bash
# Renders pages 1-30 of any new weekly-report PDF over 10 MB in the Drive inbox
# to small JPEGs in _pages/<stem>-<bytes>/, so the cloud routine (10 MB download
# cap on the Drive connector) can read them. Write-new-only: never moves,
# renames or deletes. Runs hourly from launchd (tools/com.ty.ela-pages.plist).
# Install / update after a merge: copy this file to ~/.local/bin/ela-pages.sh.
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

# Keys already handled ("<stem> <bytes>"). Seeded at install with every PDF then
# present, so only new or re-filed reports are rendered (each render pulls the
# whole 100-700 MB PDF through Drive for Desktop).
SEEN="$HOME/.local/state/ela-pages.seen"
mkdir -p "$(dirname "$SEEN")"; touch "$SEEN"

shopt -s nullglob
for pdf in "$INBOX"/*.pdf; do
  size=$(stat -f %z "$pdf" 2>/dev/null) || continue
  [ "$size" -gt "$LIMIT" ] || continue
  stem=$(basename "$pdf" .pdf)
  key="$stem $size"
  grep -qxF "$key" "$SEEN" && continue
  # A re-filed report with the same name but new bytes gets a new folder.
  out="$INBOX/_pages/$stem-$size"
  [ -f "$out/done" ] && { echo "$key" >> "$SEEN"; continue; }
  tmp=$(mktemp -d)
  # cat, not cp: cp's fcopyfile hits "Resource deadlock avoided" on a cold Drive
  # placeholder; a plain byte stream hydrates it. Size must match.
  if ! cat "$pdf" > "$tmp/src.pdf" 2>>"$LOG" || [ "$(stat -f %z "$tmp/src.pdf" 2>/dev/null)" != "$size" ]; then
    log "copy of source failed or incomplete: $stem (retry next hour)"; rm -rf "$tmp"; continue
  fi
  pages=$(pdfinfo "$tmp/src.pdf" 2>/dev/null | awk '/^Pages:/{print $2}')
  if ! pdftoppm -r 60 -jpeg -jpegopt quality=80 -f 1 -l 30 "$tmp/src.pdf" "$tmp/p" 2>>"$LOG"; then
    log "render failed: $stem (retry next hour)"; rm -rf "$tmp"; continue
  fi
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
