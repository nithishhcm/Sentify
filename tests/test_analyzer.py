"""
Unit tests for the analyzer module.
"""
import pytest
from sentify.analyzer import analyze_with_textblob, analyze_sentiment

def test_textblob_positive():
    """Test TextBlob scores a clearly positive string as Positive."""
    reviews = ["This is an absolutely wonderful and fantastic movie. I loved every second!"]
    result = analyze_with_textblob(reviews)
    assert result["positive"] == 1
    assert result["negative"] == 0
    assert result["neutral"] == 0
    assert result["avg_score"] > 0.1

def test_textblob_negative():
    """Test TextBlob scores a clearly negative string as Negative."""
    reviews = ["This is a terrible, awful, and boring movie. I hated it."]
    result = analyze_with_textblob(reviews)
    assert result["positive"] == 0
    assert result["negative"] == 1
    assert result["neutral"] == 0
    assert result["avg_score"] < -0.1

def test_aggregation_dict_keys():
    """Test the aggregation dict has the required keys."""
    reviews = ["It was okay."]
    result = analyze_sentiment(reviews, model="textblob")
    expected_keys = {"positive", "negative", "neutral", "scores", "avg_score", "reviews_analyzed"}
    assert set(result.keys()) == expected_keys

def test_empty_review_list():
    """Test that an empty review list returns zeros without crashing."""
    result = analyze_sentiment([], model="textblob")
    assert result["positive"] == 0
    assert result["negative"] == 0
    assert result["neutral"] == 0
    assert result["scores"] == []
    assert result["avg_score"] == 0.0
    assert result["reviews_analyzed"] == 0
