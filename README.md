# Hyperliquid Trader Performance vs Market Sentiment (Fear/Greed Regime Study)

This repository is an interview-ready, reproducible submission for the **Trader Performance vs Market Sentiment** assignment.

## ✅ Requirement Coverage Checklist

### Part A — Data Preparation
- [x] Dataset audit: rows, columns, dtypes, missing values, duplicates.
- [x] Timestamp normalization for both sentiment and trades.
- [x] Daily alignment by `Date` with merge diagnostics (unmatched dates + alignment rate assertion).
- [x] Key account-day metrics: PnL, win-day, volatility, drawdown proxy, trade count, avg size, leverage proxy, long/short ratio, leverage-adjusted metrics.
- [x] Segmentation: leverage / frequency / consistency.

### Part B — Analysis
- [x] Fear vs Greed performance comparison.
- [x] Behavior shifts (frequency, leverage, trade size, long/short).
- [x] Statistical testing via Mann–Whitney U test + p-values.
- [x] Segment-level regime analysis.

### Part C — Actionable Output
- [x] Segment-aware strategy rules.
- [x] One-page executive summary.

### Bonus
- [x] Predictive model (Random Forest) + feature importance.
- [x] Lightweight Streamlit dashboard.

---

## Repository Structure

- `main.py` — end-to-end pipeline orchestration (`run_pipeline`).
- `src/` — modular analysis code.
- `app/streamlit_app.py` — dashboard.
- `Data/` — input data.
- `outputs/` — generated artifacts (created locally/on deploy at runtime).

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
```

### Streamlit Cloud
Set app entrypoint to:

`app/streamlit_app.py`

The dashboard auto-generates required output tables on first run, so no pre-committed CSV artifacts are required.

---

## Why merge conflicts are now reduced

Generated files under `outputs/` are intentionally **not version-controlled** anymore. This avoids repeated PR conflicts on machine-generated CSV/Markdown artifacts while preserving full reproducibility through `python main.py`.

---

## Notes / Limitations

- The aligned trade window is short, so results are directional and should be re-validated on longer history.
- Leverage is proxy-estimated from available fields.
- Drawdown proxy uses cumulative realized daily PnL, not full mark-to-market equity curves.
