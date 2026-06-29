"""
CLI entry point for sentify.
"""
import argparse
from sentify.scraper import get_reviews
from sentify.analyzer import analyze_sentiment
from sentify.display import render_summary, show_progress, save_report

def main():
    """
    Main entry point for the CLI.
    """
    parser = argparse.ArgumentParser(
        prog="sentify",
        description="Analyze user sentiment for movies or books."
    )
    
    parser.add_argument("title", type=str, help="Movie or book title to analyze.")
    parser.add_argument("--type", choices=["movie", "book"], default="movie", help="Type of item ('movie' or 'book'). Default: movie.")
    parser.add_argument("--model", choices=["textblob", "distilbert"], default="textblob", help="NLP model to use. Default: textblob.")
    parser.add_argument("--limit", type=int, default=30, help="Max number of reviews to fetch. Default: 30.")
    parser.add_argument("--output", type=str, help="Optional: path to save a JSON report.")
    parser.add_argument("--verbose", action="store_true", help="Show per-review scores.")
    
    args = parser.parse_args()
    
    with show_progress(f"Fetching reviews for '{args.title}'...") as progress:
        progress.add_task("fetch", total=None)
        reviews = get_reviews(args.title, args.type, args.limit)
        
    if not reviews:
        print(f"No reviews found for {args.type} '{args.title}'.")
        return
        
    with show_progress(f"Analyzing sentiment using {args.model}...") as progress:
        progress.add_task("analyze", total=None)
        analysis = analyze_sentiment(reviews, args.model)
        
    render_summary(args.title, args.type, args.model, analysis, args.verbose, reviews)
    
    if args.output:
        save_report(args.output, args.title, args.type, args.model, analysis)

if __name__ == "__main__":
    main()
