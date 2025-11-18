# SEO Analyzer Tool

## Overview

A Python CLI application that analyzes web pages for SEO optimization based on user-provided focus keywords. The tool fetches web content, performs comprehensive SEO analysis across multiple dimensions (technical, content, structure, links), and provides actionable recommendations with scoring metrics. It uses intelligent keyword matching with stemming and semantic analysis to provide Google-like keyword detection.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Architecture Pattern
**Modular Pipeline Architecture** - The application follows a pipeline pattern where data flows through distinct stages: fetching → processing → analysis → scoring → output. Each stage is isolated and communicates through well-defined data structures.

### Core Components

#### 1. CLI Interface Layer
- **Technology**: Rich library for colored terminal output, argparse for command parsing
- **Purpose**: Handles user input validation and provides formatted console output
- **Key Files**: `src/main.py`, `src/output/cli_renderer.py`
- **Design Decision**: Using Rich library for beautiful CLI output instead of plain text to improve user experience and readability of complex analysis results

#### 2. Orchestrator/Controller
- **Pattern**: Orchestration pattern to coordinate the analysis pipeline
- **File**: `src/core/orchestrator.py`
- **Responsibilities**: 
  - Coordinates the execution flow between fetcher, processors, and analyzers
  - Aggregates results from all analysis modules
  - Generates final report structure
- **Design Decision**: Centralized orchestration ensures predictable execution order and makes it easy to add/remove analysis modules

#### 3. Content Fetcher
- **File**: `src/core/fetcher.py`
- **Technology**: Requests library for HTTP, BeautifulSoup4 for HTML parsing
- **Purpose**: Fetches web pages and extracts structured data (title, meta tags, headings, links, images, body text)
- **Design Decision**: Using BeautifulSoup instead of regex for robust HTML parsing that handles malformed HTML gracefully

#### 4. Keyword Processor
- **File**: `src/core/keyword_processor.py`
- **Technology**: NLTK for NLP operations (tokenization, stemming, stopword removal)
- **Purpose**: Generates keyword variations using stemming and stopword removal for intelligent matching
- **Design Decision**: Multi-variation matching (exact, stemmed, stopwords-removed) provides Google-like keyword detection that catches semantic variations

#### 5. Analysis Modules (Plugin-like Architecture)
Each analyzer inherits from `BaseAnalyzer` and implements specific SEO checks:

- **TechnicalSEOAnalyzer**: Title tags, meta descriptions, canonical tags, Open Graph tags
- **ContentAnalyzer**: Keyword density, placement, distribution, word count
- **StructureAnalyzer**: Heading hierarchy, H1 usage, image alt tags
- **LinkAnalyzer**: Internal/external link counts and quality

**Design Decision**: Abstract base class pattern allows easy addition of new analysis modules without modifying the orchestrator. Each analyzer is independent and testable.

#### 6. Scoring Engine
- **File**: `src/core/scoring.py`
- **Purpose**: Calculates weighted scores for individual metrics and overall SEO score
- **Configuration**: `src/config.py` contains all weights and thresholds
- **Design Decision**: Centralized scoring with configurable weights allows easy tuning of importance across different SEO factors

#### 7. Output Layer
- **CLI Renderer**: Rich-formatted console output with colors, tables, and progress indicators
- **JSON Exporter**: Optional structured JSON output for automation/integration
- **Design Decision**: Dual output format supports both human interaction (CLI) and machine integration (JSON)

### Data Flow

```
User Input (URL + Keywords)
    ↓
Content Fetcher (HTML → Structured WebContent)
    ↓
Keyword Processor (Keywords → Variations with stemming)
    ↓
Parallel Analysis Modules (4 analyzers process independently)
    ↓
Scoring Engine (Weighted aggregation)
    ↓
Report Generation (AnalysisReport dataclass)
    ↓
Output (CLI display and/or JSON export)
```

### Configuration Management
- **File**: `src/config.py`
- **Pattern**: Centralized configuration module
- **Contains**: 
  - SEO thresholds (optimal title length, keyword density ranges)
  - Scoring weights for different modules
  - HTTP request settings
- **Design Decision**: Single source of truth for all configurable values makes tuning and testing easier

### Text Processing Pipeline
- **NLTK Integration**: Downloads required corpora on first run
- **Stemming**: Porter Stemmer for reducing words to root forms
- **Tokenization**: Regex-based word extraction
- **Design Decision**: NLTK provides battle-tested NLP operations; lazy downloading of data reduces initial package size

## External Dependencies

### Third-Party Libraries

1. **requests** (>=2.31.0)
   - Purpose: HTTP client for fetching web pages
   - Usage: `src/core/fetcher.py`

2. **beautifulsoup4** (>=4.12.0)
   - Purpose: HTML/XML parsing
   - Usage: Extracting structured data from HTML documents
   - Parser: Uses lxml for better performance

3. **lxml** (>=4.9.0)
   - Purpose: XML/HTML parser backend for BeautifulSoup
   - Chosen for speed and robustness

4. **nltk** (>=3.8.0)
   - Purpose: Natural Language Processing
   - Features Used: Tokenization, stemming (Porter Stemmer), stopword removal
   - Data Downloads: punkt, punkt_tab, stopwords (downloaded on first run)

5. **rich** (>=13.7.0)
   - Purpose: Terminal formatting and output
   - Features Used: Colored text, tables, panels, progress indicators, box styles

### No External Services
The application operates entirely locally with no external API dependencies:
- No database connections
- No third-party SEO APIs
- No authentication services
- All processing happens in-memory

### Development Dependencies
- Testing framework would require pytest (not currently included in requirements.txt)
- Test files exist as placeholders in `src/tests/`