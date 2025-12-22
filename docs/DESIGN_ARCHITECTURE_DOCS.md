# SEO Analyzer Tool - Design & Architecture Document

## 1. Project Overview

### 1.1 Purpose
A Python-based CLI tool that analyzes web content against user-provided focus keywords (short-tail and long-tail) to provide SEO optimization recommendations with Google-like keyword matching.

### 1.2 Key Features
- URL-based content analysis
- Multi-keyword analysis (individual + cluster scoring)
- Google-like keyword matching (case-insensitive, stemming, semantic)
- Rich CLI output with colored formatting
- Optional JSON export
- Actionable improvement recommendations

---

## 2. System Architecture

### 2.1 Architecture Pattern
**Modular Pipeline Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface Layer                   │
│                  (rich + argparse)                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Orchestrator/Controller                 │
│              (Coordinates analysis pipeline)             │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Content    │  │   Keyword    │  │   Scoring    │
│   Fetcher    │  │   Processor  │  │   Engine     │
└──────────────┘  └──────────────┘  └──────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Analysis Modules                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │Technical │  │ Content  │  │Structure │  │ Links  │ │
│  │   SEO    │  │ Analyzer │  │ Analyzer │  │Analyzer│ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Report Generator                        │
│            (CLI Rich Output + JSON Export)               │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Component Breakdown

#### **CLI Interface Layer**
- **Technology**: `argparse` + `rich`
- **Responsibilities**:
  - Parse command-line arguments
  - Display progress indicators
  - Render colored, formatted output
  - Handle user input validation

#### **Orchestrator/Controller**
- **Responsibilities**:
  - Coordinate pipeline execution
  - Manage data flow between components
  - Handle errors and exceptions
  - Trigger report generation

#### **Content Fetcher**
- **Technology**: `requests` + `BeautifulSoup4`
- **Responsibilities**:
  - HTTP request handling
  - HTML content retrieval
  - Basic error handling (404, timeout, etc.)
  - robots.txt compliance (optional)

#### **Keyword Processor**
- **Technology**: `nltk` (Natural Language Toolkit)
- **Responsibilities**:
  - Tokenization
  - Stemming (PorterStemmer)
  - Stop words removal
  - Generate keyword variations
  - Create keyword clusters

#### **Scoring Engine**
- **Responsibilities**:
  - Calculate individual keyword scores
  - Calculate cluster scores
  - Aggregate module scores into overall score
  - Apply weighting logic

#### **Analysis Modules**
- **Technical SEO Analyzer**
- **Content Analyzer**
- **Structure Analyzer**
- **Link Analyzer**

#### **Report Generator**
- **Technology**: `rich` + `json`
- **Responsibilities**:
  - Format analysis results
  - Generate CLI output with colors/tables
  - Export JSON reports
  - Create actionable recommendations

---

## 3. Technical Specifications

### 3.1 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.8+ | Core language |
| HTTP Client | requests | 2.31+ | Web scraping |
| HTML Parser | BeautifulSoup4 | 4.12+ | HTML parsing |
| NLP | nltk | 3.8+ | Text processing |
| CLI Framework | rich | 13.7+ | Terminal UI |
| CLI Parser | argparse | stdlib | Argument parsing |
| JSON | json | stdlib | Report export |

### 3.2 Project Structure

```
seo_analyzer/
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── config.py                    # Configuration constants
├── README.md                    # Documentation
│
├── core/
│   ├── __init__.py
│   ├── orchestrator.py          # Main controller
│   ├── fetcher.py               # Content fetching
│   ├── keyword_processor.py    # Keyword processing
│   └── scoring.py               # Scoring logic
│
├── analyzers/
│   ├── __init__.py
│   ├── base_analyzer.py         # Base class
│   ├── technical_seo.py         # Technical SEO analysis
│   ├── content_analyzer.py      # Content analysis
│   ├── structure_analyzer.py    # Structure analysis
│   └── link_analyzer.py         # Link analysis
│
├── output/
│   ├── __init__.py
│   ├── cli_renderer.py          # Rich CLI output
│   └── json_exporter.py         # JSON export
│
├── utils/
│   ├── __init__.py
│   ├── text_utils.py            # Text processing helpers
│   └── validation.py            # Input validation
│
└── tests/
    ├── __init__.py
    ├── test_fetcher.py
    ├── test_keyword_processor.py
    └── test_analyzers.py
```

---

## 4. Data Models

### 4.1 Core Data Structures

