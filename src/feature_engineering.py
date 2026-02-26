import pandas as pd
import numpy as np

def create_daily_metrics(df):

    daily = df.groupby(['account', 'Date']).agg(
        daily_pnl=('closedPnL', 'sum'),
        trade_count=('account', 'count'),
        avg_size=('size', 'mean'),
        avg_leverage=('leverage', 'mean'),
        long_trades=('side', lambda x: (x == 'long').sum()),
        short_trades=('side', lambda x: (x == 'short').sum())
    ).reset_index()

    daily['win_day'] = (daily['daily_pnl'] > 0).astype(int)
    daily['long_short_ratio'] = daily['long_trades'] / (daily['short_trades'] + 1)

    return daily

def segment_traders(df):

    leverage_median = df['avg_leverage'].median()
    trade_median = df['trade_count'].median()

    df['leverage_segment'] = df['avg_leverage'].apply(
        lambda x: 'High_Leverage' if x > leverage_median else 'Low_Leverage'
    )

    df['frequency_segment'] = df['trade_count'].apply(
        lambda x: 'Frequent' if x > trade_median else 'Infrequent'
    )

    return df