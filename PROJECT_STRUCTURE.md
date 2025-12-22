# SEO Optimizer - Project Structure

This document outlines the organized structure of the SEO Optimizer CLI tool.

## Directory Structure

```
seo_optimizer/
├── main.py                 # Main CLI entry point
├── requirements.txt        # Python dependencies
├── README.md              # Main documentation
├── LICENSE                # License file
├── PROJECT_STRUCTURE.md   # This file
├── RELEASE_NOTES.md       # Version history
│
├── src/                   # Source code
│   ├── app.py            # CLI application logic
│   ├── config.py         # Configuration constants
│   ├── analyzers/        # SEO analysis modules
│   ├── core/             # Core functionality
│   ├── output/           # Output formatters
│   ├── utils/            # Utility functions
│   └── tests/            # Unit tests
│
├── docs/                 # Documentation
│   ├── DESIGN_ARCHITECTURE_DOCS.md
│   ├── CONTRIBUTION_GUIDE.md
│   ├── GITHUB_CONTRIBUTION_SUMMARY.md
│   └── NOTES.md
│
├── examples/             # Example outputs and reports
│   └── visit_kili_report.json
│
└── venv/                # Virtual environment (gitignored)
```

## Key Components

### Main Entry Point
- `main.py` - CLI application entry point

### Source Code (`src/`)
- `app.py` - Main CLI application logic and argument parsing
- `config.py` - Configuration constants and settings
- `analyzers/` - SEO analysis modules (technical, content, structure, etc.)
- `core/` - Core orchestration and fetching logic
- `output/` - Output formatters (CLI renderer, JSON exporter)
- `utils/` - Utility functions (validation, text processing)
- `tests/` - Unit tests for all modules

### Documentation (`docs/`)
- Technical documentation, contribution guides, and project notes

### Examples (`examples/`)
- Sample output files and example reports

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
python main.py -u https://example.com -k "keyword1,keyword2" --ai
```

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest src/tests/

# Run with verbose output
python main.py -u https://example.com -k "seo,optimization" -v --ai
```