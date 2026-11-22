# PJM Large-Load Forecast Accuracy: Requests, Forecasts, and Observed July Peaks

**Status:** exploratory / not peer reviewed / not an official PJM analysis. **Not a finding about AI-only data-center consumption.**

## Research question
How does a change in forecast vintage affect the accuracy of PJM's reported **annual summer large-load adjustment** predictions for the same target year and zone?

This repository reproduces matched July-peak comparisons from PJM's **2026 Load Forecast Accuracy Report** workbook. It does **not** link individual September 2026 utility requests to observed project-level loads; those requests are a separate prospective dataset.

## Reproduce
1. Install Python 3.11+ and dependencies `openpyxl` and `matplotlib` (matplotlib is optional for CSV-only output).
2. From the project root run `python analyze.py`.
3. Find `matched_forecasts_actuals.csv`, `paired_vintage_comparisons.csv` in `data/processed/`, and the PNG in `figures/`.

The raw input is `data/raw/2026-accuracy-report.xlsx` (PJM public data). The script reads every worksheet using `artifact_tool`, matches on **worksheet + target year**, and parses a forecast vintage from the metric name. Source data and derived outputs remain separate.

## Metrics
- Difference (MW): `observed - forecast` (positive = historical above forecast)
- Signed difference % of forecast: `(observed - forecast)/forecast*100` (this is the metric in earlier working notes)
- Conventional APE (% of observed): `abs(observed - forecast)/observed*100`
- Forecast lead proxy: `target year - forecast vintage year`; **not an exact month-level lead time**.

Both denominators are included to prevent silently mixing definitions. No weighted average of zone errors is reported. The PJM RTO aggregate is not pooled with its constituent zones, and utility subzones are not counted as independent parent zones.

## Source and comparability cautions
- [PJM May 2026 Accuracy Report](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-forecast-accuracy-report.pdf), p. 3 explains that the **monthly top panels** are data-center-only, whereas the **annual lower panels** present summer large-load adjustments, which are not necessarily data-center-only.
- Historical load observations come from EDC/LSE submissions, not a complete independent verification of every project.
- Public values may be omitted or masked for confidentiality or missing submissions. A lack of a historical value is *not zero* and is not evidence of cancellation.
- Neither a July adjustment comparison nor the 2026 request dataset is weather-normalized total-grid demand. Do not confuse these figures with actual hourly or annual energy consumption.
- These are **forecast-component accuracy** comparisons, not individual project forecasts and not proof of the cause of errors.
- Project realization scenarios (on time / delayed / smaller / canceled) remain hypotheses; zone-level outcomes cannot uniquely identify them.

## Data provenance / further reading
- PJM [Load Forecast Development Process](https://www.pjm.com/planning/resource-adequacy-planning/load-forecast-dev-process)
- PJM [2026 Accuracy Report PDF](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-forecast-accuracy-report.pdf)
- PJM [2026 Accuracy workbook](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-accuracy-report.xlsx)
- PJM [Manual 19: Load Forecasting and Analysis](https://learn.pjm.com/-/media/DotCom/documents/manuals/m19.ashx)
- [IEEE Spectrum Expert Author Guidelines](https://spectrum.ieee.org/guidelines-expert-authors)
- [IEEE Spectrum Generative AI Statement](https://spectrum.ieee.org/about)

## Editorial and AI disclosure
This is an AI-assisted **analysis and drafting aid**. The author must independently inspect data, verify calculations and source assertions, and supply their own reporting, analysis, and final writing. Do not pass AI-authored prose to IEEE Spectrum as a human-written manuscript. Follow Spectrum's human-authorship and disclosure directions and ask the assigning editor about disclosure for computational code/figures where needed. No IEEE editor has approved this work.

## Publishing this repository
This project is provided locally and is **not yet on GitHub**. After inspecting it, create a repository and upload these contents (excluding any personal/employer data). The source files here are public PJM materials. Consider whether to keep a downloaded copy of the workbook or link to the source instead; its original data provenance should remain explicit.
