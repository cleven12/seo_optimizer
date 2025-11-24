# SEO Analyzer - AI-Powered Content Optimization Tool

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/cleven12/seo_optimizer/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![GitHub stars](https://img.shields.io/github/stars/cleven12/seo_optimizer?style=social)](https://github.com/cleven12/seo_optimizer)
[![Twitter Follow](https://img.shields.io/twitter/follow/cleven02?style=social)](https://twitter.com/cleven02)

**A powerful Python CLI tool that combines traditional SEO analysis with cutting-edge AI to optimize your web content for search engines. Get actionable insights, AI-powered recommendations, and grammar-safe content improvements.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [AI Features](#-ai-powered-features) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## Table of Contents

- [Overview](#-overview)
- [Key Features](#-features)
- [AI-Powered Features](#-ai-powered-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [What It Analyzes](#-what-it-analyzes)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [Sample Output](#-sample-output)
- [Documentation](#-documentation)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## Overview

**SEO Analyzer** is an advanced Python CLI tool designed for SEO professionals, content creators, and digital marketers who want to optimize their web content for search engines. It combines traditional SEO analysis with state-of-the-art AI models (Google Gemini & OpenAI GPT-5) to provide intelligent recommendations that boost your search rankings.

### Why Choose SEO Analyzer?

- **Keyword-Focused Analysis**: Target specific keywords with Google-like matching algorithms
- **AI-Powered Insights**: Get intelligent recommendations from cutting-edge AI models
- **Grammar-Safe Optimization**: Fix grammar issues without affecting SEO keywords
- **Comprehensive Scoring**: Evaluate 40+ SEO factors with weighted scoring
- **Beautiful CLI Output**: Rich terminal interface with colors and progress indicators
- **Fast & Efficient**: Get complete analysis in seconds
- **Export-Ready**: JSON output for automation and integration

---

## Features

### Core SEO Analysis

| Feature | Description |
|---------|-------------|
| **Keyword Analysis** | Analyzes short-tail and long-tail keywords with intelligent matching |
| **Google-like Matching** | Smart keyword detection using stemming, variations, and stopword removal |
| **Individual & Cluster Scoring** | Detailed performance metrics for each keyword and keyword groups |
| **Technical SEO** | Title tags, meta descriptions, canonical tags, Open Graph validation |
| **Content Quality** | Keyword density, placement, distribution, and word count analysis |
| **Structure Analysis** | Heading hierarchy (H1-H6), image alt tags, and content organization |
| **Link Analysis** | Internal and external link counts with quality assessment |

### Advanced Features

- **NLP-Powered Matching**: NLTK-based tokenization, stemming, and semantic analysis
- **Weighted Scoring System**: Configurable weights for different SEO factors
- **Beautiful CLI**: Rich terminal output with colors, tables, and panels
- **JSON Export**: Machine-readable reports for automation
- **Verbose Mode**: Detailed breakdowns for in-depth analysis
- **Fast Analysis**: Complete reports in under 10 seconds

---

## AI-Powered Features

### NEW! Intelligent Content Optimization

Leverage the power of Google Gemini (FREE) or OpenAI GPT-5 for advanced SEO insights:

#### 1. **AI-Powered Recommendations**
- Get 5 specific, actionable SEO recommendations
- Keyword-focused suggestions tailored to your target keywords
- Based on current performance scores and content analysis

#### 2. **AI-Optimized Meta Tags**
- **Title Tag Generation**: SEO-optimized titles (50-60 characters)
- **Meta Description Generation**: Compelling descriptions (150-160 characters)
- Keyword-integrated, click-worthy, and search-engine friendly

#### 3. **Content Quality Analysis**
Evaluate your content across multiple dimensions:
- **Readability Score** (1-10): How easy is your content to read?
- **Engagement Potential** (1-10): Will readers stay on your page?
- **Keyword Stuffing Risk** (1-10): Are you over-optimizing?
- **Content Value** (1-10): Does your content provide real value?
- **Keyword Targeting** (1-10): How well do you target your keywords?

#### 4. **Grammar & Readability (SEO-Safe)** 
The most unique feature - improve grammar WITHOUT affecting SEO:
- **Grammar Score**: Identify grammar issues (1-10 scale)
- **SEO-Preserved Fixes**: Grammar corrections that keep ALL keywords intact
- **Improved Title & Meta**: Better versions with keywords preserved
- **Readability Tips**: Enhance readability without changing keyword density
- **Grammar Suggestions**: Top 3 fixes that won't hurt your SEO

> **Why This Matters**: Traditional grammar checkers often remove or change keywords, hurting your SEO. Our AI understands SEO and fixes grammar while preserving keyword density and placement.

### Supported AI Models

| Provider | Model | Cost | Recommended For |
|----------|-------|------|-----------------|
| **Google Gemini** | `gemini-2.5-flash` | **FREE** | Everyone (default) |
| **OpenAI** | `gpt-5` | Paid | Advanced users |

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for webpage analysis)

### Step 1: Clone the Repository

```bash
git clone https://github.com/cleven12/seo_optimizer.git
cd seo_optimizer
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

### Step 5: Set Up AI Features (Optional)

For AI-powered recommendations, you need an API key:

#### Option 1: Google Gemini (FREE - Recommended)

1. Get a FREE API key: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Set environment variable:

```bash
# On macOS/Linux:
export GEMINI_API_KEY="your-api-key-here"

# On Windows:
set GEMINI_API_KEY=your-api-key-here

# Or add to .env file:
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

#### Option 2: OpenAI (Paid)

1. Get API key: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Set environment variable:

```bash
# On macOS/Linux:
export OPENAI_API_KEY="your-api-key-here"

# On Windows:
set OPENAI_API_KEY=your-api-key-here
```

---

##  Quick Start

### Basic Analysis

```bash
python main.py --url "https://example.com" --keywords "seo,optimization,search engine"
```

### With AI Recommendations

```bash
python main.py --url "https://example.com" --keywords "seo,optimization" --ai
```

### Export to JSON

```bash
python main.py --url "https://example.com" --keywords "python tutorial" --output report.json --ai
```

### Verbose Mode

```bash
python main.py --url "https://example.com" --keywords "web development" --verbose --ai
```

---

## Usage Examples

### Example 1: Blog Post Optimization

```bash
python main.py \
  --url "https://myblog.com/learn-python" \
  --keywords "learn python,python tutorial,python for beginners" \
  --ai \
  --verbose
```

### Example 2: E-commerce Product Page

```bash
python main.py \
  --url "https://shop.com/product/123" \
  --keywords "buy laptop,gaming laptop,best laptop 2025" \
  --output product-seo-report.json \
  --ai
```

### Example 3: Landing Page Analysis

```bash
python main.py \
  --url "https://saas.com/landing" \
  --keywords "project management software,team collaboration tool" \
  --ai
```

### Example 4: Batch Analysis (Shell Script)

```bash
#!/bin/bash
URLS=(
  "https://example.com/page1"
  "https://example.com/page2"
  "https://example.com/page3"
)

for URL in "${URLS[@]}"; do
  python main.py --url "$URL" --keywords "target keyword" --output "report-$(basename $URL).json" --ai
done
```

---

## What It Analyzes

<table>
<tr>
<td width="50%" valign="top">

### Keyword Performance
- Title tag optimization
- Meta description optimization  
- Heading tags (H1-H6) usage
- Keyword density (1-3% optimal)
- First 100 words placement
- Content distribution analysis
- Keyword variations detection

### Technical SEO
- Title length (50-60 chars)
- Meta description (150-160 chars)
- Canonical tags
- Open Graph tags (social sharing)
- HTTP status validation
- Mobile-friendly tags

### Content Quality
- Total word count
- Readability level (AI)
- Content structure
- Keyword distribution
- Engagement potential (AI)
- Content value score (AI)

</td>
<td width="50%" valign="top">

### Page Structure
- Heading hierarchy validation
- H1 count and placement
- Image alt tag coverage
- Paragraph structure
- List usage analysis
- Content organization

### Link Analysis
- Internal links count
- External links count
- Anchor text optimization
- Link quality assessment
- Recommended link density

### AI Insights (with --ai)
- 5 actionable recommendations
- AI-optimized title tag
- AI-optimized meta description
- Grammar & readability (SEO-safe)
- Content quality analysis
- Keyword targeting score

</td>
</tr>
</table>

---

## Architecture

### Modular Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI Interface Layer                     │
│                    (Rich Terminal Output)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Orchestrator/Controller                    │
│              (Coordinates Analysis Pipeline)                 │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │ Content │    │ Keyword  │    │  NLP     │
    │ Fetcher │    │Processor │    │Processing│
    └────┬────┘    └────┬─────┘    └────┬─────┘
         │              │               │
         └──────────────┼───────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
    ┌────────┐    ┌─────────┐    ┌────────┐
    │Technical│    │ Content │    │Structure│
    │   SEO   │    │Analyzer │    │Analyzer│
    └────┬───┘    └────┬────┘    └────┬───┘
         │             │              │
         └─────────────┼──────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   AI Analyzer   │
              │ (Gemini/OpenAI) │
              └────────┬─────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Scoring Engine  │
              └────────┬─────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Output Layer   │
              │  (CLI / JSON)   │
              └─────────────────┘
```

### Key Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **CLI Interface** | Rich, argparse | User input and formatted output |
| **Content Fetcher** | requests, BeautifulSoup4 | HTML parsing and data extraction |
| **Keyword Processor** | NLTK | NLP operations (stemming, tokenization) |
| **Analysis Modules** | Plugin architecture | Modular SEO analyzers |
| **AI Analyzer** | Google Gemini / OpenAI | AI-powered recommendations |
| **Scoring Engine** | Custom algorithm | Weighted scoring system |
| **Output Layer** | Rich / JSON | CLI rendering and export |

---

## ⚙️ Configuration

Customize analysis behavior by editing `src/config.py`:

```python
# Keyword Density
OPTIMAL_KEYWORD_DENSITY_MIN = 1.0  # 1%
OPTIMAL_KEYWORD_DENSITY_MAX = 3.0  # 3%

# Title & Meta
OPTIMAL_TITLE_LENGTH_MIN = 50
OPTIMAL_TITLE_LENGTH_MAX = 60
OPTIMAL_META_DESC_LENGTH_MIN = 150
OPTIMAL_META_DESC_LENGTH_MAX = 160

# Content
MIN_WORD_COUNT = 300

# Links
RECOMMENDED_INTERNAL_LINKS_MIN = 3
RECOMMENDED_INTERNAL_LINKS_MAX = 10

# Scoring Weights
KEYWORD_ANALYSIS_WEIGHT = 0.40  # 40%
TECHNICAL_SEO_WEIGHT = 0.20     # 20%
CONTENT_QUALITY_WEIGHT = 0.20   # 20%
STRUCTURE_WEIGHT = 0.10         # 10%
LINK_ANALYSIS_WEIGHT = 0.10     # 10%
```

---

## Sample Output

```
🔍 Analyzing: https://example.com
Focus Keywords: "python tutorial", "learn python", "python for beginners"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SEO ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 OVERALL SEO SCORE: 78/100

╔════════════════════════════════════════════════════╗
║ 🎯 Keyword Cluster Performance: 75/100             ║
╚════════════════════════════════════════════════════╝

📈 Individual Keyword Scores:

✅ "python tutorial" - 85/100
   ├─ Title: ✓ Yes
   ├─ Meta: ✓ Yes
   ├─ H1: ✓ Yes
   ├─ Density: 2.1% (optimal)
   └─ First 100 words: ✓ Yes

⚠️  "learn python" - 70/100
   ├─ Title: ✗ No
   ├─ Meta: ✓ Yes
   ├─ H1: ✓ Yes
   ├─ Density: 1.5%
   └─ First 100 words: ✓ Yes
      💡 Add "learn python" to title tag

✅ "python for beginners" - 80/100
   ├─ Title: ✓ Yes
   ├─ Meta: ✓ Yes
   ├─ H1: ✗ No
   ├─ Density: 1.8%
   └─ First 100 words: ✓ Yes
      💡 Include "python for beginners" in H1 heading

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Technical SEO: 85/100
✅ Content Analysis: 82/100
✅ Structure: 75/100
⚠️  Links: 65/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI-POWERED SEO INSIGHTS (Gemini 2.5 Flash)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 AI-Optimized Title:
   Learn Python: Complete Tutorial for Beginners in 2025

📄 AI-Optimized Meta Description:
   Master Python programming with our comprehensive tutorial designed for beginners. Learn syntax, projects, and best practices. Start coding today!

📊 Content Quality Analysis:
   ├─ Readability: 8/10
   ├─ Engagement: 9/10
   └─ Content Value: 8/10

✍️  Grammar & Readability (SEO-Safe):
   ├─ Grammar Score: 7/10
   ├─ Issues Found: 5
   └─ SEO Keywords Preserved: ✓ Yes

   Improved Title (Keywords Preserved):
   Learn Python: The Complete Tutorial for Beginners

   Grammar Fixes:
   • Fix run-on sentence in paragraph 3 (keywords preserved)
   • Add comma after introductory phrase
   • Correct subject-verb agreement in section 2

   Readability Tips:
   • Break long paragraphs into shorter ones
   • Use more transition words between sections

💡 AI Recommendations:
   1. Add "learn python" to the title tag for better keyword coverage
   2. Include more internal links to related Python topics (current: 2, recommended: 5-8)
   3. Extend meta description to 155-160 characters for optimal visibility
   4. Add "python for beginners" to the H1 heading
   5. Increase keyword density for "learn python" to 1.5-2% for better targeting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TOP RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🔴 Add "learn python" to title tag
2. 🔴 Increase internal linking (add 3 more links)
3. 🟡 Extend meta description to 155-160 characters
4. 🟢 Include "python for beginners" in H1 heading

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Analysis complete! Export with --output to save as JSON
```

---

## 📚 Documentation

### Full Documentation

- **[NOTES.md](NOTES.md)**: Complete technical documentation and architecture details
- **[DESIGN_ARCHITECTURE_DOCS.md](public/DESIGN_ARCHITECTURE_DOCS.md)**: In-depth design documentation
- **[API Reference](docs/api-reference.md)**: Detailed API documentation (coming soon)

### Command Line Reference

```bash
usage: main.py [-h] -u URL -k KEYWORDS [-o OUTPUT] [-v] [--ai]

SEO Analyzer - AI-Powered Content Optimization Tool

required arguments:
  -u, --url URL         Target URL to analyze
  -k, --keywords KEYWORDS
                        Comma-separated focus keywords

optional arguments:
  -h, --help            Show this help message and exit
  -o, --output OUTPUT   JSON output file path
  -v, --verbose         Show detailed analysis
  --ai                  Enable AI-powered recommendations (requires API key)
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | For AI features |
| `OPENAI_API_KEY` | OpenAI API key | Alternative to Gemini |

---

## Roadmap

### Completed
- [x] Core SEO analysis engine
- [x] Keyword matching with NLP
- [x] Beautiful CLI output
- [x] JSON export functionality
- [x] AI-powered recommendations (Gemini & OpenAI)
- [x] Grammar analysis (SEO-safe)
- [x] Content quality evaluation

### In Progress
- [ ] Google Search Console integration
- [ ] Competitor comparison analysis
- [ ] Historical tracking dashboard

### Planned
- [ ] Semantic similarity with spaCy
- [ ] Multi-language support (ES, FR, DE, IT)
- [ ] Batch URL analysis
- [ ] Web dashboard interface
- [ ] WordPress plugin
- [ ] Browser extension
- [ ] REST API endpoint
- [ ] Slack/Discord bot integration
- [ ] Page speed metrics
- [ ] JavaScript rendering support
- [ ] Image SEO analysis
- [ ] Schema markup validation
- [ ] Backlink analysis
- [ ] SERP position tracking

---

## Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

### How to Contribute

1. **Fork the Project**
   ```bash
   git clone https://github.com/cleven12/seo_optimizer.git
   ```

2. **Create your Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Commit your Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

4. **Push to the Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```

5. **Open a Pull Request**

### Development Setup

```bash
# Clone and setup
git clone https://github.com/cleven12/seo_optimizer.git
cd seo_optimizer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For testing

# Run tests
pytest

# Code formatting
black src/
flake8 src/
```

### Contribution Guidelines

- Write clear, commented code
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Keep commits focused and atomic

---

## License

Distributed under the MIT License. See `LICENSE` file for more information.

```
MIT License

Copyright (c) 2025 Cleven

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## Support

### Get Help

- **Found a bug?** [Open an issue](https://github.com/cleven12/seo_optimizer/issues/new?template=bug_report.md)
- **Have a feature request?** [Open an issue](https://github.com/cleven12/seo_optimizer/issues/new?template=feature_request.md)
- **Have a question?** [Start a discussion](https://github.com/cleven12/seo_optimizer/discussions)
- **Need direct support?** Email: support@example.com

### Community

- [Join our Discord](https://discord.gg/seo-optimizer)
- [Follow on Twitter](https://twitter.com/cleven02)
- [YouTube Tutorials](https://youtube.com/@cleven)

---

## Show Your Support

If you find this project useful, please consider:

- **Starring the repository**
- **Sharing on social media**
- **Telling your friends**
- **Buying me a coffee**: [https://buymeacoffee.com/cleven](https://buymeacoffee.com/cleven)

---

## Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/cleven12/seo_optimizer)
![GitHub contributors](https://img.shields.io/github/contributors/cleven12/seo_optimizer)
![GitHub issues](https://img.shields.io/github/issues/cleven12/seo_optimizer)
![GitHub pull requests](https://img.shields.io/github/issues-pr/cleven12/seo_optimizer)
![GitHub last commit](https://img.shields.io/github/last-commit/cleven12/seo_optimizer)

---

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful CLI output
- NLP powered by [NLTK](https://www.nltk.org/)
- HTML parsing with [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- AI features by [Google Gemini](https://ai.google.dev/) and [OpenAI](https://openai.com/)
- Inspired by industry-leading SEO tools

---

## Author

**Cleven**

-  GitHub: [@cleven12](https://github.com/cleven12)
-  Twitter: [@cleven02](https://twitter.com/cleven02)
-  LinkedIn: [Cleven12](https://tz.linkedin.com/in/cleven-godson-0140b1355)
- Website: [Cleven12.dev](https://cleven.pythonanywhere.com)

---

<div align="center">

**Made with ❤️ by [Cleven](https://github.com/cleven12)**

⭐ **If you find this project useful, please give it a star!** ⭐

[⬆ Back to Top](#-seo-analyzer---ai-powered-content-optimization-tool)

</div>