```python
@dataclass
class AnalysisConfig:
    url: str
    keywords: List[str]
    output_json: bool = False
    json_path: Optional[str] = None
    verbose: bool = False

@dataclass
class WebContent:
    url: str
    html: str
    title: Optional[str]
    meta_description: Optional[str]
    h1: Optional[str]
    headings: Dict[str, List[str]]  # h2, h3, etc.
    body_text: str
    images: List[Dict]
    links: List[Dict]
    word_count: int

@dataclass
class KeywordVariation:
    original: str
    stemmed: str
    variations: List[str]
    stop_words_removed: str

@dataclass
class KeywordScore:
    keyword: str
    score: int  # 0-100
    in_title: bool
    in_meta: bool
    in_h1: bool
    in_headings: List[str]
    in_first_100_words: bool
    density: float
    distribution_score: int
    findings: Dict[str, Any]
    recommendations: List[str]

@dataclass
class ClusterScore:
    keywords: List[str]
    cluster_score: int  # 0-100
    individual_scores: List[KeywordScore]
    semantic_coverage: int
    co_occurrence_score: int
    related_terms_found: List[str]

@dataclass
class ModuleResult:
    module_name: str
    score: int  # 0-100
    status: str  # 'passed', 'warning', 'failed'
    details: Dict[str, Any]
    recommendations: List[str]

@dataclass
class AnalysisReport:
    url: str
    analyzed_at: str
    overall_score: int  # 0-100
    keyword_cluster: ClusterScore
    technical_seo: ModuleResult
    content_analysis: ModuleResult
    structure_analysis: ModuleResult
    link_analysis: ModuleResult
    top_recommendations: List[str]
```

---

## 5. Module Specifications

### 5.1 Technical SEO Analyzer

**Checks:**
- Title tag (length: 50-60 chars optimal, keyword presence)
- Meta description (length: 150-160 chars, keyword presence)
- Meta robots tag
- Canonical tag
- Open Graph tags (og:title, og:description)
- HTTP status code (200 OK)

**Scoring:**
```
Total: 100 points
- Title optimization: 30 points
- Meta description: 25 points
- Meta robots: 10 points
- Canonical: 10 points
- Open Graph: 15 points
- HTTP status: 10 points
```

### 5.2 Content Analyzer

**Checks:**
- Word count (min 300 words recommended)
- Keyword density per keyword (optimal: 1-3%)
- Keyword in first 100 words
- Keyword distribution (beginning, middle, end)
- Readability (optional: Flesch reading ease)
- Content uniqueness indicators

**Scoring:**
```
Total: 100 points per keyword
- Title presence: 20 points
- Meta description: 15 points
- H1 presence: 15 points
- H2-H3 presence: 10 points
- First 100 words: 10 points
- Optimal density: 15 points
- Distribution: 15 points
```

**Keyword Matching Logic:**
1. Normalize (lowercase)
2. Remove stop words ("the", "a", "and", "in", "to", "of", etc.)
3. Stem words (using PorterStemmer)
4. Match stemmed forms
5. Check for variations and proximity

### 5.3 Structure Analyzer

**Checks:**
- H1 tag (should be one, contains keyword)
- Heading hierarchy (H1 > H2 > H3...)
- Paragraph structure (not too long)
- List usage (ul, ol)
- Image optimization (alt tags, keyword in alt)

**Scoring:**
```
Total: 100 points
- H1 optimization: 30 points
- Heading hierarchy: 25 points
- Paragraph structure: 20 points
- List usage: 10 points
- Image alt tags: 15 points
```

### 5.4 Link Analyzer

**Checks:**
- Internal links count (3-10 recommended)
- External links count
- Broken links (optional)
- Anchor text analysis (keyword usage)
- Nofollow attributes

**Scoring:**
```
Total: 100 points
- Internal links: 35 points
- External links: 25 points
- Anchor text: 25 points
- Link health: 15 points
```

---

## 6. Keyword Processing Algorithm

### 6.1 Processing Pipeline

```python
def process_keyword(keyword: str) -> KeywordVariation:
    """
    1. Normalize: lowercase
    2. Tokenize: split into words
    3. Remove stop words
    4. Stem each word
    5. Generate variations
    """
    pass

def match_keyword_in_content(keyword_variation: KeywordVariation, 
                             content: str) -> List[Match]:
    """
    1. Process content (normalize, stem)
    2. Search for exact matches
    3. Search for variations
    4. Search for partial matches
    5. Calculate proximity scores
    """
    pass
```

### 6.2 Stop Words List

Use NLTK's English stop words:
```python
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
```

### 6.3 Stemming

Use Porter Stemmer for consistency:
```python
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
```

---

## 7. Scoring System

### 7.1 Overall Score Calculation

```
Overall Score (0-100) = Weighted Average:
- Keyword Analysis: 40%
- Technical SEO: 20%
- Content Quality: 20%
- Structure: 10%
- Links: 10%
```

### 7.2 Individual Keyword Score

```
Score = (
    title_match * 0.20 +
    meta_match * 0.15 +
    h1_match * 0.15 +
    headings_match * 0.10 +
    first_100_words * 0.10 +
    density_score * 0.15 +
    distribution_score * 0.15
) * 100
```

### 7.3 Cluster Score

```
Cluster Score = (
    avg(individual_scores) * 0.60 +
    semantic_coverage * 0.25 +
    co_occurrence * 0.15
) * 100

Where:
- semantic_coverage = related_terms_found / expected_terms
- co_occurrence = keywords_used_together / total_keywords
```

---

## 8. CLI Interface Design

### 8.1 Command Structure

```bash
python seo_analyzer.py --url "https://example.com" \
                       --keywords "python tutorial,learn python,python for beginners" \
                       [--output report.json] \
                       [--verbose] \
                       [--help]
```

