# Measurement audit — November 2026

## Confirmed from PJM's May 2026 report
- The report evaluates **large load adjustments** included in PJM's Long-Term Load Forecast against operational data submitted by EDCs and LSEs.
- The **monthly data center load peak** dashboard is expressly filtered to data centers only.
- The separate **annual summer large load adjustment** chart includes adjustment categories beyond just data centers.
- Historical data are plotted only where supplied, and single-customer values can be suppressed.
- The reported “actual peak” is a peak observation, **not** annual energy, and is not necessarily an ordinary hourly system peak.

## Valid inference
Compare reported July historical and corresponding forecast-vintage values **within a worksheet and target year** as a descriptive accuracy diagnostic of the *reported large-load adjustment series*.

## Not established
- That this series includes only AI data centers, or that actuals are fully measured for every utility.
- That observed discrepancies quantify delays/cancellations or weather effects.
- That an individual September 2026 **requested** amount is the same metric as a PJM **reviewed/adjusted** amount; do not subtract without aligning vintage, peak basis, MW vs capacity, cumulative definitions and utility coverage.
- That public large-load tables can reveal independent project-level outcomes.

## Denominators
Earlier phase notes used `abs(actual - forecast)/forecast`; conventional absolute percentage error instead uses `abs(actual - forecast)/actual`. Both are exported, and notes should always specify the denominator. Avoid claiming prior 5.59% is a conventional APE.
