# Điều Hành Vận Hành ECP × ELA

Live dashboard: **https://ttrng3.github.io/ecp-ela-weekly/**

A weekly executive briefing comparing **Eco Central Park** (Vinh) and
**Eco Retreat** (Long An) week over week — not a time series. Each week is a
self-contained read: KPIs, what was done, handover progress, and what needs a
decision from BLĐ.

## How this repo is the source of truth

```
Google Drive — 00 Inbox/Weekly Reports ECP-ELA (ECP-W<N>.pdf, ELA-W<N>.pdf)
        ▼
weekly routine ──writes──▶ data/index.json + data/weeks/W<N>.json
                                   │
                                   ▼
                            GitHub Pages
                            (index.html)
```

`index.html` is a **renderer with no data in it** (~10 KB). It fetches `data/`
at load — relative first, falling back to the published
`https://ttrng3.github.io/ecp-ela-weekly/data/` — so the same file works as a
Pages site and from a local copy.

## Why it changed

The page used to be a single hand-built HTML file. The weekly routine assembled
it, republished a claude.ai artifact, saved a standalone copy to Drive, then
pushed *that file* to GitHub with a PAT — so the published page was downstream
of the artifact, and every hop carried the whole document.

Now the routine writes data and the page renders it. A weekly update is one new
`data/weeks/W<N>.json` (~9 KB) plus a rewritten `data/index.json` (~0.4 KB).

The split was verified by rendering both the old page and the new one and
comparing the resulting text: **identical, 5,666 characters.**

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | Renderer only. No data. |
| `data/index.json` | `generatedUtc`, `current` week, project names, `weeks` manifest. |
| `data/weeks/W<N>.json` | That week's whole briefing: verdict, KPIs, done, progress, actions, KSNB notes, sources. |
| `data/.last-check` | Heartbeat. Proves the job ran even when there was no new report. |
| `.github/workflows/freshness-check.yml` | Opens an issue if the job stops, or if the reports go quiet. |

## Why the heartbeat matters here more than anywhere else

This dashboard's source is **irregular** — ECP and ELA file their weekly PDFs on
their own cadence, and some weeks are missing entirely (no W34–W35 for ECP, no
W35 for ELA). So "the page has not changed in a week" is a completely normal
state, and is indistinguishable from "the routine died" if you only look at the
published page.

`data/.last-check` is what separates them. The freshness check reads both: the
heartbeat says the job ran, `generatedUtc` says it published.

## Data caveats

- **ECP publishes its weekly report as images** (no text layer), so its numbers
  cannot be extracted automatically. When a week cannot be read, the runbook
  requires keeping the prior figures, labelling them, and naming exactly which
  indicators are missing — never inventing a number.
- ELA's PDFs run 100–130 MB and the template changes between weeks.

## Visual standard

The renderer uses Apple HIG light tokens (base sheet) plus an **Apple layer**
(`<style id="apple-layer">`, 2026-09-24, from the `apple-design` skill): card
shadows, optical sizing, and the contrast/motion accessibility blocks.
**Light only — Ty ruled 2026-09-24** (dark mode ran for one morning and was withdrawn): the page stays light whatever the viewer's system setting, and there is no dark theme. Do not add one back. Any new colour must be a token, never a raw hex.
A refresh writes `data/`, never the stylesheet.

## One address, one preview

    schedule → cloud routine → source → GitHub → Pages (the address) → artifact (Cowork preview)

**https://ttrng3.github.io/ecp-ela-weekly/ is the only link.** A claude.ai artifact exists as the Cowork preview
of this page, and the routine refreshes it as its last step, only after the
repo is correct. Its URL is never written here, in a Drive doc, or in a run
report: Ty ruled on 2026-09-24 and again on 2026-09-26 that content with a
Pages address gets no second link. The routine prompt is the only place it
lives. The preview must exist: "no artifact link" means the URL stays out of
sight, never that the artifact goes.

**This replaces the 2026-09-23 rule** that stood here ("there is no claude.ai
artifact copy … do not recreate one"). That text is withdrawn, not a conflict
to weigh: the routine prompt says this repo's files win, and on 2026-09-27 the
TMDV routine read the same old text and skipped its mirror step.

`tools/build-fragment.py` derives the fragment the preview needs from
`index.html`; the routine uses it only when the renderer itself changes.
