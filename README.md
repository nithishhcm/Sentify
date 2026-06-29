[![Python application](https://github.com/nithishhcm/Sentify/actions/workflows/python-app.yml/badge.svg)](https://github.com/nithishhcm/Sentify/actions/workflows/python-app.yml)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# Sentify

A production-quality CLI tool that analyzes user sentiment for movies or books.

## Installation

To install this tool locally, clone the repository and run:

```bash
pip install -e .
```

This will make the `sentify` command available globally in your environment.

## Usage

You can run `sentify` to fetch and analyze reviews. 

```bash
# Analyze a movie using the default TextBlob model
sentify "Dune" --type movie --limit 50

# Analyze a book using DistilBERT model
sentify "Project Hail Mary" --type book --model distilbert --limit 20

# View all options
sentify --help
```

### Example Output

```text
╭─ Dune · Movie · TextBlob ──────────────────────╮
│  Reviews analyzed: 47                          │
│  ✅ Positive   32  (68%)  ████████████████     │
│  ❌ Negative    8  (17%)  ████                 │
│  ⬜ Neutral     7  (15%)  ███                  │
│  Avg sentiment score: 0.42                     │
╰────────────────────────────────────────────────╯
```

## Models and Tradeoffs

Sentify supports two sentiment analysis backends:

1. **TextBlob** (`--model textblob`):
   - *Pros*: Extremely fast, lightweight, and requires no large model downloads. Good for basic rule-based lexical analysis.
   - *Cons*: Struggles with sarcasm, complex sentence structures, and context.

2. **DistilBERT** (`--model distilbert`):
   - *Pros*: Uses a fine-tuned transformer model (`distilbert-base-uncased-finetuned-sst-2-english`) which understands context, nuances, and performs significantly better on real-world reviews.
   - *Cons*: Slower to run. Requires downloading the model weights (~260MB) on the first run, and depends on larger packages (`torch` and `transformers`).
"# Sentify" 
"# Sentify" 
