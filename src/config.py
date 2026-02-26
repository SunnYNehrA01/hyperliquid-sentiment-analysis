from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
TABLE_DIR = OUTPUT_DIR / "tables"

FEAR_GREED_PATH = DATA_DIR / "fear_greed_index.csv"
TRADER_DATA_PATH = DATA_DIR / "historical_data.csv"