### 8.2 Arguments

| Argument | Short | Required | Description |
|----------|-------|----------|-------------|
| --url | -u | Yes | Target URL to analyze |
| --keywords | -k | Yes | Comma-separated keywords |
| --output | -o | No | JSON output file path |
| --verbose | -v | No | Detailed output |
| --help | -h | No | Show help message |

### 8.3 Output Format

#### CLI Output Structure:
```
🔍 Analyzing: https://example.com
Focus Keywords: "python tutorial", "learn python", "python for beginners"

[Progress bar with rich.Progress]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SEO ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 OVERALL SEO SCORE: 72/100

┌────────────────────────────────────────────────────────┐
│ 🎯 Keyword Cluster Performance: 75/100                 │
├────────────────────────────────────────────────────────┤
│ Related terms detected: tutorial, tutorials, learn,    │
│ learning, beginner, beginners, python                  │
└────────────────────────────────────────────────────────┘

📈 Individual Keyword Scores:

✅ "python tutorial" - 85/100
   ├─ Title: ✓ Found (exact match)
   ├─ Meta: ✓ Found
   ├─ H1: ✓ Found (variation: "Python Tutorial")
   ├─ Density: 1.2% (optimal)
   └─ First 100 words: ✓ Yes

⚠️  "learn python" - 65/100
   ├─ Title: ✗ Not found
   ├─ Meta: ✓ Found
   ├─ H2: ✓ Found (variation: "learning Python")
   ├─ Density: 0.8% (low)
   └─ First 100 words: ✗ No
   💡 Recommendation: Add to title or first paragraph

❌ "python for beginners" - 45/100
   ├─ Title: ✗ Not found
   ├─ Meta: ✗ Not found
   ├─ Headings: ✗ Not found
   ├─ Density: 0.3% (very low)
   └─ First 100 words: ✗ No
   💡 Recommendation: This keyword needs more prominence

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Technical SEO: 88/100
   ├─ Title Tag: ✓ Optimized (58 chars)
   ├─ Meta Description: ⚠️  Too short (145 chars)
   ├─ H1 Tag: ✓ Present and optimized
   ├─ Canonical: ✓ Present
   └─ Open Graph: ✓ Complete

⚠️  Content Analysis: 70/100
   ├─ Word Count: ✓ 850 words
   ├─ Keyword Usage: ⚠️  Uneven distribution
   └─ Readability: ✓ Good (Flesch: 65)

✅ Structure: 82/100
   ├─ Heading Hierarchy: ✓ Proper
   ├─ Images: ⚠️  3 missing alt tags
   └─ Paragraphs: ✓ Well structured

⚠️  Links: 65/100
   ├─ Internal Links: ⚠️  Only 2 (recommend 5-10)
   ├─ External Links: ✓ 4 links
   └─ Anchor Text: ⚠️  Generic text used

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TOP RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🔴 CRITICAL: Add "python for beginners" to title and H2 headings
2. 🟡 HIGH: Increase internal linking (add 3-8 more links)
3. 🟡 HIGH: Add alt tags to 3 images with relevant keywords
4. 🟢 MEDIUM: Extend meta description to 150-160 characters
5. 🟢 MEDIUM: Include "learn python" in first paragraph

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Analysis complete! Report saved to: report.json
```

#### Color Scheme (Rich):
- **Green** (`[green]`): Passed checks, good scores (80-100)
- **Yellow** (`[yellow]`): Warnings, medium scores (60-79)
- **Red** (`[red]`): Failed checks, low scores (0-59)
- **Blue** (`[blue]`): Information, headers
- **Cyan** (`[cyan]`): URLs, data values
- **Magenta** (`[magenta]`): Keywords, important terms

### 8.4 JSON Output Format

