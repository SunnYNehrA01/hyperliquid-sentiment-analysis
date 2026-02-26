import pandas as pd

def load_fear_greed(path):
    df = pd.read_csv(path)
    return df

def load_trader_data(path):
    df = pd.read_csv(path)
    return df

def basic_info(df, name="Dataset"):
    print(f"\n{name} Shape: {df.shape}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nDuplicates: {df.duplicated().sum()}")