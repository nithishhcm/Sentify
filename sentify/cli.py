import argparse
import sys

from sentify.scraper import get_reviews as fetch_reviews
from sentify.analyzer import analyze_sentiment
from sentify.display import render_summary as show_results

def main():
    parser = argparse.ArgumentParser(description="Sentify - Sentiment Analyzer")
    parser.add_argument("title", help="Title of the movie or book")
    parser.add_argument("--type", choices=["movie", "book"], default="movie", help="Type of the item (movie/book)")
    parser.add_argument("--model", choices=["textblob", "distilbert"], default="textblob", help="Model to use for sentiment analysis")
    parser.add_argument("--limit", type=int, default=30, help="Maximum number of reviews to analyze")
    
    args = parser.parse_args()
    
    try:
        reviews = fetch_reviews(args.title, args.type, args.limit)
        analysis = analyze_sentiment(reviews, args.model)
        show_results(args.title, args.type, args.model, analysis)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
