"""Public analysis API.

This module intentionally stays small and stable to reduce merge conflicts.
Core implementations live in :mod:`src.analysis_core`.
"""

from src.analysis_core import (
    daily_regime_timeseries_impl,
    merge_sentiment_impl,
    segment_performance_impl,
    sentiment_comparison_impl,
)


def merge_sentiment(daily_metrics, sentiment_df):
    return merge_sentiment_impl(daily_metrics, sentiment_df)


def sentiment_comparison(df):
    return sentiment_comparison_impl(df)


def segment_performance(df):
    return segment_performance_impl(df)


def daily_regime_timeseries(df):
    return daily_regime_timeseries_impl(df)
