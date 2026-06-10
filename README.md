# 📊 The Stagnant Safety Net: A Tri-State Forensic Audit

## Architected by The Data Vigilante (Sierra Napier, MPA)

An open-source programmatic model isolating the institutional, unindexed decay of the Unemployment Insurance safety net frameworks across the DMV area (District of Columbia, Maryland, and Virginia).

## 📐 Forensic Metrics Defined

1. **Benefit Adequacy Index (BAI)** `BAI = Max_WBA / Median_Weekly_Housing_Costs`
    Isolates whether the maximum weekly benefit cap programmatically forces a choice between rent and immediate starvation. Any index $< 1.0$ indicates systemic failure.

2. **Regressive Wage Base Index (WBI)** `WBI = Statutory_Taxable_Wage_Base / State_Average_Annual_Wage`
 Exposes the regressive nature of flat SUI caps (e.g., Maryland's $8,500 base frozen since 1992), proving that corporations stop funding the safety net almost immediately each fiscal year.

3. **Multi-Income Penalty Index (MIPI)** `MIPI = (Part_Time_Earnings - Income_Disregard) / Max_WBA`  
 Measures the institutional "clawback penalty" applied to resourceful workers trying to cushion their own insolvency with secondary part-time work.

## 🚀 Environment Quickstart

```bash
pip install -r requirements.txt
python ui_index_engine.py
```

Once you drop these files into your Codespace workspace, you'll be able to run `python ui_index_engine.py` right in your terminal, see the matrix parse flawlessly, and push it up to main whenever you're ready!
