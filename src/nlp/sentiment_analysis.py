
import pandas as pd
import torch
from models import  load_sentiment_model

def predict_sentiment(review_df, model, tokenizer, neutral_threshold=0.2):
    text = review_df['review']
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1).squeeze().tolist()
    negative, positive = probs[0], probs[1]

    if abs(positive - negative) < neutral_threshold:
        return {"sentiment": "neutral", "scores": {"positive": positive, "negative": negative, "neutral": 1.0}}
    else:
        sentiment = "positive" if positive > negative else "negative"
        return {"sentiment": sentiment, "scores": {"positive": positive, "negative": negative, "neutral": 0.0}}

def analyze_reviews(input_csv):
    model, tokenizer = load_sentiment_model()
    df = pd.read_csv(input_csv)

    results = []
    for _, row in df.iterrows():
        result = predict_sentiment(row, model, tokenizer)
        results.append({
            "review_id": row["review_id"],
            "review": row["review"],
            **result
        })

    return  pd.DataFrame(results)