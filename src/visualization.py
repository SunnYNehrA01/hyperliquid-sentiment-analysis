import matplotlib.pyplot as plt
import seaborn as sns

def plot_pnl_by_sentiment(df, output_path=None):
    plt.figure()
    sns.boxplot(x='Classification', y='daily_pnl', data=df)
    plt.title("PnL Distribution by Sentiment")
    if output_path:
        plt.savefig(output_path)
    plt.close()

def plot_leverage_distribution(df, output_path=None):
    plt.figure()
    sns.boxplot(x='Classification', y='avg_leverage', data=df)
    plt.title("Leverage by Sentiment")
    if output_path:
        plt.savefig(output_path)
    plt.close()