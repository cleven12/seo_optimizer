# SEO Analyzer Tool

## Overview
A powerful Python CLI tool that analyzes web content for SEO optimization based on user-provided focus keywords. The tool provides comprehensive SEO analysis including keyword performance, technical SEO, content quality, structure, and links.

## Recent Changes
- **2025-11-24**: Initial setup on Local Dev Env
- **2025-11-24**: Integrated AI-powered recommendations using Google Gemini (free) and OpenAI
- **2025-11-24**: Updated to support both Gemini and OpenAI for flexibility
- **2025-11-24**: Configured for keyword-focused SEO analysis
  *********************
 - **YEAR-MON-DATE**: Short Description

## Project Architecture

### Technology Stack
- **Language**: Python 3.11
- **HTTP Client**: requests
- **HTML Parser**: BeautifulSoup4 + lxml
- **NLP**: NLTK (tokenization, stemming, stopwords)
- **CLI Framework**: Rich (colored terminal output)
- **AI Integration**: Google Gemini (free tier) + OpenAI (optional)

### Core Features
1. **Keyword Analysis**: Analyzes short-tail and long-tail keywords with Google-like matching
2. **Technical SEO**: Title tags, meta descriptions, canonical tags, Open Graph
3. **Content Analysis**: Keyword density, placement, distribution, word count
4. **Structure Analysis**: Heading hierarchy, H1 usage, image alt tags
5. **Link Analysis**: Internal/external link counts and quality
6. **AI-Powered Recommendations**: Optional AI analysis using Gemini or OpenAI

### Project Structure
```
seo_analyzer/
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── src/
│   ├── app.py                   # CLI interface
│   ├── config.py                # Configuration constants
│   ├── core/                    # Core functionality
│   │   ├── orchestrator.py      # Main controller
│   │   ├── fetcher.py           # Web content fetching
│   │   ├── keyword_processor.py # NLP keyword processing
│   │   └── scoring.py           # Scoring engine
│   ├── analyzers/               # Analysis modules
│   │   ├── base_analyzer.py     # Base class
│   │   ├── technical_seo.py     # Technical SEO checks
│   │   ├── content_analyzer.py  # Content analysis
│   │   ├── structure_analyzer.py# Structure checks
│   │   ├── link_analyzer.py     # Link analysis
│   │   └── ai_analyzer.py       # AI-powered recommendations
│   ├── output/                  # Output formatters
│   │   ├── cli_renderer.py      # Rich CLI output
│   │   └── json_exporter.py     # JSON export
│   └── utils/                   # Utilities
│       ├── text_utils.py        # Text processing helpers
│       └── validation.py        # Input validation
├── public/
│   └── DESIGN_ARCHITECTURE_DOCS.md  # Detailed architecture docs
└── README.md                    # User documentation
```

## User Preferences
- Simple, everyday language preferred
- Focus on actionable SEO recommendations
- Keyword-focused analysis for defined keywords only

## How to Use

### Basic Usage
```bash
# Analyze a webpage with keywords
python main.py --url "https://example.com" --keywords "seo,optimization,website"

# With verbose output
python main.py --url "https://example.com" --keywords "seo,optimization" --verbose

# With AI-powered recommendations (requires GEMINI_API_KEY or OPENAI_API_KEY)
python main.py --url "https://example.com" --keywords "seo,optimization" --ai

# Export to JSON
python main.py --url "https://example.com" --keywords "seo,optimization" --output report.json
```

### Command Line Arguments
- `-u, --url`: Target URL to analyze (required)
- `-k, --keywords`: Comma-separated focus keywords (required)
- `-o, --output`: JSON output file path (optional)
- `-v, --verbose`: Show detailed analysis (optional)
- `--ai`: Enable AI-powered SEO recommendations (optional, requires API key)

## AI Integration

### Using Google Gemini (FREE - Recommended)
1. Get a FREE API key from https://aistudio.google.com/apikey
2. Add it to Local Dev Env Secrets as `GEMINI_API_KEY`
3. Run with `--ai` flag to get AI-powered recommendations
4. Uses `gemini-2.5-flash` model (fast and free)

### Using OpenAI (Paid)
1. Get an API key from https://platform.openai.com/api-keys
2. Add it to Local Dev Env Secrets as `OPENAI_API_KEY`
3. Run with `--ai` flag to get AI-powered recommendations
4. Uses `gpt-5` model (requires credits)

### AI Features
When enabled with `--ai` flag, the tool provides:
- 5 specific, actionable SEO recommendations focused on your keywords
- AI-optimized title tag (50-60 characters)
- AI-optimized meta description (150-160 characters)
- Content quality analysis (readability, engagement, keyword targeting)
- **Grammar & Readability Analysis (SEO-Safe)**:
  - Grammar score (1-10)
  - Grammar issues detection
  - Grammar fixes that preserve all SEO keywords
  - Readability improvements without keyword changes
  - Improved title and meta description with keywords intact

## Keyword Matching Algorithm
The tool uses intelligent keyword matching similar to Google:
1. **Normalization**: Lowercase conversion
2. **Tokenization**: Word splitting
3. **Stemming**: Porter Stemmer for root forms (e.g., "learning" → "learn")
4. **Stop Words Removal**: Ignores common words ("the", "a", "and", etc.)
5. **Variation Detection**: Finds keyword variations and related terms

## Scoring System
- **Overall SEO Score**: 0-100
  - Keyword Analysis: 40%
  - Technical SEO: 20%
  - Content Quality: 20%
  - Structure: 10%
  - Links: 10%

## Dependencies
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- nltk>=3.8.0
- rich>=13.7.0
- lxml>=4.9.0
- google-genai>=1.0.0 (for Gemini AI)
- openai>=2.0.0 (for OpenAI)

## Environment Variables
- `GEMINI_API_KEY`: Google Gemini API key (optional, for AI features)
- `OPENAI_API_KEY`: OpenAI API key (optional, for AI features)

## Notes
- NLTK data (punkt, stopwords, punkt_tab) is automatically downloaded on first run
- The tool works with static HTML pages only (no JavaScript rendering)
- AI recommendations are keyword-focused and tailored to your specific keywords
- Gemini is recommended for free, powerful AI analysis
