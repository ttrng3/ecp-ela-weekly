# Intent: publish ELA's W38 and W39 figures, read from the report page images

**Status:** accepted 2026-09-30
**Source:** chat, 2026-09-29/30 (Ty: "Force read to extract info from what we have", then "do both")

**Problem.** The published W38 and W39 weeks show ELA figures from W37 (12/09) with ⚠, because ELA's PDFs are slides exported as images and the routine read no text. On 2026-09-29 the W38 (19/09) and W39 (26/09) decks were rendered page by page and read as images; the same method on the W37 deck matched all 6 published W37 figures.

**Outcome.** `data/weeks/W38.json` and `data/weeks/2026-W39.json` carry ELA's real figures for their weeks (6 KPIs, PK1/PK3/PK4, what was done), each Δ against the week before it, so W38 compares with W37 and W39 with W38 from published data. Figures read from images are labelled so in the legend. The two contradictions inside ELA's own decks stay marked ⚠: W38's visitor count equals W37's exactly, and Eco Bazaar reads 54/66 on the summary slide but 58 on the detail slide.

**Who and what is affected.** The two week files only; the live page and the Cowork preview show them. No code, renderer, stylesheet or routine change (that is a separate intent, `work/260930-ela-page-images/`).

**Constraints.** "Report, don't fake": nothing guessed; a figure not on a slide is not written. "Deltas are computed, never copied." The KPI "Khai trương x/66" no longer exists in ELA's decks; it is replaced by their own label, "Căn đang hoạt động kinh doanh", and whether the two mean the same is left as an open question in the DECIDE item, not assumed. OMNI and ECOPM never share.

**Open questions.** none known.
