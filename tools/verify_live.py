#!/usr/bin/env python3
"""Machine half of verification/weekly.md: is the live page what main says, and is main sound?

Run from an up-to-date checkout of main, outside the Sunday run (14:00 UTC):
  git pull --ff-only && python3 tools/verify_live.py --forbid WORD [WORD ...]

--forbid takes the other entity's name and the inbox folder id (from the routine prompt). The runner
supplies them at run time so the repo never holds them. Without them the check fails rather than
passing unchecked.

Prints one JSON object of verdicts and exits 0 only when every verdict is true.
Matches are reported by count and file, never by value.
"""
import argparse, datetime as dt, glob, hashlib, json, pathlib, re, subprocess, sys, time, unicodedata, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "https://ttrng3.github.io/ecp-ela-weekly/"
# Tracked but never served (.pages-allow); each must exist on main and answer 404 live.
PRIVATE = ["README.md", "CLAUDE.md", "REVIEW.md", "data/.last-check", "docs/weekly-refresh.md",
           "tools/build-fragment.py", "tools/reconcile.py", "tools/ela-pages.sh", "tools/com.ty.ela-pages.plist",
           "tools/verify_live.py", "verification/weekly.md", "build/artifact.html", "archive/status_20260915.html",
           ".github/scripts/freshness.py", ".pages-allow"]
# Storage links, full email addresses, bare handles ("name@"), and the Drive mount folder name.
TRACES = re.compile(r"/personal/|sharepoint\.com|1drv\.ms|[\w.+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}|\b[a-z][a-z0-9._-]{2,}@(?![\w-])|GoogleDrive-[\w.@-]+", re.I)
HEARTBEAT_MAX = 9  # the watchdog pipeline-wiring's collect_status.py sets for ecp-ela
DATA_MAX = 24      # MAX_DATA_AGE_DAYS default in .github/scripts/freshness.py
LEGACY = ["W37", "W38"]  # keys with no year; they mean 2026 (runbook steps 2 and 5)
SECTIONS = ["kpis", "done", "progress", "actions"]


def get(path, tries=2):
    """One retry on a network error or a 5xx: a blip must not read as a mismatch."""
    url = f"{LIVE}{path}?v={int(time.time())}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "verify-live"}), timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return get(path, tries - 1) if e.code >= 500 and tries > 1 else (e.code, b"")
    except Exception as e:
        return get(path, tries - 1) if tries > 1 else (str(e), b"")


