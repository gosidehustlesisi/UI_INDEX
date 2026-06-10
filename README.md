# 📊 The Stagnant Safety Net: A Tri-State Forensic Audit

**Architected by The Data Vigilante (Sierra Napier, MPA)**

An open-source comparative static model isolating the institutional decay of Unemployment Insurance safety net frameworks across the DMV area (District of Columbia, Maryland, and Virginia). Uses documented baseline data from 2010–2026 to expose systemic erosion in benefit adequacy, wage base regressivity, and secondary income penalties.

## 📐 Forensic Metrics Defined

### 1. Benefit Adequacy Index (BAI)
`BAI = Max_WBA / Median_Weekly_Housing_Costs`

Isolates whether the maximum weekly benefit cap forces a choice between rent and immediate survival. Any index < 1.0 indicates systemic failure.

### 2. Regressive Wage Base Index (WBI)
`WBI = Statutory_Taxable_Wage_Base / State_Average_Annual_Wage`

Exposes the regressive nature of flat SUI caps. Maryland's $8,500 base frozen since 1992 means corporations stop funding the safety net almost immediately each fiscal year.

### 3. Multi-Income Penalty Index (MIPI)
`MIPI = (Part_Time_Earnings - Income_Disregard) / Max_WBA`

Measures the institutional clawback penalty applied to resourceful workers trying to cushion insolvency with secondary part-time work.

## 📁 Data Source

Primary data is stored in `data/dmv_macro_baselines.csv`, documenting:
- Maximum Weekly Benefit Amount (WBA) by jurisdiction and year
- Statutory Taxable Wage Base (SUI cap)
- Average Annual Wage (BLS-derived estimates)
- Weekly Housing Costs (HUD FMR-derived estimates)

Years covered: 2010, 2018, 2026

## 🚀 Environment Quickstart

```bash
pip install -r requirements.txt
python ui_index_engine.py
```

## 🛠️ Methodology Note

This model uses **documented comparative static baselines** rather than live API polling. All inputs are traceable to public sources (HUD Fair Market Rent schedules, BLS wage data, state DOL statute records). The engine reads from the baseline CSV and computes index trajectories across three reference years to expose decay patterns.

## 📈 Output

The engine generates a formatted dashboard showing all three indices across DC, MD, and VA for 2010, 2018, and 2026, plus a systemic status flag (CRITICAL DECAY / STABLE).

## 📊 Visual Analysis

See `ui_index_analysis.ipynb` for full interactive charts showing BAI decay trajectories, WBI stagnation, and MIPI clawback severity across the 16-year window.

## 📝 License

MIT — see [LICENSE](LICENSE)
