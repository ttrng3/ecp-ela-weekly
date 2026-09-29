"""Report dashboard freshness for the freshness-check workflow.

Two clocks, because they mean different things:

  data/.last-check  — the job ran. Written on EVERY run, including quiet ones.
  data/index.json   — the job found new source data and published it.

Only reading index.json cannot tell "the team published no new week" apart from
"the job stopped running", and those need different responses. Reading both can.
"""
import datetime as dt
import json
import os
import pathlib
import re

RUN_MAX = int(os.environ.get("MAX_RUN_AGE_DAYS", "10"))
DATA_MAX = int(os.environ.get("MAX_DATA_AGE_DAYS", "24"))
NOW = dt.datetime.now(dt.timezone.utc)


def age_days(stamp):
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    return (NOW - t).days


data = json.loads(pathlib.Path("data/index.json").read_text(encoding="utf-8"))
data_age = age_days(data["generatedUtc"])

beat = pathlib.Path("data/.last-check")
if beat.exists():
    m = re.match(r"(\S+)", beat.read_text(encoding="utf-8").strip())
    run_stamp = m.group(1) if m else None
    src = re.search(r"newest-source=(\S+)", beat.read_text(encoding="utf-8"))
    source = src.group(1) if src else None
else:
    run_stamp, source = None, None
run_age = age_days(run_stamp) if run_stamp else None

if run_age is None or run_age > RUN_MAX:
    state, why = "stale", (
        "the weekly job has not run" if run_age is None
        else f"the weekly job last ran {run_age} days ago")
elif source == "inbox-unreachable":
    state, why = "stale", (
        f"the job ran {run_age}d ago but could not read the Drive inbox "
        f"— check the folder id in the routine prompt and the folder's access")
elif source == "inbox-empty":
    state, why = "stale", (
        f"the job ran {run_age}d ago and read the Drive inbox, but no PDF matched "
        f"ECP or ELA — check the file names")
elif data_age > DATA_MAX:
    state, why = "stale", (
        f"the job is running (last run {run_age}d ago) but no new week has been "
        f"published in {data_age} days — check whether BQLVH is still filing")
else:
    state, why = "fresh", f"job ran {run_age}d ago, data {data_age}d old"

print(f"generated={data['generatedUtc']}")
print(f"week={data['current']}")
print(f"days={data_age}")
print(f"run_days={run_age if run_age is not None else -1}")
print(f"why={why}")
print(f"stale={'true' if state == 'stale' else 'false'}")
