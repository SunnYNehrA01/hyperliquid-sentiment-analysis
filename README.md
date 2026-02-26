# Hyperliquid Trader Performance vs Market Sentiment (Fear/Greed Regime Study)

This repository is structured as an interview-ready, reproducible submission for the **Trader Performance vs Market Sentiment** assignment.

## ✅ Requirement Coverage Checklist

### Part A — Data Preparation
- [x] Dataset audit: rows, columns, dtypes, missing values, duplicates.
- [x] Timestamp normalization for both sentiment and trades.
- [x] Daily alignment by `Date` with merge diagnostics:
  - unmatched trading days
  - unmatched sentiment days
  - alignment rate assertion
- [x] Key daily metrics:
  - Daily PnL, win-day, PnL volatility, drawdown proxy
  - Trade count, avg size, avg leverage proxy, long/short ratio
  - Leverage-adjusted PnL features
- [x] Segmentation:
  - High vs Low leverage
  - Frequent vs Infrequent
  - Consistent vs Inconsistent

### Part B — Analysis
- [x] Fear vs Greed performance comparison with summary table.
- [x] Behavior shift analysis (trade frequency, leverage, size, long/short).
- [x] Statistical significance via Mann–Whitney tests with p-values.
- [x] Segment-level regime analysis tables.
- [x] Charts saved for evidence.

### Part C — Actionable Output
- [x] Segment-aware strategy rules in `outputs/strategy_recommendations.md`.
- [x] 1-page executive write-up in `outputs/executive_summary.md`.

### Bonus
- [x] Predictive model (Random Forest) with feature-importance report.
- [x] Lightweight Streamlit dashboard for exploration.

---

## Repository Structure

- `main.py` — end-to-end pipeline entrypoint.
- `src/` — modular data science code.
- `app/streamlit_app.py` — interactive dashboard.
- `Data/` — input datasets.
- `outputs/` — generated artifacts.

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
```

> For Streamlit Cloud: set main file path to `app/streamlit_app.py`.

---

## Generated Outputs

### Tables
- `outputs/tables/account_day_merged.csv`
- `outputs/tables/daily_regime_timeseries.csv`
- `outputs/tables/sentiment_summary.csv`
- `outputs/tables/statistical_tests.csv`
- `outputs/tables/segment_performance.csv`
- `outputs/tables/model_feature_importance.csv`
- `outputs/tables/merge_report.json`
- `outputs/tables/classification_report.txt`

### Figures
- `outputs/figures/pnl_by_sentiment.png`
- `outputs/figures/behavior_shift.png`
- `outputs/figures/segment_heatmap.png`

### Writeups
- `outputs/strategy_recommendations.md`
- `outputs/executive_summary.md`

---

## Notes / Limitations

- The aligned trade window is short (few days), so findings are directional and should be re-tested on longer history.
- Leverage uses a proxy estimate from available fields (not explicit exchange leverage).
- Drawdown proxy is from cumulative daily realized PnL (not full equity curve mark-to-market).
