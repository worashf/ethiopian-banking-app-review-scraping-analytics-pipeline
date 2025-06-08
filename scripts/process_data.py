import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
import re
import numpy as np

from scripts import  load_bank_data, save_processed_bank_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




def preprocess_reviews(df: pd.DataFrame, bank_name: str) -> pd.DataFrame:
    """
    Clean and standardize review data with robust NaN handling.
    Returns DataFrame with columns: review_id, review, rating, date, bank, source, helpful_votes
    """
    try:

        df_clean = df.copy()

        # 1. Initial NaN check
        logger.info(f"\nInitial NaN check for {bank_name}:")
        logger.info(df_clean.isna().sum())
        logger.info(df_clean.columns)

        # Check reviewId existence and quality
        if 'reviewid' not in df_clean.columns:
            logger.error("reviewId column missing - cannot process")
            return pd.DataFrame()

        # 3. NaN and duplicate analysis
        nan_ids = df_clean['reviewid'].isna().sum()
        dup_ids = df_clean['reviewid'].duplicated().sum()



        logger.info(f"Found {nan_ids} NaN reviewIds")
        logger.info(f"Found {dup_ids} duplicate reviewIds")

        # 4. Handle missing reviewIds
        if nan_ids > 0:
            logger.warning("Rows with NaN reviewIds will be dropped")
            df_clean = df_clean.dropna(subset=['reviewid'])

        # 5. Remove duplicates (keeping first occurrence)
        initial_count = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['reviewid'], keep='first')
        logger.info(f"Removed {initial_count - len(df_clean)} duplicates")

        # 3. Essential column validation
        essential_cols = ['content', 'score', 'at']
        missing_essential = [col for col in essential_cols if col not in df_clean.columns]
        if missing_essential:
            logger.error(f"Missing essential columns: {missing_essential}")
            return pd.DataFrame()

        # 4. Handle missing values in each column
        # Content (review text)
        df_clean.loc[:, 'content'] = df_clean['content'].fillna('[No review text]')

        # Rating (score)
        df_clean.loc[:, 'score'] = (
            df_clean['score']
            .replace([np.inf, -np.inf], np.nan)  # Handle infinities
            .fillna(0)  # Fill NaN with 0
            .clip(1, 5)  # Ensure ratings are between 1-5
            .astype(int)  # Convert to integer
        )

        # Date (at)
        df_clean['at'] = pd.to_datetime(df_clean['at'], errors='coerce')
        df_clean['at'] = df_clean['at'].fillna(pd.Timestamp.now())

        # 5. Post-cleaning NaN check
        logger.info(f"\nPost-cleaning NaN check for {bank_name}:")
        logger.info(df_clean[essential_cols].isna().sum())

        # 6. Create processed DataFrame
        processed = pd.DataFrame({
            'review_id': df_clean['reviewid'],
            'review': df_clean['content'].str.strip(),
            'rating': df_clean['score'],
            'date': df_clean['at'].dt.strftime('%Y-%m-%d'),
            'bank': bank_name.upper(),
            'source': 'Google Play',

        })

        # 7. Final validation
        empty_reviews = processed['review'].str.len() <= 3
        if empty_reviews.any():
            logger.warning(f"Removing {empty_reviews.sum()} empty reviews")
            processed = processed[~empty_reviews]

        invalid_ratings = ~processed['rating'].between(1, 5)
        if invalid_ratings.any():
            logger.warning(f"Found {invalid_ratings.sum()} invalid ratings - keeping for analysis")

        logger.info(f"\nFinal data quality for {bank_name}:")
        logger.info(f"Total reviews: {len(processed)}")
        logger.info(f"Date range: {processed['date'].min()} to {processed['date'].max()}")
        logger.info(f"Rating distribution:\n{processed['rating'].value_counts().sort_index()}")

        return processed

    except Exception as e:
        logger.error(f"Preprocessing failed for {bank_name}: {str(e)}", exc_info=True)
        return pd.DataFrame()


def clean_text(text: str) -> str:
    """Clean review text"""
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    return text[:5000]  # Truncate very long reviews



def process_all_banks():
    """Process data for all known banks"""
    banks = ['cbe', 'boa', 'dashen']
    all_processed = []

    for bank in banks:
        # 1. Load raw data
        raw_df = load_bank_data(bank)
        if raw_df.empty:
            continue

        # 2. Preprocess
        processed_df = preprocess_reviews(raw_df, bank)
        if processed_df.empty:
            continue

        # 3. Save individual bank file
        save_processed_bank_data(processed_df, bank)
        all_processed.append(processed_df)

    # 4. Save combined file
    if all_processed:
        combined_df = pd.concat(all_processed, ignore_index=True)
        save_processed_bank_data(combined_df, "ALL_BANKS")
        return combined_df
    return pd.DataFrame()


