# extractor.py
# Placeholder for hashtag and mention extraction logic 
from transformers import pipeline # type: ignore

# Load the sentiment analysis pipeline once at startup
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text: str):
    result = sentiment_pipeline(text)[0]
    # result['label'] will be 'POSITIVE' or 'NEGATIVE'
    return {"sentiment": result['label']} 