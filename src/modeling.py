from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def profitability_model(df):

    features = ['sentiment', 'avg_leverage', 'trade_count', 'long_short_ratio']
    df = df.dropna()

    X = df[features]
    y = df['win_day']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print(classification_report(y_test, preds))

    return model