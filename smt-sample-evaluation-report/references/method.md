# Method - formulas, rounding, evidence labels, report structure

## Formulas (calc.py)
| Figure | Formula |
|---|---|
| ppb (parts per board) | Σ qty of BOM parts with fit ≠ false |
| ppp (parts per panel) | ppb × boards_per_panel |
| panels/h theoretical | 3600 ÷ cycle_s_per_panel |
| boards/h theoretical | panels/h × boards_per_panel |
| CPH | boards/h × ppb |
| s per insertion | cycle ÷ ppp |
| planned boards/h | boards/h × efficiency |
| boards / shift | planned boards/h × hours_per_shift |
| boards / month (1 shift) | boards/shift × working_days_month |
| ramp week i | planned boards/h × hours × days_per_week × ramp[i]; cumulative sum |
| parts/h needed | planned boards/h × ppb |
| manual operators / shift | ceil(parts/h ÷ manual_parts_per_operator_hour) |
| cost per operator-month | monthly_wage × employer_factor |
| manual cost (n shifts) | n × manual operators × cost per operator |
| automated cost (n shifts) | n × machine_operators × cost per operator + machine_running_cost_month |
| net saving / month | manual − automated; yearly = × 12 |
| recovered in M months | net saving × M (payback = customer quote ÷ net saving) |
| operators released | manual operators − machine operators |
| productivity ratio | planned boards/h ÷ (manual rate ÷ ppb) |
| defects avoided / month | boards/month × ppb × (manual_ppm − machine_ppm) ÷ 10⁶ |

Rounding: calculate unrounded, round only for display (integers; 2 decimals for s/insertion; 1 decimal for ratio and factor; millions with 2 decimals).
Reference figures (Zebu example, v1.0.0): 514 panels/h, 1,029 boards/h, 11,314 CPH, 874 boards/h at 85 %, 6,994/shift, 153,874/month, 11 operators, R$ 32,096 vs R$ 3,468, saving R$ 28,628/month, R$ 343,536/year, 2 shifts R$ 57,806, 3 shifts R$ 86,984, 10.7×, 2,539 defects. Re-run after any change and compare.

## Evidence labels (learn-SMT-in-3-hours)
- **Measured** - from the sample test (cycle, boards/panel, program points, photos).
- **Verified source** - customer BOM, machine catalogue, official wage source.
- **Planning assumption / Concept view** - efficiency, manual rate, employer factor, manual PPM, running cost, ramp path.
- **To be confirmed** - anything the test did not prove (full-BOM cycle, body heights, panel outline).
Slide notes carry the sources; the assumptions slide lists every assumption and open point.

## Report structure (16 slides on the 202309 template)
1 Cover (4 key metrics) · 2 Why automate · 3 Test evidence · 4 BOM fit · 5 Capacity · 6 Ramp-up · 7 ROI manual vs automation · 8 Payback / break-even · 9 Why <machine> · 10 Benefits · 11 Gallery · 12 Machine specifications · 13 Assumptions & open points · 14 Next steps · 15-16 template after-sales and contact slides.
