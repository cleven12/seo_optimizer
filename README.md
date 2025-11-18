# SEO Analyzer

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![GitHub stars](https://img.shields.io/github/stars/cleven12/seo_optimizer?style=social)](https://github.com/cleven12/seo_optimizer)

  **A powerful Python CLI tool that analyzes web content for SEO optimization based on focus keywords. Get actionable insights to improve your search rankings.**

> **For technical details and architecture**: See [NOTES.md](NOTES.md) <br/>**Full design docs**: [DESIGN_ARCHITECTURE_DOCS.md](public/DESIGN_ARCHITECTURE_DOCS.md)

---

## Features

-  **Keyword Analysis**: Analyze short-tail and long-tail keywords
-  **Google-like Matching**: Smart keyword detection with stemming and variations
-  **Individual & Cluster Scoring**: Detailed performance metrics
-  **Beautiful CLI Output**: Colored, formatted terminal interface
-  **JSON Export**: Optional report export for automation
-  **Fast Analysis**: Get results in seconds

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/cleven12/seo_optimizer.git
cd seo_optimizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Basic Usage

```bash
# Analyze a webpage
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
usage: main.py [-h] -u URL -k KEYWORDS [-o OUTPUT] [-v]

SEO Analyzer - Analyze web content for SEO optimization

options:
  -h, --help            show this help message and exit
  -u, --url URL         Target URL to analyze
  -k, --keywords KEYWORDS
                        Comma-separated focus keywords
  -o, --output OUTPUT   JSON output file path (optional)
  -v, --verbose         Show detailed analysis
```

## What It Analyzes

<table>
<tr>
<td width="50%">

### Keyword Performance
- Title tag optimization
- Meta description optimization
- Heading tags (H1-H6)
- Keyword density (1-3% optimal)
- First 100 words placement
- Content distribution

### Technical SEO
- Title length (50-60 chars)
- Meta description length (150-160 chars)
- Canonical tags
- Open Graph tags
- HTTP status

</td>
<td width="50%">

### Content Quality
- Word count
- Readability
- Content structure
- Keyword distribution

### Page Structure
- Heading hierarchy
- Image alt tags
- Paragraph structure
- List usage

### Link Analysis
- Internal links count
- External links count
- Anchor text optimization

</td>
</tr>
</table>

## Sample Output

```
🔍 Analyzing: https://example.com
Focus Keywords: "python tutorial", "learn python"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SEO ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 OVERALL SEO SCORE: 72/100

┌────────────────────────────────────────────────────────┐
│ 🎯 Keyword Cluster Performance: 75/100                 │
└────────────────────────────────────────────────────────┘

✅ "python tutorial" - 85/100
   ├─ Title: ✓ Found
   ├─ H1: ✓ Found
   └─ Density: 1.2% (optimal)

⚠️  "learn python" - 65/100
   ├─ Title: ✗ Not found
   └─ Density: 0.8% (low)
   💡 Add to title or first paragraph

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TOP RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🔴 Add "learn python" to title tag
2. 🟡 Increase internal linking (add 3-8 more links)
3. 🟢 Extend meta description to 150-160 characters
```

## Configuration

Customize analysis by editing `src/config.py`:

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

### Keyword Matching

The tool uses Google-like keyword matching:

- Case-insensitive
- Stemming (learn/learning/learned)
- Stop words removal (ignore "the", "a", "and")
- Partial matching
- Variations detection

>  **Deep dive**: See [NOTES.md](NOTES.md) for detailed architecture and technical implementation

## Requirements

- Python 3.8+
- requests
- beautifulsoup4
- nltk
- rich
- lxml

## Limitations

- Works with HTML/server-rendered sites only
- Does not render JavaScript (React, Vue, etc.)
- Requires internet connection for website which hosted online
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

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- 🐛 **Found a bug?** [Open an issue](https://github.com/cleven12/seo_optimizer/issues)
- 💡 **Have a feature request?** [Start a discussion](https://github.com/cleven12/seo_optimizer/discussions)
- ⭐ **Like this project?** Give it a star!

## Author

**Cleven**
- GitHub: [@cleven12](https://github.com/cleven12)
- X: [@cleven02](https://x.com/)

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful CLI
- NLP powered by [NLTK](https://www.nltk.org/)
- HTML parsing with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

<div align="center">

⭐ **If you find this tool useful, please consider giving it a star!** ⭐

[Report Bug](https://github.com/cleven12/seo_optimizer/issues) · [Request Feature](https://github.com/cleven12/seo_optimizer/issues) · [Documentation](NOTES.md)

</div>