def age_days(stamp):
    """Days since an ISO stamp; None if unreadable."""
    try:
        t = dt.datetime.fromisoformat(stamp.strip().replace("Z", "+00:00"))
        t = t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
        return round((dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 86400, 1)
    except (ValueError, AttributeError):
        return None


def week_order(key):
    """(year, week) for a manifest key; None if it has neither shape."""
    if key in LEGACY:
        return (2026, int(key[1:]))
    m = re.fullmatch(r"(\d{4})-W(\d{2})", key)
    return (int(m.group(1)), int(m.group(2))) if m else None


def norm(t):
    return unicodedata.normalize("NFC", str(t or "")).casefold()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forbid", nargs="*", default=[])
    forbid = [norm(w) for w in ap.parse_args().forbid if w.strip()]

    v, info, live = {}, {}, {}
    try:
        d = json.loads((ROOT / "data/index.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        d = {}
        info["index_error"] = str(e)
    d = d if isinstance(d, dict) else {}
    weeks = d.get("weeks") if isinstance(d.get("weeks"), dict) else {}
    keys = list(weeks)

    v["manifest_consistent"] = (bool(keys) and d.get("current") in weeks and keys[-1] == d.get("current") and
                                all((ROOT / f"data/weeks/{f}.json").exists() for f in weeks.values()))
    order = [week_order(k) for k in keys]
    info["bad_keys"] = [k for k, o in zip(keys, order) if o is None]
    v["weeks_ordered"] = bool(keys) and not info["bad_keys"] and order == sorted(order) and len(set(order)) == len(order)
    v["legacy_keys_kept"] = all(weeks.get(k) == k for k in LEGACY)

    # Wait-for-both (runbook step 3): every published week carries both projects in every section.
    info["one_sided"] = []
    for k, f in weeks.items():
        try:
            w = json.loads((ROOT / f"data/weeks/{f}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            info["one_sided"].append(f"{k}:unreadable")
            continue
        for s in SECTIONS:
            for side in ("ecp", "ela"):
                if not (isinstance(w.get(s), dict) and isinstance(w[s].get(side), list) and w[s][side]):
                    info["one_sided"].append(f"{k}:{s}.{side}")
    v["both_projects_every_week"] = bool(keys) and not info["one_sided"]

    served = ["index.html", "data/index.json"] + [f"data/weeks/{f}.json" for f in weeks.values()]
    for p in served:
        st, body = get(p)
        live[p] = body
        info[p] = {"status": st, "live": hashlib.sha256(body).hexdigest()[:12],
                   "main": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:12] if (ROOT / p).exists() else None}
    v["served_equals_main"] = all(info[p]["status"] == 200 and info[p]["live"] == info[p]["main"] for p in served)
    info["served_mismatch"] = [p for p in served if info[p]["status"] != 200 or info[p]["live"] != info[p]["main"]]
    for p in served:
        del info[p]

    work = sorted(glob.glob(str(ROOT / "work/*/intent.md")))[:1]  # any one work file, found at run time
    private = PRIVATE + [str(pathlib.Path(w).relative_to(ROOT)) for w in work]
    info["private_status"] = {p: get(p)[0] for p in private}
    info["private_missing_on_main"] = [p for p in private if not (ROOT / p).exists()] + ([] if work else ["work/*/intent.md"])
    v["private_not_served"] = all(s == 404 for s in info["private_status"].values()) and not info["private_missing_on_main"]

    beat_line = (ROOT / "data/.last-check").read_text(encoding="utf-8").strip() if (ROOT / "data/.last-check").exists() else ""
    info["heartbeat_age_days"] = age_days((beat_line.split() or [""])[0])
    info["data_age_days"] = age_days(str(d.get("generatedUtc", "")))
    # -1 allows clock skew; a stamp in the future (a wrong year) would otherwise pass forever.
    v["heartbeat_fresh"] = info["heartbeat_age_days"] is not None and -1 <= info["heartbeat_age_days"] <= HEARTBEAT_MAX
    # The 30/09 rule (PR #12): the line is the stamp and newest-source=<value>, nothing after it.
    v["heartbeat_bare"] = re.fullmatch(r"\S+Z newest-source=\S+", beat_line) is not None
    v["data_fresh"] = info["data_age_days"] is not None and -1 <= info["data_age_days"] <= DATA_MAX

    # Every served path, live and on main, plus every other tracked text file on main. Only this script
    # is left out of the trace check, because it spells out the patterns; the forbidden words are
    # checked everywhere.
    texts = {f"live:{p}": b.decode("utf-8", "replace") for p, b in live.items()}
    tracked = [p for p in subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True).stdout.split("\0") if p]
    info["unreadable"] = []
    for p in tracked:
        try:
            texts[f"main:{p}"] = (ROOT / p).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pass  # binary file
        except OSError:
            info["unreadable"].append(p)
    v["all_tracked_read"] = not info["unreadable"]
    hits = {p: len(TRACES.findall(t)) for p, t in texts.items() if p != "main:tools/verify_live.py"}
    info["traces"] = {p: n for p, n in hits.items() if n}
    v["no_personal_traces"] = not info["traces"]
    info["forbid_checked"] = len(forbid)
    # Forbidden words on what is served only: docs may name the other entity's label (REVIEW.md allows it).
    info["forbidden_in"] = sorted({k for k, t in texts.items() if k.split(":", 1)[1] in served for w in forbid if w in norm(t)})
    v["no_forbidden_words"] = bool(forbid) and not info["forbidden_in"]

    print(json.dumps({"pass": all(v.values()), "verdicts": v, "info": info}, ensure_ascii=False, indent=1))
    sys.exit(0 if all(v.values()) else 1)


if __name__ == "__main__":
    main()
