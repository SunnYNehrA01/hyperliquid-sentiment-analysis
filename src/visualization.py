import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def plot_pnl_by_sentiment(df, output_path):
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="Classification", y="daily_pnl", data=df[df["Classification"].isin(["Fear", "Greed"])])
    plt.title("Daily PnL Distribution by Sentiment Regime")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_behavior_shift(df, output_path):
    plot_df = (
        df[df["Classification"].isin(["Fear", "Greed"])]
        .groupby("Classification")[["trade_count", "avg_leverage", "avg_trade_size"]]
        .mean()
        .reset_index()
        .melt(id_vars="Classification", var_name="metric", value_name="value")
    )

    plt.figure(figsize=(10, 5))
    sns.barplot(data=plot_df, x="metric", y="value", hue="Classification")
    plt.title("Behavioral Metrics Across Sentiment Regimes")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_segment_heatmap(segment_df, output_path):
    focus = segment_df[segment_df["segment_type"] == "leverage_segment"]
    pivot = focus.pivot(index="leverage_segment", columns="Classification", values="avg_pnl")
    plt.figure(figsize=(6, 4))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="RdYlGn")
    plt.title("Avg PnL by Leverage Segment and Sentiment")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
