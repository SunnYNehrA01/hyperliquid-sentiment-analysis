import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu


def merge_sentiment(daily_metrics, sentiment_df):
    merged = daily_metrics.merge(sentiment_df, on="Date", how="left", indicator=True)

    unmatched_trading_days = merged.loc[merged["_merge"] == "left_only", "Date"].nunique()
    unmatched_sentiment_days = sentiment_df.loc[~sentiment_df["Date"].isin(daily_metrics["Date"]), "Date"].nunique()
    alignment_rate = (merged["_merge"] == "both").mean()

    merge_report = {
        "trading_days": int(daily_metrics["Date"].nunique()),
        "sentiment_days": int(sentiment_df["Date"].nunique()),
        "unmatched_trading_days": int(unmatched_trading_days),
        "unmatched_sentiment_days": int(unmatched_sentiment_days),
        "alignment_rate": float(alignment_rate),
    }

    assert merge_report["alignment_rate"] > 0.5, "Low alignment rate between datasets"

    merged = merged.drop(columns=["_merge"])
    return merged, merge_report


def sentiment_comparison(df):
    filtered = df[df["Classification"].isin(["Fear", "Greed"])].copy()

    summary = (
        filtered.groupby("Classification").agg(
            avg_daily_pnl=("daily_pnl", "mean"),
            median_daily_pnl=("daily_pnl", "median"),
            win_rate=("win_day", "mean"),
            pnl_volatility=("daily_pnl", "std"),
            avg_drawdown_proxy=("drawdown_proxy", "mean"),
            avg_trade_count=("trade_count", "mean"),
            avg_leverage=("avg_leverage", "mean"),
            avg_trade_size=("avg_trade_size", "mean"),
            avg_long_short_ratio=("long_short_ratio", "mean"),
        )
    ).reset_index()

    tests = {}
    metrics = ["daily_pnl", "win_day", "trade_count", "avg_leverage", "long_short_ratio", "drawdown_proxy"]
    fear = filtered[filtered["Classification"] == "Fear"]
    greed = filtered[filtered["Classification"] == "Greed"]

    for metric in metrics:
        fear_vals = fear[metric].dropna()
        greed_vals = greed[metric].dropna()
        if len(fear_vals) > 20 and len(greed_vals) > 20:
            stat, pvalue = mannwhitneyu(fear_vals, greed_vals, alternative="two-sided")
            tests[metric] = {
                "statistic": float(stat),
                "p_value": float(pvalue),
                "fear_median": float(fear_vals.median()),
                "greed_median": float(greed_vals.median()),
                "pct_shift_greed_vs_fear": float(((greed_vals.median() - fear_vals.median()) / (abs(fear_vals.median()) + 1e-9)) * 100),
            }
        else:
            tests[metric] = {
                "statistic": np.nan,
                "p_value": np.nan,
                "fear_median": np.nan,
                "greed_median": np.nan,
                "pct_shift_greed_vs_fear": np.nan,
            }

    tests_df = pd.DataFrame(tests).T.reset_index().rename(columns={"index": "metric"})
    return summary, tests_df


def segment_performance(df):
    filtered = df[df["Classification"].isin(["Fear", "Greed"])].copy()
    segment_cols = ["leverage_segment", "frequency_segment", "consistency_segment"]

    out = []
    for seg_col in segment_cols:
        agg = (
            filtered.groupby([seg_col, "Classification"]).agg(
                avg_pnl=("daily_pnl", "mean"),
                win_rate=("win_day", "mean"),
                pnl_std=("daily_pnl", "std"),
                drawdown=("drawdown_proxy", "mean"),
                trades=("trade_count", "mean"),
                avg_leverage=("avg_leverage", "mean"),
            )
        ).reset_index()
        agg["segment_type"] = seg_col
        out.append(agg)

    return pd.concat(out, ignore_index=True)


def daily_regime_timeseries(df):
    filtered = df[df["Classification"].isin(["Fear", "Greed"])].copy()
    ts = (
        filtered.groupby(["Date", "Classification"]).agg(
            total_pnl=("daily_pnl", "sum"),
            avg_win_rate=("win_day", "mean"),
            avg_leverage=("avg_leverage", "mean"),
            active_accounts=("Account", "nunique"),
            total_trades=("trade_count", "sum"),
        )
    ).reset_index()
    return ts
