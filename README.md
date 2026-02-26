# Hyperliquid Sentiment Regime Analysis

Assignment repo for analyzing trader behavior/performance under Fear vs Greed regimes, with a lightweight Streamlit dashboard.

## Run locally

```bash
pip install -r requirements.txt
python main.py
streamlit run app/streamlit_app.py
```

## Streamlit Cloud

Use `app/streamlit_app.py` as the app entrypoint.

The app auto-generates `outputs/tables/*` on first run using the same pipeline logic.

## Important merge-conflict note

Generated files under `outputs/` are intentionally not tracked by git (`outputs/**` ignored, only `outputs/.gitkeep` kept). This avoids repeated merge conflicts in machine-generated artifacts.

## Project layout

- `main.py`: minimal CLI entrypoint
- `src/pipeline.py`: orchestration logic
- `src/analysis.py`: lightweight wrappers
- `src/analysis_core.py`: analysis implementations
- `app/streamlit_app.py`: dashboard
