import numpy as np
import pandas as pd


def _estimate_leverage(row):
    start_pos = row.get("Start Position", np.nan)
    if pd.notna(start_pos) and start_pos != 0:
        return abs(row["Size USD"]) / abs(start_pos)
    notional = abs(row["Execution Price"] * row["Size Tokens"])
    fee = abs(row.get("Fee", np.nan))
    if pd.notna(fee) and fee > 0:
        margin_proxy = fee / 0.0005
        if margin_proxy > 0:
            return notional / margin_proxy
    return np.nan


def create_daily_metrics(df):
    working = df.copy()
    working["Side"] = working["Side"].str.lower()
    working["leverage_proxy"] = working.apply(_estimate_leverage, axis=1)

    daily = (
        working.groupby(["Account", "Date"]).agg(
            daily_pnl=("Closed PnL", "sum"),
            trade_count=("Trade ID", "count"),
            avg_trade_size=("Size USD", "mean"),
            avg_leverage=("leverage_proxy", "mean"),
            long_trades=("Side", lambda x: (x == "buy").sum()),
            short_trades=("Side", lambda x: (x == "sell").sum()),
        )
    ).reset_index()

    daily["long_short_ratio"] = daily["long_trades"] / (daily["short_trades"] + 1)
    daily["win_day"] = (daily["daily_pnl"] > 0).astype(int)

    daily = daily.sort_values(["Account", "Date"])
    daily["cum_pnl"] = daily.groupby("Account")["daily_pnl"].cumsum()
    daily["rolling_peak"] = daily.groupby("Account")["cum_pnl"].cummax()
    daily["drawdown_proxy"] = daily["cum_pnl"] - daily["rolling_peak"]

    pnl_vol = daily.groupby("Account")["daily_pnl"].std().rename("pnl_volatility")
    daily = daily.merge(pnl_vol, on="Account", how="left")

    daily["lev_adjusted_pnl"] = daily["daily_pnl"] / daily["avg_leverage"].replace(0, np.nan)
    daily["pnl_per_unit_leverage"] = daily["daily_pnl"] / (daily["avg_leverage"].abs() + 1)

    return daily


def segment_traders(daily):
    seg = daily.copy()

    leverage_median = seg["avg_leverage"].median(skipna=True)
    freq_threshold = seg["trade_count"].quantile(0.75)

    account_win_rate = seg.groupby("Account")["win_day"].mean().rename("account_win_rate")
    account_pnl_std = seg.groupby("Account")["daily_pnl"].std().rename("account_pnl_std")
    consistency_cutoff = account_pnl_std.median(skipna=True)

    seg = seg.merge(account_win_rate, on="Account", how="left")
    seg = seg.merge(account_pnl_std, on="Account", how="left")

    seg["leverage_segment"] = np.where(seg["avg_leverage"] >= leverage_median, "High_Leverage", "Low_Leverage")
    seg["frequency_segment"] = np.where(seg["trade_count"] >= freq_threshold, "Frequent", "Infrequent")

    seg["consistency_segment"] = np.where(
        (seg["account_win_rate"] >= 0.60) | (seg["account_pnl_std"] <= consistency_cutoff),
        "Consistent",
        "Inconsistent",
    )

    return seg
