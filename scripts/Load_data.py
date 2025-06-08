
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory setup
RAW_DATA_DIR = Path(__file__).resolve().parent / "../../data/raw"

def load_bank_data(bank_name: str) -> pd.DataFrame:
    """Load and combine all CSV files for a specific bank."""
    try:
        bank_files = list(RAW_DATA_DIR.glob(f"{bank_name.lower()}_reviews_*.csv"))
        if not bank_files:
            logger.warning(f"No files found for bank: {bank_name}")
            return pd.DataFrame()

        dfs = []
        for file in bank_files:
            df = pd.read_csv(file)

            # Normalize columns
            df.columns = df.columns.str.strip().str.lower()

            # Add source tracking
            df['source_file'] = file.name
            dfs.append(df)

        combined = pd.concat(dfs, ignore_index=True)
        logger.info(f"✅ Loaded {len(combined)} reviews for {bank_name}")
        return combined

    except Exception as e:
        logger.error(f"❌ Error loading data for {bank_name}: {str(e)}")
        return pd.DataFrame()
