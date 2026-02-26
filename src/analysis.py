import pandas as pd

def merge_sentiment(daily_metrics, sentiment_df):
    merged = daily_metrics.merge(sentiment_df, on='Date', how='left')
    return merged

def sentiment_comparison(df):

    summary = df.groupby('Classification').agg(
        avg_pnl=('daily_pnl', 'mean'),
        win_rate=('win_day', 'mean'),
        avg_leverage=('avg_leverage', 'mean'),
        avg_trade_count=('trade_count', 'mean')
    )

    return summary