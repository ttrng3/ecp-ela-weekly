# Điều Hành Vận Hành ECP × ELA

Live dashboard: **https://ttrng3.github.io/ecp-ela-weekly/**

A weekly executive briefing comparing **Eco Central Park** (Vinh) and
**Eco Retreat** (Long An) week over week — not a time series. Each week is a
self-contained read: KPIs, what was done, handover progress, and what needs a
decision from BLĐ.

## How this repo is the source of truth

```
Google Drive — 07 Weekly Reports (ECP + ELA weekly PDFs)
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
(`<style id="apple-layer">`, 2026-09-24, from the `apple-design` skill): full
**dark mode** that follows the system or `<html data-theme="light|dark">`, card
shadows, optical sizing, and the contrast/motion accessibility blocks. Dark is
screen-only — print always comes out light. The page is **not** light-only any
more; any new colour must be a token with a dark value, never a raw hex.
A refresh writes `data/`, never the stylesheet.

## One surface, on purpose

    schedule → cloud routine → source → GitHub → Pages

**GitHub Pages is the only published surface.** Ty ruled on 2026-09-23 that he
wants control over what exists of his work, so there is no claude.ai artifact
copy of this dashboard: the Pages URL above is the address, full stop.

A mirror artifact existed for a few hours that day and was deleted. Do not
recreate one, and do not add an artifact URL to this repo. `tools/build-fragment.py`
is kept only because it is the one thing that can derive a standalone fragment
of this page if it is ever needed; nothing in the refresh calls it.
