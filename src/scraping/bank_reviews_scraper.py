from google_play_scraper import app, reviews_all, Sort
import pandas as pd
from time import sleep
from scripts import  save_scraped_data_to_csv
# ----- Bank App Package Names (Verified) -----
BANKS = {
    "cbe": "com.combanketh.mobilebanking",        # Commercial Bank of Ethiopia
    "boa": "com.boa.boaMobileBanking",            # Bank of Abyssinia
    "dashen": "com.dashen.dashensuperapp"         # Dashen Bank
}



def scrape_bank_reviews():
    """
    Scrape reviews for Ethiopian bank apps and save to CSV.
    """
    all_reviews = []

    for bank_name, app_id in BANKS.items():
        print(f"\n🔍 Scraping {bank_name.upper()} ({app_id})...")

        try:
            # Confirm the app exists
            app_info = app(app_id, lang='en', country='us')
            print(f"📱 App found: {app_info['title']} ({app_info['score']} stars)")

            # Fetch reviews (Amharic not supported directly, so we use English in Ethiopia)
            reviews = reviews_all(
                app_id,
                lang='en',
                country='et',
                sort=Sort.NEWEST,
                count=200,
                filter_score_with=None,
                sleep_milliseconds=2000
            )

            print(f"Fetched {len(reviews)} reviews")
            if reviews:
                for r in reviews:
                    r['bank'] = bank_name.upper()
                all_reviews.extend(reviews)
                print(f"Sample: {reviews[0]['content'][:50]}...")

            sleep(2)  # Delay to prevent rate limiting

        except Exception as e:
            print(f"Error scraping {bank_name.upper()}: {str(e)}")
            continue

    # Process and save results
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        desired_columns = [
            'bank', 'userName', 'score', 'at', 'content',
            'reviewId', 'thumbsUpCount', 'replyContent', 'repliedAt'
        ]
        for col in desired_columns:
            if col not in df.columns:
                df[col] = None

        # Save for each bank separately
        for bank in BANKS.keys():
            bank_df = df[df['bank'] == bank.upper()]
            save_scraped_data_to_csv(bank_df, bank)
    return  all_reviews