```json
{
  "meta": {
    "url": "https://example.com",
    "analyzed_at": "2025-11-18T10:30:00Z",
    "tool_version": "1.0.0",
    "keywords_analyzed": ["python tutorial", "learn python", "python for beginners"]
  },
  "overall_score": 72,
  "keyword_analysis": {
    "cluster_score": 75,
    "semantic_coverage": 85,
    "co_occurrence_score": 70,
    "related_terms_found": ["tutorial", "tutorials", "learn", "learning", "beginner"],
    "individual_keywords": [
      {
        "keyword": "python tutorial",
        "score": 85,
        "findings": {
          "in_title": true,
          "title_position": 0,
          "in_meta": true,
          "in_h1": true,
          "in_headings": ["h1", "h2"],
          "in_first_100_words": true,
          "density": 1.2,
          "occurrences": 12,
          "distribution": {
            "beginning": 4,
            "middle": 5,
            "end": 3
          }
        },
        "recommendations": []
      },
      {
        "keyword": "learn python",
        "score": 65,
        "findings": {
          "in_title": false,
          "in_meta": true,
          "in_h1": false,
          "in_headings": ["h2"],
          "in_first_100_words": false,
          "density": 0.8,
          "occurrences": 7,
          "distribution": {
            "beginning": 1,
            "middle": 4,
            "end": 2
          }
        },
        "recommendations": [
          "Add 'learn python' to title tag",
          "Include in first 100 words",
          "Increase density to 1-3%"
        ]
      }
    ]
  },
  "technical_seo": {
    "score": 88,
    "status": "passed",
    "details": {
      "title": {
        "present": true,
        "length": 58,
        "optimal_length": true,
        "contains_keyword": true,
        "content": "Python Tutorial - Learn Programming Basics"
      },
      "meta_description": {
        "present": true,
        "length": 145,
        "optimal_length": false,
        "contains_keyword": true,
        "content": "Learn Python programming with our comprehensive tutorial..."
      },
      "canonical": {
        "present": true,
        "url": "https://example.com/python-tutorial"
      },
      "open_graph": {
        "present": true,
        "complete": true
      },
      "http_status": 200
    },
    "recommendations": [
      "Extend meta description to 150-160 characters"
    ]
  },
  "content_analysis": {
    "score": 70,
    "status": "warning",
    "details": {
      "word_count": 850,
      "adequate_length": true,
      "readability_score": 65,
      "readability_level": "Good",
      "keyword_distribution": "uneven"
    },
    "recommendations": [
      "Distribute keywords more evenly throughout content",
      "Add more occurrences of 'python for beginners'"
    ]
  },
  "structure_analysis": {
    "score": 82,
    "status": "passed",
    "details": {
      "h1": {
        "count": 1,
        "proper": true,
        "contains_keyword": true
      },
      "heading_hierarchy": {
        "proper": true,
        "structure": ["h1", "h2", "h2", "h3", "h3", "h2"]
      },
      "images": {
        "total": 8,
        "with_alt": 5,
        "without_alt": 3,
        "alt_with_keywords": 3
      },
      "paragraphs": {
        "count": 15,
        "avg_length": 85,
        "well_structured": true
      }
    },
    "recommendations": [
      "Add alt text to 3 images",
      "Include keywords in alt text where relevant"
    ]
  },
  "link_analysis": {
    "score": 65,
    "status": "warning",
    "details": {
      "internal_links": {
        "count": 2,
        "recommended_min": 5
      },
      "external_links": {
        "count": 4,
        "nofollow_count": 1
      },
      "anchor_text": {
        "keyword_anchors": 1,
        "generic_anchors": 3
      }
    },
    "recommendations": [
      "Add 3-8 more internal links",
      "Use keyword-rich anchor text",
      "Link to related content on your site"
    ]
  },
  "top_recommendations": [
    {
      "priority": "critical",
      "category": "keyword_optimization",
      "message": "Add 'python for beginners' to title and H2 headings"
    },
    {
      "priority": "high",
      "category": "internal_linking",
      "message": "Increase internal linking (add 3-8 more links)"
    },
    {
      "priority": "high",
      "category": "image_optimization",
      "message": "Add alt tags to 3 images with relevant keywords"
    },
    {
      "priority": "medium",
      "category": "meta_optimization",
      "message": "Extend meta description to 150-160 characters"
    },
    {
      "priority": "medium",
      "category": "content_optimization",
      "message": "Include 'learn python' in first paragraph"
    }
  ]
}
```

---

## 9. Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Set up project structure
- [ ] Implement CLI interface with argparse
- [ ] Implement Content Fetcher
- [ ] Basic HTML parsing with BeautifulSoup
- [ ] Simple keyword matching (case-insensitive)

### Phase 2: Core Analysis (Week 2)
- [ ] Implement Keyword Processor (NLTK integration)
- [ ] Implement Technical SEO Analyzer
- [ ] Implement Content Analyzer
- [ ] Implement Structure Analyzer
- [ ] Basic scoring system

### Phase 3: Advanced Features (Week 3)
- [ ] Implement Link Analyzer
- [ ] Implement Cluster scoring
- [ ] Advanced keyword matching (stemming, variations)
- [ ] Implement Scoring Engine with weights
- [ ] Generate recommendations logic

### Phase 4: Output & Polish (Week 4)
- [ ] Implement Rich CLI renderer
- [ ] Implement JSON exporter
- [ ] Add progress indicators
- [ ] Error handling and validation
- [ ] Testing and bug fixes
- [ ] Documentation

---

## 10. Configuration

### 10.1 config.py

```python
# Optimal ranges
OPTIMAL_TITLE_LENGTH = (50, 60)
OPTIMAL_META_DESC_LENGTH = (150, 160)
OPTIMAL_KEYWORD_DENSITY = (1.0, 3.0)
MIN_WORD_COUNT = 300
RECOMMENDED_INTERNAL_LINKS = (5, 10)

# Scoring weights
WEIGHTS = {
    'keyword_analysis': 0.40,
    'technical_seo': 0.20,
    'content_analysis': 0.20,
    'structure': 0.10,
    'links': 0.10
}

# Keyword scoring weights
KEYWORD_WEIGHTS = {
    'title': 0.20,
    'meta': 0.15,
    'h1': 0.15,
    'headings': 0.10,
    'first_100_words': 0.10,
    'density': 0.15,
    'distribution': 0.15
}

# Cluster scoring weights
CLUSTER_WEIGHTS = {
    'individual_avg': 0.60,
    'semantic_coverage': 0.25,
    'co_occurrence': 0.15
}

# HTTP settings
REQUEST_TIMEOUT = 30
USER_AGENT = 'SEO-Analyzer/1.0 (Python)'

# NLTK settings
NLTK_DATA_PATH = './nltk_data'
STEMMER_TYPE = 'porter'  # or 'lancaster'
```

