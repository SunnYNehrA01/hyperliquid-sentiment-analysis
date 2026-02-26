import pandas as pd


def preprocess_fear_greed(df):
    sentiment = df.copy()
    sentiment.columns = [c.strip() for c in sentiment.columns]

    sentiment["Date"] = pd.to_datetime(sentiment["date"], errors="coerce").dt.normalize()
    sentiment["Classification"] = sentiment["classification"].fillna("Unknown")
    sentiment["Classification"] = sentiment["Classification"].replace(
        {"Extreme Fear": "Fear", "Extreme Greed": "Greed"}
    )
    sentiment["sentiment"] = sentiment["Classification"].map({"Fear": 0, "Greed": 1})

    sentiment = sentiment[["Date", "Classification", "sentiment", "value"]].dropna(subset=["Date"])
    sentiment = sentiment.drop_duplicates(subset=["Date"], keep="last")
    return sentiment


def preprocess_trader_data(df):
    trader = df.copy()
    trader.columns = [c.strip() for c in trader.columns]

    trader["Closed PnL"] = pd.to_numeric(trader["Closed PnL"], errors="coerce")
    trader["Size USD"] = pd.to_numeric(trader["Size USD"], errors="coerce")
    trader["Execution Price"] = pd.to_numeric(trader["Execution Price"], errors="coerce")
    trader["Size Tokens"] = pd.to_numeric(trader["Size Tokens"], errors="coerce")

    ts_raw = pd.to_numeric(trader["Timestamp"], errors="coerce")
    # Handle ms timestamps (13 digits)
    trader["time"] = pd.to_datetime(ts_raw, unit="ms", errors="coerce", utc=True)
    trader["Date"] = trader["time"].dt.tz_convert(None).dt.normalize()

    trader = trader.dropna(subset=["Date", "Account", "Closed PnL"])
    trader = trader.drop_duplicates()
    return trader
