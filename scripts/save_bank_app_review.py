from pathlib import Path
import pandas as pd
from datetime import datetime

# Define and create the directory if it doesn't exist
DATA_DIR = Path('../data/raw/')
DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_scraped_data_to_csv(scraped_data: pd.DataFrame, bank_name: str):
    """
    Save scraped data to CSV file with proper error handling.

    Args:
        scraped_data (pd.DataFrame): DataFrame containing scraped reviews.
        bank_name (str): Name of the bank (used for the filename).

    Returns:
        Path to the saved file if successful, None otherwise.
    """
    try:
        # Validate input
        if not isinstance(scraped_data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")
        if scraped_data.empty:
            print(f"No data to save for {bank_name}.")
            return None

        # Prepare filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = DATA_DIR / f"{bank_name.lower()}_reviews_{timestamp}.csv"

        # Save the DataFrame to CSV
        scraped_data.to_csv(filename, index=False, encoding='utf-8')
        print(f"Successfully saved {len(scraped_data)} reviews to {filename}")
        return filename

    except Exception as e:
        print(f"Failed to save data for {bank_name}: {e}")
        return None
