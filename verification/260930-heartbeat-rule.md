# Verification: heartbeat-rule (30/09)

Branch heartbeat-rule, run on the Mac 2026-09-30. The inbox folder id is passed in at run time from the routine prompt and never written here.

```
$ cat data/.last-check
2026-09-30T01:38:29Z newest-source=ECP-2026-W39/ELA-2026-W39
$ python3 .github/scripts/test_freshness.py
ok   ECP-W38/ELA-W38      stale=false (want false)
ok   ECP-2026-W39/ELA-2026-W38 stale=false (want false)
ok   ECP-none/ELA-2026-W40 stale=false (want false)
ok   inbox-unreachable    stale=true (want true)
ok   inbox-empty          stale=true (want true)
ok   ECP-none/ELA-none    stale=true (want true)
$ python3 .github/scripts/freshness.py
generated=2026-09-29T16:36:01Z
week=2026-W39
days=0
run_days=0
why=job ran 0d ago, data 0d old
stale=false
$ git grep -n -F "$INBOX_ID"   # exit 1 = no match
exit 1
```