---

## 11. Error Handling

### 11.1 Expected Errors

| Error Type | Handling Strategy |
|------------|------------------|
| URL not accessible (404, 500) | Show error, suggest checking URL |
| Network timeout | Retry 2 times, then fail gracefully |
| Invalid HTML | Parse what's available, warn user |
| Empty content | Error: "No content found to analyze" |
| No keywords provided | Error: "Keywords required" |
| NLTK data missing | Auto-download or provide instructions |

### 11.2 Validation Rules

```python
def validate_url(url: str) -> bool:
    # Must start with http:// or https://
    # Must be valid URL format
    pass

def validate_keywords(keywords: str) -> bool:
    # Must not be empty
    # At least one keyword after splitting
    pass
```

---

## 12. Dependencies

### 12.1 requirements.txt

```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
nltk>=3.8.0
rich>=13.7.0
lxml>=4.9.0
```

### 12.2 NLTK Data Requirements

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

---

## 13. Testing Strategy

### 13.1 Unit Tests
- Test each analyzer independently
- Test keyword processing functions
- Test scoring calculations
- Test URL validation

### 13.2 Integration Tests
- Test full pipeline with sample URLs
- Test CLI argument parsing
- Test JSON export

### 13.3 Test Data
Create sample HTML files:
- `test_data/good_seo.html` (high scores)
- `test_data/poor_seo.html` (low scores)
- `test_data/medium_seo.html` (medium scores)

---

## 14. Future Enhancements (v2.0)

- [ ] Integrate Google Search Console API
- [ ] Add competitor comparison
- [ ] Implement semantic similarity (spaCy)
- [ ] Add synonym matching
- [ ] Content freshness analysis
- [ ] Mobile-friendliness check
- [ ] Page speed analysis
- [ ] Schema markup validation
- [ ] Multi-language support
- [ ] Batch URL analysis
- [ ] Historical tracking (database)
- [ ] Web dashboard (Flask/FastAPI)

---

## 15. Success Metrics

### 15.1 Performance Targets
- Analysis time: < 10 seconds per URL
- Memory usage: < 200MB
- Accuracy: 85%+ compared to manual SEO audit

### 15.2 Code Quality
- Test coverage: > 80%
- PEP 8 compliance
- Type hints throughout
- Comprehensive docstrings

---

## 16. Getting Started

### 16.1 Installation

```bash
# Clone repository
git clone <repo-url>
cd seo_analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 16.2 Basic Usage

```bash
python main.py --url "https://example.com" \
               --keywords "python tutorial,learn python" \
               --output report.json
```

---

## 17. Development Guidelines

### 17.1 Code Style
- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused and small
- Use meaningful variable names

### 17.2 Git Workflow
- Feature branches: `feature/feature-name`
- Commit messages: Clear and descriptive
- Pull requests: Required for main branch
- Code review: Before merging

### 17.3 Documentation
- README with usage examples
- Inline code comments for complex logic
- API documentation for public functions
- Keep this design doc updated

---

## 18. Example Implementation Snippets

### 18.1 Main Entry Point

```python
# main.py
import argparse
from rich.console import Console
from core.orchestrator import Orchestrator
from output.cli_renderer import CLIRenderer
from output.json_exporter import JSONExporter

def main():
    parser = argparse.ArgumentParser(
        description='SEO Analyzer - Analyze web content for SEO optimization'
    )
    parser.add_argument('-u', '--url', required=True, help='Target URL to analyze')
    parser.add_argument('-k', '--keywords', required=True, 
                       help='Comma-separated keywords')
    parser.add_argument('-o', '--output', help='JSON output file path')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Verbose output')
    
    args = parser.parse_args()
    
    console = Console()
    
    try:
        # Parse keywords
        keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
        
        # Initialize orchestrator
        orchestrator = Orchestrator(args.url, keywords, args.verbose)
        
        # Run analysis
        console.print(f"🔍 Analyzing: [cyan]{args.url}[/cyan]")
        console.print(f"Focus Keywords: [magenta]{', '.join(keywords)}[/magenta]\n")
        
        report = orchestrator.analyze()
        
        # Render CLI output
        renderer = CLIRenderer(console)
        renderer.render(report)
        
        # Export JSON if requested
        if args.output:
            exporter = JSONExporter()
            exporter.export(report, args.output)
            console.print(f"\n✅ Analysis complete! Report saved to: [cyan]{args.output}[/cyan]")
        else:
            console.print("\n✅ Analysis complete!")
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
```

### 18.2 Orchestrator Class

```python
# core/orchestrator.py
from typing import List
from rich.progress import Progress, SpinnerColumn, TextColumn
from dataclasses import dataclass

