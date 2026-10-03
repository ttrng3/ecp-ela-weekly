# Verification: preview-wrapper (04/10)

Branch `work/preview-wrapper`, run on the Mac on 2026-10-04. `tools/preview_matches.py <preview> <build>`. The preview is the page `Artifact read` saved from the preview titled "Điều Hành Vận Hành ECP × ELA" into the session's scratch folder; its id is never written here. Variants were made from that copy in the scratch folder:

| Case | Input | Expected | Exit |
|---|---|---|---|
| real | the saved preview vs `build/artifact.html` | match | 0 |
| one-byte | one fragment byte flipped | no match | 1 |
| unknown-head | `<!doctype html>` changed to `<!DOCTYPE html>` | head not pinned | 1 |
| trailing-newline | a `\n` appended (a save that adds one) | tail not exact | 1 |
| empty-build | an empty build file | no match | 1 |

```
real exit=0 {"skeleton_head_pinned": true, "skeleton_head": 537, "skeleton_tail_exact": true, "match": true}
one-byte exit=1 {"skeleton_head_pinned": true, "skeleton_head": 537, "skeleton_tail_exact": true, "match": false}
unknown-head exit=1 {"skeleton_head_pinned": false, "skeleton_head": null, "skeleton_tail_exact": true, "match": false}
trailing-newline exit=1 {"skeleton_head_pinned": true, "skeleton_head": 537, "skeleton_tail_exact": false, "match": false}
empty-build exit=1 {"skeleton_head_pinned": true, "skeleton_head": 537, "skeleton_tail_exact": true, "match": false}
```

Step 1 (`tools/verify_live.py`) on the branch after the change: `"pass": true`, 12/12.
