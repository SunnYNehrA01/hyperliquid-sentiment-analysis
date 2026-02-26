# Hyperliquid Trader Performance vs Market Sentiment (Fear/Greed Regime Study)

This project analyzes how **market sentiment regimes (Fear vs Greed)** influence trader behavior, risk-taking, and profitability dynamics on Hyperliquid.

## Project Structure

- `main.py` — end-to-end pipeline runner.
- `src/` — modular code for loading, preprocessing, feature engineering, analysis, visualization, and modeling.
- `Data/` — input CSV files.
- `outputs/` — generated charts, tables, and strategy recommendations.

## Methodology

### Part A — Data preparation

1. Audited both datasets:
   - rows/columns
   - column names + dtypes
   - missing values
   - duplicate rows
2. Standardized and parsed timestamps:
   - sentiment date parsing
   - trader millisecond timestamp parsing
3. Aligned data daily (`Date`) and produced a merge quality report:
   - unmatched trading days
   - unmatched sentiment days
   - alignment rate + assertion check
4. Built account-day metrics:
   - daily PnL, win-day flag
   - trade count, average trade size, average leverage proxy
   - long/short ratio
   - PnL volatility per account
   - drawdown proxy using cumulative PnL peak-to-trough
   - leverage-adjusted PnL

### Part B — Analysis

1. Fear vs Greed comparison for:
   - average/median daily PnL
   - win rate
   - volatility
   - drawdown proxy
   - behavior shifts (trade count, leverage, size, long/short ratio)
2. Statistical testing via Mann–Whitney U test with p-values.
3. Segment analysis across sentiment:
   - High vs Low leverage
   - Frequent vs Infrequent traders
   - Consistent vs Inconsistent traders

### Part C — Actionable output

Rules are generated in `outputs/strategy_recommendations.md` using observed regime and segment-level risk/performance differences.

## Key Findings (Current Data Snapshot)

- Daily PnL differs significantly between Fear and Greed regimes (Mann–Whitney `p=0.0134`).
- Trader activity and leverage usage shift materially across regimes:
  - trade count difference is significant (`p=0.00006`)
  - leverage difference is significant (`p=0.00179`)
- Model feature importance suggests behavior features (long/short ratio, trade count, size) are stronger than sentiment alone for predicting next-day win/loss.

> Note: The provided trader data spans a short date window, so results should be treated as directional and re-validated on longer history.

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

## Outputs Produced

- Figures:
  - `outputs/figures/pnl_by_sentiment.png`
  - `outputs/figures/behavior_shift.png`
  - `outputs/figures/segment_heatmap.png`
- Tables:
  - `outputs/tables/sentiment_summary.csv`
  - `outputs/tables/statistical_tests.csv`
  - `outputs/tables/segment_performance.csv`
  - `outputs/tables/model_feature_importance.csv`
  - `outputs/tables/merge_report.json`
  - `outputs/tables/classification_report.txt`
- Strategy rules:
  - `outputs/strategy_recommendations.md`

## Limitations

- Trader data period is short (few trading days after alignment).
- Leverage is approximated with available fields (proxy method), not an exchange-provided explicit leverage column.
- Drawdown proxy is based on cumulative daily PnL (account-level), not mark-to-market equity curves.
