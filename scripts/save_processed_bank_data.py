import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory setup - using proper path joining
RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

# Create directories if they don't exist
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_processed_bank_data(df: pd.DataFrame, bank_name: str) -> Path:
    """
    Save processed bank review data to CSV
    Args:
        df: Processed DataFrame to save
        bank_name: Name of the bank (used in filename)
    Returns:
        Path to the saved file or None if failed
    """
    if df.empty:
        logger.warning(f"No data to save for {bank_name}")
        return None

    try:
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = PROCESSED_DATA_DIR / f"{bank_name.lower()}_processed_{timestamp}.csv"

        # Save to CSV
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Successfully saved {len(df)} reviews to {filename}")
        return filename

    except Exception as e:
        logger.error(f"Failed to save {bank_name} data: {str(e)}", exc_info=True)
        return None