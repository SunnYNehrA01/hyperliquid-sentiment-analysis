# Hyperliquid: Trader Behavior vs Fear/Greed

A small data project that studies how Hyperliquid trader behavior changes across market sentiment regimes.

## What is included
- Daily account-level feature pipeline
- Fear vs Greed comparison with statistical testing
- Trader segmentation (leverage, activity, consistency)
- Simple profitability model + feature importance
- Streamlit dashboard for exploration

## Run locally
```bash
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
```

## Streamlit Cloud
Set the entrypoint to:

`app/streamlit_app.py`

If output tables are missing, the app will generate them automatically.

## Project files
- `src/pipeline.py` — orchestration
- `src/analysis_core.py` — analysis logic
- `src/analysis.py` — stable wrapper API
- `app/streamlit_app.py` — dashboard
- `main.py` — CLI entrypoint

## Notes
- `outputs/**` is ignored by git (except `outputs/.gitkeep`) to avoid merge conflicts from generated files.
- The available trade window is short, so results should be treated as directional.