from core.fetcher import ContentFetcher
from core.keyword_processor import KeywordProcessor
from core.scoring import ScoringEngine
from analyzers.technical_seo import TechnicalSEOAnalyzer
from analyzers.content_analyzer import ContentAnalyzer
from analyzers.structure_analyzer import StructureAnalyzer
from analyzers.link_analyzer import LinkAnalyzer

class Orchestrator:
    def __init__(self, url: str, keywords: List[str], verbose: bool = False):
        self.url = url
        self.keywords = keywords
        self.verbose = verbose
        
        # Initialize components
        self.fetcher = ContentFetcher()
        self.keyword_processor = KeywordProcessor()
        self.scoring_engine = ScoringEngine()
        
        # Initialize analyzers
        self.analyzers = {
            'technical_seo': TechnicalSEOAnalyzer(),
            'content': ContentAnalyzer(),
            'structure': StructureAnalyzer(),
            'links': LinkAnalyzer()
        }
    
    def analyze(self) -> 'AnalysisReport':
        """Run complete analysis pipeline"""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            
            # Step 1: Fetch content
            task = progress.add_task("Fetching content...", total=None)
            web_content = self.fetcher.fetch(self.url)
            progress.update(task, completed=True)
            
            # Step 2: Process keywords
            task = progress.add_task("Processing keywords...", total=None)
            keyword_variations = self.keyword_processor.process_keywords(self.keywords)
            progress.update(task, completed=True)
            
            # Step 3: Run analyzers
            results = {}
            for name, analyzer in self.analyzers.items():
                task = progress.add_task(f"Running {name} analysis...", total=None)
                results[name] = analyzer.analyze(web_content, keyword_variations)
                progress.update(task, completed=True)
            
            # Step 4: Calculate scores
            task = progress.add_task("Calculating scores...", total=None)
            report = self.scoring_engine.generate_report(
                self.url, 
                self.keywords,
                web_content,
                keyword_variations,
                results
            )
            progress.update(task, completed=True)
        
        return report
```

### 18.3 Content Fetcher

```python
# core/fetcher.py
import requests
from bs4 import BeautifulSoup
from typing import Optional
from dataclasses import dataclass
from config import REQUEST_TIMEOUT, USER_AGENT

@dataclass
class WebContent:
    url: str
    html: str
    soup: BeautifulSoup
    title: Optional[str]
    meta_description: Optional[str]
    h1: Optional[str]
    headings: dict
    body_text: str
    images: list
    links: list
    word_count: int

class ContentFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def fetch(self, url: str) -> WebContent:
        """Fetch and parse web content"""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            
            # Extract elements
            title = self._extract_title(soup)
            meta_desc = self._extract_meta_description(soup)
            h1 = self._extract_h1(soup)
            headings = self._extract_headings(soup)
            body_text = self._extract_body_text(soup)
            images = self._extract_images(soup)
            links = self._extract_links(soup, url)
            word_count = len(body_text.split())
            
            return WebContent(
                url=url,
                html=html,
                soup=soup,
                title=title,
                meta_description=meta_desc,
                h1=h1,
                headings=headings,
                body_text=body_text,
                images=images,
                links=links,
                word_count=word_count
            )
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else None
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        return meta_tag.get('content', '').strip() if meta_tag else None
    
    def _extract_h1(self, soup: BeautifulSoup) -> Optional[str]:
        h1_tag = soup.find('h1')
        return h1_tag.get_text().strip() if h1_tag else None
    
    def _extract_headings(self, soup: BeautifulSoup) -> dict:
        headings = {}
        for level in range(1, 7):
            tags = soup.find_all(f'h{level}')
            headings[f'h{level}'] = [tag.get_text().strip() for tag in tags]
        return headings
    
    def _extract_body_text(self, soup: BeautifulSoup) -> str:
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _extract_images(self, soup: BeautifulSoup) -> list:
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        return images
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> list:
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            links.append({
                'href': href,
                'text': link.get_text().strip(),
                'is_internal': self._is_internal_link(href, base_url),
                'nofollow': 'nofollow' in link.get('rel', [])
            })
        return links
    
    def _is_internal_link(self, href: str, base_url: str) -> bool:
        from urllib.parse import urlparse
        base_domain = urlparse(base_url).netloc
        
        if href.startswith('/') or href.startswith('#'):
            return True
        
        link_domain = urlparse(href).netloc
        return link_domain == base_domain or link_domain == ''
```

### 18.4 Keyword Processor

```python
# core/keyword_processor.py
from typing import List
from dataclasses import dataclass
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

@dataclass
class KeywordVariation:
    original: str
    normalized: str
    stemmed_tokens: List[str]
    tokens_no_stopwords: List[str]

