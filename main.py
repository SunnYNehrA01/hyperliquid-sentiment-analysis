from src.config import *
from src.data_loader import *
from src.preprocessing import *
from src.feature_engineering import *
from src.analysis import *
from src.visualization import *
from src.modeling import *

def run():

    fg = load_fear_greed(FEAR_GREED_PATH)
    trader = load_trader_data(TRADER_DATA_PATH)

    basic_info(fg, "Fear Greed")
    basic_info(trader, "Trader Data")

    fg = preprocess_fear_greed(fg)
    trader = preprocess_trader_data(trader)

    daily = create_daily_metrics(trader)
    daily = segment_traders(daily)

    merged = merge_sentiment(daily, fg)

    summary = sentiment_comparison(merged)
    print(summary)

    plot_pnl_by_sentiment(merged, OUTPUT_DIR / "figures/pnl_sentiment.png")
    plot_leverage_distribution(merged, OUTPUT_DIR / "figures/leverage_sentiment.png")

    profitability_model(merged)

if __name__ == "__main__":
    run()