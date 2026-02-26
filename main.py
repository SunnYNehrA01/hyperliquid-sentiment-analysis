import json
from pathlib import Path

from src.analysis import merge_sentiment, segment_performance, sentiment_comparison
from src.config import FEAR_GREED_PATH, FIGURE_DIR, OUTPUT_DIR, TABLE_DIR, TRADER_DATA_PATH
from src.data_loader import dataset_audit, load_fear_greed, load_trader_data, print_audit
from src.feature_engineering import create_daily_metrics, segment_traders
from src.modeling import profitability_model
from src.preprocessing import preprocess_fear_greed, preprocess_trader_data
from src.visualization import plot_behavior_shift, plot_pnl_by_sentiment, plot_segment_heatmap


def _ensure_dirs():
    for path in [OUTPUT_DIR, FIGURE_DIR, TABLE_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def _save_actionable_rules(summary_df, segment_df, model_importances):
    fear = summary_df.loc[summary_df["Classification"] == "Fear"].iloc[0]
    greed = summary_df.loc[summary_df["Classification"] == "Greed"].iloc[0]

    pnl_delta = ((greed["avg_daily_pnl"] - fear["avg_daily_pnl"]) / (abs(fear["avg_daily_pnl"]) + 1e-6)) * 100
    lev_delta = ((greed["avg_leverage"] - fear["avg_leverage"]) / (abs(fear["avg_leverage"]) + 1e-6)) * 100

    high_lev = segment_df[(segment_df["segment_type"] == "leverage_segment") & (segment_df["leverage_segment"] == "High_Leverage")]
    high_fear_var = float(high_lev[high_lev["Classification"] == "Fear"]["pnl_std"].iloc[0])
    high_greed_var = float(high_lev[high_lev["Classification"] == "Greed"]["pnl_std"].iloc[0])

    top_feature = model_importances.iloc[0]["feature"]

    rules = [
        f"Rule 1: In Fear regimes, high-leverage traders show high risk (PnL std={high_fear_var:.2f} vs Greed {high_greed_var:.2f}). Cap leverage and reduce position size for this segment.",
        f"Rule 2: Greed regime average leverage is {lev_delta:.1f}% above Fear and average PnL shifts by {pnl_delta:.1f}%. Increase activity only for consistent/frequent segments with tight risk limits.",
        f"Rule 3: The predictive model ranks '{top_feature}' as the strongest signal for next-day profitability; prioritize this metric in monitoring dashboards.",
    ]

    (OUTPUT_DIR / "strategy_recommendations.md").write_text("\n\n".join(rules))


def run():
    _ensure_dirs()

    fg_raw = load_fear_greed(FEAR_GREED_PATH)
    trader_raw = load_trader_data(TRADER_DATA_PATH)

    fg_audit = dataset_audit(fg_raw, "Fear/Greed Raw")
    trader_audit = dataset_audit(trader_raw, "Trader Raw")
    print_audit(fg_audit)
    print_audit(trader_audit)

    fg = preprocess_fear_greed(fg_raw)
    trader = preprocess_trader_data(trader_raw)

    daily = create_daily_metrics(trader)
    daily = segment_traders(daily)

    merged, merge_report = merge_sentiment(daily, fg)
    summary, stats_tests = sentiment_comparison(merged)
    segment_df = segment_performance(merged)

    model, clf_report, model_importances = profitability_model(merged)
    _ = model

    summary.to_csv(TABLE_DIR / "sentiment_summary.csv", index=False)
    stats_tests.to_csv(TABLE_DIR / "statistical_tests.csv", index=False)
    segment_df.to_csv(TABLE_DIR / "segment_performance.csv", index=False)
    model_importances.to_csv(TABLE_DIR / "model_feature_importance.csv", index=False)

    (TABLE_DIR / "classification_report.txt").write_text(clf_report)
    (TABLE_DIR / "merge_report.json").write_text(json.dumps(merge_report, indent=2))

    plot_pnl_by_sentiment(merged, FIGURE_DIR / "pnl_by_sentiment.png")
    plot_behavior_shift(merged, FIGURE_DIR / "behavior_shift.png")
    plot_segment_heatmap(segment_df, FIGURE_DIR / "segment_heatmap.png")

    _save_actionable_rules(summary, segment_df, model_importances)

    print("\nSentiment Summary:\n", summary)
    print("\nStatistical Tests:\n", stats_tests)
    print("\nMerge Report:\n", merge_report)
    print("\nTop Model Features:\n", model_importances.head(5))


if __name__ == "__main__":
    run()