class KeywordProcessor:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
    
    def process_keywords(self, keywords: List[str]) -> List[KeywordVariation]:
        """Process list of keywords into variations"""
        return [self.process_keyword(kw) for kw in keywords]
    
    def process_keyword(self, keyword: str) -> KeywordVariation:
        """Process single keyword"""
        # Normalize
        normalized = keyword.lower().strip()
        
        # Tokenize
        tokens = word_tokenize(normalized)
        
        # Remove stop words
        tokens_no_stopwords = [t for t in tokens if t not in self.stop_words]
        
        # Stem
        stemmed_tokens = [self.stemmer.stem(t) for t in tokens_no_stopwords]
        
        return KeywordVariation(
            original=keyword,
            normalized=normalized,
            stemmed_tokens=stemmed_tokens,
            tokens_no_stopwords=tokens_no_stopwords
        )
    
    def match_in_text(self, keyword_var: KeywordVariation, text: str) -> dict:
        """Find keyword matches in text"""
        text_lower = text.lower()
        text_tokens = word_tokenize(text_lower)
        text_stemmed = [self.stemmer.stem(t) for t in text_tokens]
        
        matches = {
            'exact': keyword_var.normalized in text_lower,
            'partial': any(token in text_tokens for token in keyword_var.tokens_no_stopwords),
            'stemmed': any(stem in text_stemmed for stem in keyword_var.stemmed_tokens),
            'count': text_lower.count(keyword_var.normalized),
            'positions': []
        }
        
        # Find positions
        start = 0
        while True:
            pos = text_lower.find(keyword_var.normalized, start)
            if pos == -1:
                break
            matches['positions'].append(pos)
            start = pos + 1
        
        return matches
    
    def calculate_density(self, keyword_var: KeywordVariation, text: str, word_count: int) -> float:
        """Calculate keyword density"""
        matches = self.match_in_text(keyword_var, text)
        keyword_word_count = len(keyword_var.tokens_no_stopwords)
        
        if word_count == 0:
            return 0.0
        
        # Count all variations
        total_matches = matches['count']
        
        density = (total_matches * keyword_word_count / word_count) * 100
        return round(density, 2)
```

### 18.5 Content Analyzer Example

```python
# analyzers/content_analyzer.py
from typing import List
from dataclasses import dataclass
from core.keyword_processor import KeywordVariation
from core.fetcher import WebContent
from config import OPTIMAL_KEYWORD_DENSITY, MIN_WORD_COUNT, KEYWORD_WEIGHTS

@dataclass
class KeywordScore:
    keyword: str
    score: int
    in_title: bool
    in_meta: bool
    in_h1: bool
    in_headings: List[str]
    in_first_100_words: bool
    density: float
    distribution_score: int
    recommendations: List[str]

class ContentAnalyzer:
    def __init__(self):
        self.keyword_processor = KeywordProcessor()
    
    def analyze(self, content: WebContent, keyword_vars: List[KeywordVariation]) -> dict:
        """Analyze content for keywords"""
        keyword_scores = []
        
        for kw_var in keyword_vars:
            score = self._analyze_keyword(content, kw_var)
            keyword_scores.append(score)
        
        # Calculate cluster score
        avg_score = sum(s.score for s in keyword_scores) / len(keyword_scores)
        
        return {
            'individual_scores': keyword_scores,
            'cluster_score': int(avg_score),
            'word_count': content.word_count,
            'adequate_length': content.word_count >= MIN_WORD_COUNT
        }
    
    def _analyze_keyword(self, content: WebContent, kw_var: KeywordVariation) -> KeywordScore:
        """Analyze single keyword"""
        # Check title
        in_title = self._check_in_text(kw_var, content.title or '')
        
        # Check meta description
        in_meta = self._check_in_text(kw_var, content.meta_description or '')
        
        # Check H1
        in_h1 = self._check_in_text(kw_var, content.h1 or '')
        
        # Check headings
        in_headings = []
        for level, headings in content.headings.items():
            for heading in headings:
                if self._check_in_text(kw_var, heading):
                    in_headings.append(level)
        
        # Check first 100 words
        first_100 = ' '.join(content.body_text.split()[:100])
        in_first_100 = self._check_in_text(kw_var, first_100)
        
        # Calculate density
        density = self.keyword_processor.calculate_density(
            kw_var, content.body_text, content.word_count
        )
        
        # Calculate distribution score
        distribution_score = self._calculate_distribution(kw_var, content.body_text)
        
        # Calculate total score
        score = self._calculate_score(
            in_title, in_meta, in_h1, in_headings, 
            in_first_100, density, distribution_score
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            kw_var.original, in_title, in_meta, in_h1, 
            in_first_100, density
        )
        
        return KeywordScore(
            keyword=kw_var.original,
            score=score,
            in_title=in_title,
            in_meta=in_meta,
            in_h1=in_h1,
            in_headings=in_headings,
            in_first_100_words=in_first_100,
            density=density,
            distribution_score=distribution_score,
            recommendations=recommendations
        )
    
    def _check_in_text(self, kw_var: KeywordVariation, text: str) -> bool:
        """Check if keyword is in text"""
        matches = self.keyword_processor.match_in_text(kw_var, text)
        return matches['exact'] or matches['stemmed']
    
    def _calculate_distribution(self, kw_var: KeywordVariation, text: str) -> int:
        """Calculate how well keyword is distributed"""
        matches = self.keyword_processor.match_in_text(kw_var, text)
        positions = matches['positions']
        
        if not positions:
            return 0
        
        text_len = len(text)
        beginning = text_len * 0.33
        end = text_len * 0.67
        
        in_beginning = any(p < beginning for p in positions)
        in_middle = any(beginning <= p < end for p in positions)
        in_end = any(p >= end for p in positions)
        
        # Score based on distribution
        coverage = sum([in_beginning, in_middle, in_end])
        return int((coverage / 3) * 100)
    
    def _calculate_score(self, in_title, in_meta, in_h1, in_headings, 
                        in_first_100, density, distribution) -> int:
        """Calculate keyword score"""
        score = 0
        
        # Apply weights from config
        if in_title:
            score += KEYWORD_WEIGHTS['title'] * 100
        if in_meta:
            score += KEYWORD_WEIGHTS['meta'] * 100
        if in_h1:
            score += KEYWORD_WEIGHTS['h1'] * 100
        if in_headings:
            score += KEYWORD_WEIGHTS['headings'] * 100
        if in_first_100:
            score += KEYWORD_WEIGHTS['first_100_words'] * 100
        
        # Density score
        min_density, max_density = OPTIMAL_KEYWORD_DENSITY
        if min_density <= density <= max_density:
            score += KEYWORD_WEIGHTS['density'] * 100
        elif density > 0:
            # Partial credit if outside optimal range
            score += KEYWORD_WEIGHTS['density'] * 50
        
        # Distribution score
        score += KEYWORD_WEIGHTS['distribution'] * (distribution / 100) * 100
        
        return int(score)
    
    def _generate_recommendations(self, keyword, in_title, in_meta, 
                                 in_h1, in_first_100, density) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if not in_title:
            recommendations.append(f"Add '{keyword}' to title tag")
        if not in_meta:
            recommendations.append(f"Add '{keyword}' to meta description")
        if not in_h1:
            recommendations.append(f"Include '{keyword}' in H1 heading")
        if not in_first_100:
            recommendations.append(f"Use '{keyword}' in the first 100 words")
        
        min_density, max_density = OPTIMAL_KEYWORD_DENSITY
        if density < min_density:
            recommendations.append(f"Increase keyword density (current: {density}%, optimal: {min_density}-{max_density}%)")
        elif density > max_density:
            recommendations.append(f"Reduce keyword density to avoid stuffing (current: {density}%, optimal: {min_density}-{max_density}%)")
        
        return recommendations
