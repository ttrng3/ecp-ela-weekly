# Intent: the weekly routine reads ELA's figures from page images when the PDF has no text

**Status:** draft
**Source:** chat, 2026-09-29/30 (Ty: "Force read to extract info from what we have", then "do both": fix the W39 page and make the routine do it)

**Problem.** ELA's weekly reports are slide decks exported as images: W37 (126 MB, 12/09), W38 (164,5 MB, 58 pages) and W39 (141,9 MB, 55 pages) have no text layer. The routine reads them through the Drive connector's text extraction, gets empty content, and holds every ELA figure with ⚠ (W38 and W39 both, runbook step 4). On 2026-09-29 the figures were read by hand by rendering pages 3, 9, 16, 19–21 to images; checked against the published W37 page, 6/6 matched.

**Outcome.** When an ELA (or ECP) PDF returns no text, the scheduled run renders the needed pages to images and reads the figures from them, instead of holding last week's values. Figures read this way are labelled as read from images. Any page that cannot be read still falls back to ⚠, as today. The run reports which pages it read.

**Who and what is affected.** `docs/weekly-refresh.md` step 4, possibly the routine prompt, the cloud run's time and tool use. The page, renderer and data shape do not change.

**Constraints.** Cloud-only: no Mac, no mount ("never mount a machine"). "Report, don't fake": a number the run is unsure of is labelled, never guessed. Contradictions inside ELA's own deck are flagged, not resolved. Nothing new is published; the repo stays public, no folder id in it.

**Open questions.**
- Can the cloud run get a 140 MB PDF at all? The Drive connector's download may have a size limit; if it cannot, the fallback is ⚠ plus a request to ELA for a text-layer export.
- Does the cloud sandbox have a PDF renderer (`pdftoppm`), or can it install one?
- Read only the known slides (summary p.3, Eco Bazaar, nghiệm thu, handover, progress survey), or scan the whole deck each week?
