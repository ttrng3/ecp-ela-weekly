"""Checks freshness.py's verdict for each heartbeat form. Run: python3 .github/scripts/test_freshness.py"""
import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

SCRIPT = pathlib.Path(__file__).resolve().parent / "freshness.py"
NOW = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

CASES = {
    "ECP-W38/ELA-W38": "false",
    "ECP-2026-W39/ELA-2026-W38": "false",
    "ECP-none/ELA-W40": "false",
    "inbox-unreachable": "true",
    "inbox-empty": "true",
    "ECP-none/ELA-none": "true",
}

failed = 0
for source, want in CASES.items():
    tmp = pathlib.Path(tempfile.mkdtemp())
    (tmp / "data").mkdir()
    (tmp / "data/index.json").write_text(json.dumps({"generatedUtc": NOW, "current": "W38"}))
    (tmp / "data/.last-check").write_text(f"{NOW} newest-source={source}\n")
    out = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp, capture_output=True, text=True).stdout
    got = next((l.split("=", 1)[1] for l in out.splitlines() if l.startswith("stale=")), None)
    ok = got == want
    failed += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {source:20} stale={got} (want {want})")
    shutil.rmtree(tmp)
sys.exit(1 if failed else 0)
