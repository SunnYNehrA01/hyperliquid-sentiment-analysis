from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def profitability_model(df):
    model_df = df[df["Classification"].isin(["Fear", "Greed"])].dropna(
        subset=["sentiment", "avg_leverage", "trade_count", "long_short_ratio", "win_day"]
    )

    features = ["sentiment", "avg_leverage", "trade_count", "long_short_ratio", "avg_trade_size"]
    X = model_df[features]
    y = model_df["win_day"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    report = classification_report(y_test, preds)

    import pandas as pd

    importances = (
        pd.Series(model.feature_importances_, index=features, name="importance")
        .reset_index()
        .rename(columns={"index": "feature"})
        .sort_values("importance", ascending=False)
    )

    return model, report, importances
