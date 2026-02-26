from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import run_pipeline


TABLE_DIR = ROOT / "outputs" / "tables"

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Hyperliquid Sentiment Regime Dashboard", page_icon="📊", layout="wide")


@st.cache_data
def load_data():
    merged = pd.read_csv(TABLE_DIR / "account_day_merged.csv", parse_dates=["Date"])
    summary = pd.read_csv(TABLE_DIR / "sentiment_summary.csv")
    tests = pd.read_csv(TABLE_DIR / "statistical_tests.csv")
    segment = pd.read_csv(TABLE_DIR / "segment_performance.csv")
    ts = pd.read_csv(TABLE_DIR / "daily_regime_timeseries.csv", parse_dates=["Date"])
    feat_imp = pd.read_csv(TABLE_DIR / "model_feature_importance.csv")
    return merged, summary, tests, segment, ts, feat_imp


def ensure_outputs():
    required = [
        TABLE_DIR / "account_day_merged.csv",
        TABLE_DIR / "sentiment_summary.csv",
        TABLE_DIR / "statistical_tests.csv",
        TABLE_DIR / "segment_performance.csv",
        TABLE_DIR / "daily_regime_timeseries.csv",
        TABLE_DIR / "model_feature_importance.csv",
    ]
    if all(path.exists() for path in required):
        return
    with st.spinner("Generating outputs (first run only)..."):
        run_pipeline(verbose=False)
    load_data.clear()


st.title("Hyperliquid Trader Behavior vs Fear/Greed Regimes")
st.caption("Interactive dashboard for assignment review: performance, behavior shifts, segment diagnostics, and model signals.")

ensure_outputs()
merged, summary, tests, segment, ts, feat_imp = load_data()

with st.sidebar:
    st.header("Filters")
    sentiment_choice = st.multiselect(
        "Sentiment Regime",
        options=sorted(merged["Classification"].dropna().unique().tolist()),
        default=["Fear", "Greed"],
    )
    account_limit = st.slider("Rows in sample table", min_value=20, max_value=500, value=100, step=20)

filtered = merged[merged["Classification"].isin(sentiment_choice)].copy()

st.subheader("1) KPI Snapshot")
row1 = st.columns(4)
fear_pnl = summary.loc[summary["Classification"] == "Fear", "avg_daily_pnl"].iloc[0]
greed_pnl = summary.loc[summary["Classification"] == "Greed", "avg_daily_pnl"].iloc[0]
lev_shift = tests.loc[tests["metric"] == "avg_leverage", "pct_shift_greed_vs_fear"].iloc[0]
pnl_p = tests.loc[tests["metric"] == "daily_pnl", "p_value"].iloc[0]

row1[0].metric("Avg PnL (Fear)", f"{fear_pnl:,.0f}")
row1[1].metric("Avg PnL (Greed)", f"{greed_pnl:,.0f}", delta=f"{((greed_pnl-fear_pnl)/(abs(fear_pnl)+1e-6))*100:.1f}%")
row1[2].metric("Leverage Shift (Greed vs Fear)", f"{lev_shift:.1f}%")
row1[3].metric("PnL Regime p-value", f"{pnl_p:.4f}")

st.subheader("2) Regime-level Behavior & Performance")
col1, col2 = st.columns(2)

fig1, ax1 = plt.subplots(figsize=(7, 4))
sns.boxplot(data=filtered, x="Classification", y="daily_pnl", hue="Classification", palette={"Fear": "#d62728", "Greed": "#2ca02c"}, ax=ax1, legend=False)
ax1.set_title("Daily PnL Distribution by Sentiment")
col1.pyplot(fig1)

behavior_df = (
    filtered.groupby("Classification")[["trade_count", "avg_leverage", "avg_trade_size"]]
    .mean()
    .reset_index()
    .melt(id_vars="Classification", var_name="metric", value_name="value")
)
fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.barplot(data=behavior_df, x="metric", y="value", hue="Classification", palette={"Fear": "#d62728", "Greed": "#2ca02c"}, ax=ax2)
ax2.set_title("Behavior Shifts by Sentiment")
ax2.tick_params(axis="x", rotation=20)
col2.pyplot(fig2)

st.subheader("3) Time-Series Regime Lens")
metric_ts = st.selectbox("Select metric", ["total_pnl", "avg_win_rate", "avg_leverage", "active_accounts", "total_trades"])
ts_plot = ts[ts["Classification"].isin(sentiment_choice)].copy()
fig3, ax3 = plt.subplots(figsize=(12, 4))
sns.lineplot(data=ts_plot, x="Date", y=metric_ts, hue="Classification", marker="o", palette={"Fear": "#d62728", "Greed": "#2ca02c"}, ax=ax3)
ax3.set_title(f"{metric_ts} over time")
st.pyplot(fig3)

st.subheader("4) Segment Diagnostics")
segment_type = st.selectbox("Segment Type", ["leverage_segment", "frequency_segment", "consistency_segment"])
seg_df = segment[segment["segment_type"] == segment_type].copy()
id_col = [c for c in seg_df.columns if c.endswith("segment") and c != "segment_type"][0]
fig4, ax4 = plt.subplots(figsize=(9, 4))
sns.barplot(data=seg_df, x=id_col, y="avg_pnl", hue="Classification", palette={"Fear": "#d62728", "Greed": "#2ca02c"}, ax=ax4)
ax4.set_title(f"Average PnL by {segment_type}")
st.pyplot(fig4)

st.subheader("5) Predictive Signal Importance")
fi = feat_imp.sort_values("importance")
fig5, ax5 = plt.subplots(figsize=(8, 4))
ax5.barh(fi["feature"], fi["importance"], color="#1f77b4")
ax5.set_title("Feature Importance (Win-Day Model)")
st.pyplot(fig5)

st.subheader("6) Statistical Tests")
st.dataframe(tests.sort_values("p_value"), width="stretch")

st.subheader("7) Sample Account-Day Panel")
show_cols = [
    "Date",
    "Account",
    "Classification",
    "daily_pnl",
    "win_day",
    "trade_count",
    "avg_leverage",
    "long_short_ratio",
    "drawdown_proxy",
    "leverage_segment",
    "frequency_segment",
    "consistency_segment",
]
st.dataframe(filtered[show_cols].head(account_limit), width="stretch")