```

---

## 19. Sample Usage Examples

### 19.1 Basic Analysis
```bash
python main.py --url "https://example.com/python-tutorial" \
               --keywords "python tutorial,learn python"
```

### 19.2 With JSON Export
```bash
python main.py --url "https://example.com/python-tutorial" \
               --keywords "python tutorial,learn python,python for beginners" \
               --output reports/example_report.json
```

### 19.3 Verbose Mode
```bash
python main.py --url "https://example.com/python-tutorial" \
               --keywords "python tutorial" \
               --verbose
```

---

## 20. Troubleshooting Guide

### 20.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| ModuleNotFoundError: nltk | NLTK not installed | `pip install nltk` |
| LookupError: punkt | NLTK data missing | Run `python -c "import nltk; nltk.download('punkt')"` |
| Connection timeout | Server slow/blocked | Increase REQUEST_TIMEOUT in config |
| Empty content extracted | JS-rendered site | Consider Selenium (future enhancement) |
| UnicodeDecodeError | Encoding issues | Add encoding handling in fetcher |

### 20.2 Debug Mode

Add debug logging:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 21. Performance Optimization Tips

1. **Caching**: Cache fetched content for repeated analyses
2. **Parallel Processing**: Analyze multiple keywords in parallel
3. **Lazy Loading**: Load NLTK data only when needed
4. **Connection Pooling**: Reuse HTTP connections
5. **Memory Management**: Process large HTML in chunks

---

## 22. Security Considerations

1. **URL Validation**: Validate URLs before fetching
2. **SSRF Protection**: Block internal IPs (127.0.0.1, localhost)
3. **Size Limits**: Limit response size to prevent DoS
4. **Timeout**: Always use timeouts on requests
5. **User Input**: Sanitize all user input

---

## 23. Deployment Checklist

- [ ] All dependencies in requirements.txt
- [ ] NLTK data download automated
- [ ] Error handling comprehensive
- [ ] Logging configured
- [ ] Documentation complete
- [ ] Tests passing
- [ ] README with examples
- [ ] License file included
- [ ] .gitignore configured
- [ ] Version number set

---

## 24. Support and Maintenance

### 24.1 Versioning
Follow Semantic Versioning (SemVer):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

### 24.2 Changelog
Maintain CHANGELOG.md with:
- Added features
- Changed functionality
- Deprecated features
- Removed features
- Fixed bugs
- Security updates

---

## 25. License

Recommend: MIT License (permissive, widely accepted)

---

## END OF DOCUMENT

**Document Version**: 1.0  
**Last Updated**: November 18, 2025  
**Status**: Ready for Development  

**Next Steps**:
1. Review and approve design
2. Set up development environment
3. Create GitHub repository
4. Begin Phase 1 implementation
5. Schedule code reviews

**Questions or Concerns?**  
Contact development team for clarifications before starting implementation.
