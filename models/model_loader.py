from transformers import AutoTokenizer, AutoModelForSequenceClassification




def load_sentiment_model():
    """Returns model and tokenizer for sentiment analysis"""
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    try:
        # Try loading from local models folder first
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except:
        # Fallback to downloading from HuggingFace
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Save locally for future use
        model.save_pretrained(f"./models/{model_name}")
        tokenizer.save_pretrained(f"./models/{model_name}")

    return model, tokenizer

