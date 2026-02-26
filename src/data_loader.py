import pandas as pd


def load_fear_greed(path):
    return pd.read_csv(path)


def load_trader_data(path):
    return pd.read_csv(path)


def dataset_audit(df, name="Dataset"):
    info = {
        "dataset": name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
    }
    return info


def print_audit(info):
    print(f"\n=== {info['dataset']} Audit ===")
    print(f"Rows: {info['rows']} | Columns: {info['columns']}")
    print(f"Columns: {info['column_names']}")
    print(f"Dtypes: {info['dtypes']}")
    print(f"Missing Values: {info['missing_values']}")
    print(f"Duplicate Rows: {info['duplicate_rows']}")
