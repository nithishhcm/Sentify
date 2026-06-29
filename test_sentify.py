import unittest
from sentify.analyzer import analyze_sentiment

class TestSentify(unittest.TestCase):
    def test_sentiment_analysis(self):
        # Mock data for testing
        mock_reviews = ["Great movie", "Terrible movie"]
        results = analyze_sentiment(mock_reviews, model="textblob")
        
        # Verify the analyzer returns results
        self.assertIn("positive", results)
        self.assertIn("negative", results)

if __name__ == "__main__":
    unittest.main()
