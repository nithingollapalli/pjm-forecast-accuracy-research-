#!/usr/bin/env python3
"""Reproduce PJM summer large-load July peak forecast-vintage comparisons.
Requires: openpyxl and matplotlib; input: data/raw/2026-accuracy-report.xlsx.
Only reported historic observations are compared; missing actuals are excluded.
"""
from pathlib import Path
from collections import defaultdict
import csv, re
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data/raw/2026-accuracy-report.xlsx'
OUT = ROOT / 'data/processed'
OUT.mkdir(parents=True, exist_ok=True)
wb = load_workbook(SOURCE, read_only=True, data_only=True)
raw=[]
for sheet in wb.worksheets:
    # Read the area containing zone, target year, metric, and MW, ignoring chart objects.
    for row in sheet.iter_rows(min_row=2, max_col=4, values_only=True):
        if len(row) < 4: continue
        zone, yr, metric, mw = row
        if isinstance(yr, (int,float)) and isinstance(mw, (int,float)) and isinstance(metric,str):
            raw.append(dict(sheet=sheet.title, zone=str(zone), target_year=int(yr), metric=metric.strip(), mw=float(mw)))
print('data rows',len(raw),'sheets',len(wb.worksheets))

actual = {}
forecasts = []
for r in raw:
    if r['metric']=='Historical July Peak':
        k=(r['sheet'],r['target_year'])
        if k in actual:
            raise ValueError(f'duplicate observed actual at {k}')
        actual[k]=r['mw']
    else:
        m=re.fullmatch(r'(20\d\d) Load Forecast July Peak',r['metric'])
        if m:
            forecasts.append((r,int(m.group(1))))

matched=[]
for r,vintage in forecasts:
    k=(r['sheet'],r['target_year'])
    if k not in actual: continue
    observed=actual[k]; predicted=r['mw']
    if observed <= 0 or predicted <= 0: continue
    matched.append(dict(sheet=r['sheet'],zone=r['zone'],target_year=r['target_year'],forecast_vintage=vintage,
                        lead_years=r['target_year']-vintage,forecast_mw=round(predicted,6),actual_mw=round(observed,6),
                        error_mw=round(observed-predicted,6),signed_pct_forecast_denominator=round((observed-predicted)/predicted*100,5),
                        abs_pct_forecast_denominator=round(abs(observed-predicted)/predicted*100,5),
                        ape_pct_actual_denominator=round(abs(observed-predicted)/observed*100,5)))
matched.sort(key=lambda x:(x['sheet'],x['target_year'],x['forecast_vintage']))
assert len({(x['sheet'],x['target_year'],x['forecast_vintage']) for x in matched})==len(matched)

def write_csv(name, rows):
    if not rows:return
    with (OUT/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
write_csv('matched_forecasts_actuals.csv',matched)

# Only parent zones, and PJM RTO as a separately identified regional aggregate.
# Exclude subzones to avoid duplicate geographic components and avoid aggregating RTO into zone statistics.
parent={'AEP','APS','ATSI','BGE','COMED','DAYTON','DOM','DQE','JCPL','METED','PECO','PEPCO','PL','PS'}
groups=defaultdict(list)
for r in matched:
    if r['sheet'] in parent or r['sheet']=='RTO':
        groups[(r['sheet'],r['target_year'])].append(r)
paired=[]
for (sheet,year),items in sorted(groups.items()):
    items.sort(key=lambda x:x['forecast_vintage'])
    if len(items)<2:continue
    old,new,previous=items[0],items[-1],items[-2]
    paired.append(dict(sheet=sheet,target_year=year,oldest_vintage=old['forecast_vintage'],latest_vintage=new['forecast_vintage'],
                       previous_vintage=previous['forecast_vintage'],oldest_ape_pct=old['ape_pct_actual_denominator'],
                       previous_ape_pct=previous['ape_pct_actual_denominator'],latest_ape_pct=new['ape_pct_actual_denominator'],
                       earliest_to_latest_ape_change_pp=round(new['ape_pct_actual_denominator']-old['ape_pct_actual_denominator'],5),
                       final_revision_ape_change_pp=round(new['ape_pct_actual_denominator']-previous['ape_pct_actual_denominator'],5),
                       earliest_to_latest_improved=new['ape_pct_actual_denominator']<old['ape_pct_actual_denominator'],
                       last_revision_improved=new['ape_pct_actual_denominator']<previous['ape_pct_actual_denominator']))
write_csv('paired_vintage_comparisons.csv',paired)

# Raw findings displayed for inspection
for row in matched:
    if row['sheet']=='RTO' and row['target_year']==2025:
        print('RTO 2025',row)
print('matched',len(matched),'paired parent / RTO',len(paired))
print('improved oldest->latest',sum(x['earliest_to_latest_improved'] for x in paired),'final',sum(x['last_revision_improved'] for x in paired))

try:
    import matplotlib.pyplot as plt
    rto=[r for r in matched if r['sheet']=='RTO' and r['target_year']==2025]
    (ROOT / 'figures').mkdir(parents=True, exist_ok=True)
    fig,ax=plt.subplots(figsize=(9,5))
    ax.bar([str(x['forecast_vintage']) for x in rto],[x['ape_pct_actual_denominator'] for x in rto])
    ax.set(xlabel='PJM forecast vintage',ylabel='Absolute percentage error vs actual (%)',
           title='2025 PJM RTO July large-load peak: forecast vintage accuracy')
    ax.text(.02,-.23,'Source: PJM 2026 Load Forecast Accuracy Report, RTO worksheet.\nActual-denominator APE; not systemwide electric-load forecasting error.',
            transform=ax.transAxes,fontsize=9)
    fig.tight_layout();fig.savefig(ROOT/'figures/rto_2025_vintage_ape.png',dpi=180,bbox_inches='tight')
    plt.close(fig)
except ImportError:
    print('matplotlib unavailable; CSVs still generated')
