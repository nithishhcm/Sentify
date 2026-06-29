"""
Display module for rendering rich terminal output.
"""
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import json
import sys

# Force UTF-8 encoding for standard output on Windows to support emojis and block characters
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()

def show_progress(task_desc: str):
    """
    Context manager for showing a progress spinner.
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    )

def render_summary(title: str, item_type: str, model: str, analysis: Dict[str, Any], verbose: bool = False, reviews: List[str] = None):
    """
    Render a rich panel summarizing the sentiment analysis results.
    """
    total = analysis["reviews_analyzed"]
    if total == 0:
        console.print(Panel("No reviews found to analyze.", title=f"{title} · {item_type.capitalize()} · {model.capitalize()}"))
        return

    pos = analysis["positive"]
    neg = analysis["negative"]
    neu = analysis["neutral"]

    pos_pct = int((pos / total) * 100)
    neg_pct = int((neg / total) * 100)
    neu_pct = int((neu / total) * 100)

    pos_bar = "█" * int((pos_pct / 100) * 16)
    neg_bar = "█" * int((neg_pct / 100) * 16)
    neu_bar = "█" * int((neu_pct / 100) * 16)

    content = f"Reviews analyzed: {total}\n"
    content += f"✅ [green]Positive[/green]   {pos:<3} ({pos_pct:>2}%)  [green]{pos_bar}[/green]\n"
    content += f"❌ [red]Negative[/red]    {neg:<3} ({neg_pct:>2}%)  [red]{neg_bar}[/red]\n"
    content += f"⬜ [gray]Neutral[/gray]     {neu:<3} ({neu_pct:>2}%)  [gray]{neu_bar}[/gray]\n"
    content += f"Avg sentiment score: {analysis['avg_score']:.2f}"
    
    panel_title = f"{title} · {item_type.capitalize()} · {model.capitalize()}"
    console.print(Panel(content, title=panel_title, expand=False))
    
    if verbose and reviews:
        console.print("\n[bold]Detailed Reviews:[/bold]")
        for review, score in zip(reviews, analysis["scores"]):
            color = "green" if score > 0.1 else ("red" if score < -0.1 else "gray")
            console.print(f"[{color}][{score:+.2f}][/{color}] {review[:100]}...")

def save_report(output_path: str, title: str, item_type: str, model: str, analysis: Dict[str, Any]):
    """
    Save the analysis to a JSON file.
    """
    report = {
        "title": title,
        "type": item_type,
        "model": model,
        "results": analysis
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    console.print(f"[bold green]Report saved to {output_path}[/bold green]")
