from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

analyzer = SentimentIntensityAnalyzer()


def classify_sentiment(text):
    """Classify sentiment using VADER and return compound score with label"""
    if pd.isna(text) or str(text).strip() == "":
        return {'compound': 0, 'sentiment': 'neutral'}

    scores = analyzer.polarity_scores(str(text))
    return {
        'compound': scores['compound'],
        'sentiment': 'positive' if scores['compound'] >= 0.05 else
        'negative' if scores['compound'] <= -0.05 else
        'neutral'
    }


def analyze_bank_reviews(df, bank_name):
    """Add sentiment columns to a bank's review DataFrame"""
    print(f"\nAnalyzing {bank_name} reviews...")

    # Apply sentiment analysis
    sentiment_results = df['review'].apply(lambda x: classify_sentiment(x))
    df = df.assign(
        sentiment_score=[x['compound'] for x in sentiment_results],
        sentiment=[x['sentiment'] for x in sentiment_results]
    )

    # Count sentiment distribution
    sentiment_counts = df['sentiment'].value_counts(normalize=True) * 100
    print(f"Sentiment distribution for {bank_name}:")
    print(sentiment_counts.to_string())

    return df