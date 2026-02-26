# Hyperliquid Trader Performance vs Market Sentiment (Fear/Greed Regime Study)

This project analyzes how **market sentiment regimes (Fear vs Greed)** influence trader behavior, risk-taking, and profitability dynamics on Hyperliquid.

## Run locally

```bash
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
```

## Streamlit Cloud

Use `app/streamlit_app.py` as the entrypoint.  
The app auto-generates `outputs/tables/*` on first run via the same pipeline logic.

## Conflict-safe structure (resolved)

To avoid recurring merge conflicts in frequently-edited files:

- `main.py` is a **thin entrypoint** that only calls pipeline orchestration.
- `src/analysis.py` is a **thin API wrapper**.
- Core logic lives in stable implementation modules:
  - `src/pipeline.py`
  - `src/analysis_core.py`

Generated artifacts under `outputs/` are not tracked in git (`outputs/**` ignored, keeping `outputs/.gitkeep` only).

## Project layout

- `main.py`: minimal CLI runner.
- `src/pipeline.py`: end-to-end orchestration.
- `src/analysis.py`: compatibility wrappers.
- `src/analysis_core.py`: analysis implementations.
- `app/streamlit_app.py`: lightweight dashboard.

## What the pipeline covers

- Dataset audit (rows/cols/dtypes/missing/duplicates)
- Timestamp parsing and daily alignment with merge diagnostics
- Feature engineering (PnL, behavior, risk, drawdown proxy, segmentation)
- Regime comparison + Mann–Whitney significance testing
- Segment-level analysis
- Predictive model + feature importances
- Saved tables/figures + executive summary + strategy recommendations
