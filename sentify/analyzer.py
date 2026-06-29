"""
NLP Sentiment Logic module.
Supports TextBlob and DistilBERT.
"""
from typing import List, Dict, Any

def analyze_with_textblob(reviews: List[str]) -> Dict[str, Any]:
    """
    Analyze sentiment using TextBlob.
    Positive (>0.1), Negative (<-0.1), Neutral.
    """
    from textblob import TextBlob
    
    positive = 0
    negative = 0
    neutral = 0
    scores = []
    
    for review in reviews:
        score = TextBlob(review).sentiment.polarity
        scores.append(score)
        if score > 0.1:
            positive += 1
        elif score < -0.1:
            negative += 1
        else:
            neutral += 1
            
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "scores": scores,
        "avg_score": avg_score,
        "reviews_analyzed": len(reviews)
    }

def analyze_with_distilbert(reviews: List[str]) -> Dict[str, Any]:
    """
    Analyze sentiment using DistilBERT.
    Lazy-loads transformers pipeline.
    """
    try:
        from transformers import pipeline
    except ImportError:
        raise ImportError("Please install transformers and torch to use the distilbert model.")
        
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    positive = 0
    negative = 0
    neutral = 0
    scores = []
    
    if not reviews:
        return {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "scores": [],
            "avg_score": 0.0,
            "reviews_analyzed": 0
        }
        
    results = sentiment_pipeline(reviews, truncation=True, max_length=512)
    
    for res in results:
        label = res['label']
        score = res['score'] 
        
        mapped_score = score if label == 'POSITIVE' else -score
        scores.append(mapped_score)
        
        if label == 'POSITIVE':
            positive += 1
        elif label == 'NEGATIVE':
            negative += 1
        else:
            neutral += 1
            
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "scores": scores,
        "avg_score": avg_score,
        "reviews_analyzed": len(reviews)
    }

def analyze_sentiment(reviews: List[str], model: str = "textblob") -> Dict[str, Any]:
    """
    Analyze the sentiment of a list of reviews using the specified model.
    """
    if not reviews:
        return {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "scores": [],
            "avg_score": 0.0,
            "reviews_analyzed": 0
        }
        
    if model.lower() == "textblob":
        return analyze_with_textblob(reviews)
    elif model.lower() == "distilbert":
        return analyze_with_distilbert(reviews)
    else:
        raise ValueError(f"Unknown model: {model}. Supported models: textblob, distilbert.")
