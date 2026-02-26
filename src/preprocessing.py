import pandas as pd

def preprocess_fear_greed(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['sentiment'] = df['Classification'].map({'Fear': 0, 'Greed': 1})
    return df[['Date', 'Classification', 'sentiment']]

def preprocess_trader_data(df):
    df['time'] = pd.to_datetime(df['time'])
    df['Date'] = df['time'].dt.date
    df['Date'] = pd.to_datetime(df['Date'])
    return df