# SEO Analyzer

A Python CLI tool that analyzes web content for SEO optimization based on focus keywords. Get actionable insights to improve your search rankings.

## Features

-  **Keyword Analysis**: Analyze short-tail and long-tail keywords
-  **Google-like Matching**: Smart keyword detection with stemming and variations
-  **Individual & Cluster Scoring**: Detailed performance metrics
-  **Beautiful CLI Output**: Colored, formatted terminal interface
-  **JSON Export**: Optional report export for automation
-  **Fast Analysis**: Get results in seconds

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/seo-analyzer.git
cd seo-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Quick Start

```bash
# Basic usage
python main.py --url "https://example.com" --keywords "python tutorial,learn python"

# With JSON export
python main.py --url "https://example.com" \
               --keywords "python tutorial,learn python,python for beginners" \
               --output report.json

# Verbose mode
python main.py --url "https://example.com" --keywords "seo tips" --verbose
```

## Usage

```bash
python main.py -u URL -k KEYWORDS [OPTIONS]

Required Arguments:
  -u, --url         Target URL to analyze
  -k, --keywords    Comma-separated focus keywords

Optional Arguments:
  -o, --output      JSON output file path
  -v, --verbose     Show detailed analysis
  -h, --help        Show help message
```

## What It Analyzes

###  Keyword Performance
- Title tag optimization
- Meta description optimization
- Heading tags (H1-H6)
- Keyword density (1-3% optimal)
- First 100 words placement
- Content distribution

###  Technical SEO
- Title length (50-60 chars)
- Meta description length (150-160 chars)
- Canonical tags
- Open Graph tags
- HTTP status

###  Content Quality
- Word count
- Readability
- Content structure
- Keyword distribution

###  Page Structure
- Heading hierarchy
- Image alt tags
- Paragraph structure
- List usage

###  Link Analysis
- Internal links count
- External links count
- Anchor text optimization

## Sample Output

```
  Analyzing: https://example.com
Focus Keywords: "python tutorial", "learn python"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SEO ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OVERALL SEO SCORE: 72/100

┌────────────────────────────────────────────────────────┐
│   Keyword Cluster Performance: 75/100                 │
└────────────────────────────────────────────────────────┘

 "python tutorial" - 85/100
   ├─ Title: ✓ Found
   ├─ H1: ✓ Found
   └─ Density: 1.2% (optimal)

  "learn python" - 65/100
   ├─ Title: ✗ Not found
   └─ Density: 0.8% (low)
    Add to title or first paragraph

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TOP RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🔴 Add "learn python" to title tag
2. 🟡 Increase internal linking (add 3-8 more links)
3. 🟢 Extend meta description to 150-160 characters
```

## JSON Output Format

```json
{
  "url": "https://example.com",
  "overall_score": 72,
  "keyword_analysis": {
    "cluster_score": 75,
    "individual_scores": [...]
  },
  "technical_seo": {...},
  "content_analysis": {...},
  "recommendations": [...]
}
```

## Requirements

- Python 3.8+
- requests
- beautifulsoup4
- nltk
- rich
- lxml

## Project Structure

```
seo_analyzer/
├── main.py                 # Entry point
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── core/                   # Core functionality
│   ├── orchestrator.py
│   ├── fetcher.py
│   ├── keyword_processor.py
│   └── scoring.py
├── analyzers/              # Analysis modules
│   ├── technical_seo.py
│   ├── content_analyzer.py
│   ├── structure_analyzer.py
│   └── link_analyzer.py
└── output/                 # Output formatters
    ├── cli_renderer.py
    └── json_exporter.py
```

## Configuration

Edit `config.py` to customize:

- Optimal keyword density range
- Title/meta length preferences
- Scoring weights
- Request timeout
- User agent

## How It Works

1. **Fetches** web content from provided URL
2. **Processes** keywords using NLP (stemming, stop words removal)
3. **Analyzes** content across multiple SEO factors
4. **Scores** each element with weighted algorithm
5. **Generates** actionable recommendations
6. **Outputs** colored CLI report and optional JSON

## Keyword Matching

The tool uses Google-like keyword matching:

- Case-insensitive
- Stemming (learn/learning/learned)
- Stop words removal (ignore "the", "a", "and")
- Partial matching
- Variations detection

## Limitations

- Works with HTML/server-rendered sites only
- Does not render JavaScript (React, Vue, etc.)
- Requires internet connection
- Does not check page speed metrics

## Roadmap

- [ ] Google Search Console integration
- [ ] Competitor comparison
- [ ] Semantic similarity (spaCy)
- [ ] Multi-language support
- [ ] Batch URL analysis
- [ ] Historical tracking
- [ ] Web dashboard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

Found a bug or have a feature request? Open an issue on GitHub.

## Author

- Cleven - [cleven12](https://github.com/cleven12)

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful CLI
- NLP powered by [NLTK](https://www.nltk.org/)
- HTML parsing with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

⭐ If you find this tool useful, please consider giving it a star on GitHub!