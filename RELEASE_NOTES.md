# Release Notes

## v2.2.0: 20 Stars Milestone — CI, Dependabot & Community

**Released:** August 3, 2026  
**Branch:** `release/v2.2.0-20-stars`

Thank you for **20+ GitHub stars**. This release hardens the project for contributors and long-term maintenance so more people can trust and adopt SEO Analyzer.

### Highlights

#### GitHub automation (`.github/`)
- **CI workflow** (`ci.yml`): lint/compile + pytest on Python 3.9–3.12 for pushes and pull requests on `main`, `release/**`, and `feature/**`
- **CLI smoke job**: verifies `main.py --help` and `--version`
- **Dependabot** (`dependabot.yml`): weekly updates for `pip` and `github-actions` (opened by `@dependabot[bot]`)
- **Daily Maintenance** (`daily-maintenance.yml`): scheduled 09:00 UTC activity log + `workflow_dispatch`
- **FUNDING.yml**: support link for sponsors and fans
- **Issue & PR templates**: faster bug reports and feature requests

#### Product / DX
- CLI **`--version`** (`SEO Analyzer 2.2.0`)
- Real unit tests under `src/tests/` (validation, scoring, fetcher, keywords, analyzers)
- `requirements-dev.txt` for pytest in local and CI environments
- README badges (CI + Support) and clearer support section

#### Support anyone interested
- Primary support link: **[https://snippe.me/pay/support-cleven](https://snippe.me/pay/support-cleven)**
- Also available via the GitHub **Sponsor / Fund** button (custom funding URL)

### How to try this branch

```bash
git fetch origin
git checkout release/v2.2.0-20-stars
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest src/tests -v
python main.py --version
```

### Upgrade notes
- No breaking CLI changes from v2.1.x
- CI expects Python **3.9+** in the matrix (3.8 may still work locally but is not CI-tested)

---

## v2.1.1: Enhanced Developer Experience & Documentation

**Released:** January 8, 2026

### New Additions

#### Contributing Guidelines
- Added comprehensive CONTRIBUTING.md with detailed guidelines
- Development setup instructions and prerequisites
- Code style guide with examples and best practices
- Testing guidelines with pytest examples
- Commit message format using Conventional Commits
- Pull request checklist for contributors
- Security guidelines for safe development

#### Improvements
- Enhanced documentation structure for better contributor onboarding
- Clear project structure overview
- Quick contribution checklist for PRs
- Recognition section for contributors

### Developer Experience
- Detailed environment setup instructions
- Code example templates for consistent style
- Testing framework documentation
- Performance and security considerations

---

## v2.1.0: AI Flexibility with Gemini & OpenAI

**Released:** November 24, 2025

## Major Features

### Dual AI Provider Support
We've completely refactored the AI integration system to provide maximum flexibility and cost-effectiveness:

- **Google Gemini 2.5 Flash** (FREE - Recommended)
  - Free tier API access
  - Fast and reliable
  - Perfect for individual developers and startups
  - No credit card required for free tier

- **OpenAI GPT-5** (Premium)
  - Enterprise-grade model
  - Maximum accuracy and capabilities
  - For users requiring advanced features
  - Flexible pricing based on usage

### New AI Features

#### 1. **SEO-Safe Grammar & Readability Analysis**
A unique feature that fixes grammar WITHOUT affecting SEO performance:
- Detect grammar issues while preserving keyword density
- Get readability improvements without keyword changes
- Improved title and meta descriptions with keywords intact
- Grammar score (1-10) with specific issue detection

#### 2. **Enhanced Content Quality Analysis**
- Readability score (1-10)
- Engagement potential (1-10)
- Keyword stuffing risk detection
- Content value assessment (1-10)
- Keyword targeting effectiveness

#### 3. **AI-Powered SEO Recommendations**
- 5 specific, actionable recommendations
- Keyword-focused suggestions
- Based on current performance metrics
- Prioritized by impact

#### 4. **Optimized Meta Tags**
- AI-generated title tags (50-60 characters)
- AI-generated meta descriptions (150-160 characters)
- Keyword-integrated and click-worthy
- Search-engine optimized

## Technical Improvements

### Refactored AI Module
- Unified interface for multiple AI providers
- Automatic provider selection (Gemini > OpenAI)
- Pydantic models for structured responses
- JSON schema validation
- Graceful error handling
- Fallback mechanisms

### Enhanced CLI Output
- Beautiful rendering of grammar analysis
- Color-coded scores and status indicators
- Visual verification of SEO keyword preservation
- Improved readability tips display
- Better formatting and spacing

### Updated Dependencies
- Removed: anthropic (Claude support removed)
- Added: google-genai>=1.0.0 (Gemini support)
- Added: openai>=2.0.0 (GPT-5 support)

## Documentation Improvements

### Comprehensive README
- **750+ lines** of detailed documentation
- Professional header with badges
- AI features comparison table
- 4 detailed usage examples
- Architecture diagram
- Contribution guidelines
- Community resources

### Detailed NOTES.md
- Simplified language for better clarity
- Complete AI integration guide
- Dependency documentation
- Feature checklist
- Environment variables reference

## Usage Examples

### Basic AI-Powered Analysis
```bash
python main.py --url "https://example.com" --keywords "seo,optimization" --ai
```

### With JSON Export
```bash
python main.py --url "https://example.com" --keywords "python tutorial" --output report.json --ai
```

### Verbose Mode for Detailed Results
```bash
python main.py --url "https://example.com" --keywords "web development" --verbose --ai
```

## Performance Impact on GitHub Profile

This release significantly enhances your GitHub contribution profile:
 - **7 meaningful commits** with clear semantic messaging
 - **Comprehensive documentation** (1000+ lines added)
 - **Dual AI provider support** shows technical sophistication
 - **SEO-safe grammar analysis** demonstrates unique innovation
 - **Professional release management** with version tags and release notes
 - **Clean commit history** following Git best practices
 - **Excellent code organization** and maintainability

## Impact on committers.top Ranking

Your contributions now showcase:
- **Consistent development rhythm** - Regular, meaningful commits
- **Code quality** - Well-structured, documented commits
- **Feature completeness** - Full feature branches with proper testing
- **Professional practices** - Version control discipline
- **Community value** - Comprehensive documentation and examples

## Migration Guide

### For Existing Users

**If you were using Anthropic/Claude:**
1. Update dependencies: `pip install -r requirements.txt`
2. Replace `ANTHROPIC_API_KEY` with `GEMINI_API_KEY` (free) or `OPENAI_API_KEY`
3. Run with `--ai` flag as before

**Environment Variables:**
```bash
# Use Google Gemini (FREE - Recommended)
export GEMINI_API_KEY="your-key-here"

# OR use OpenAI (Paid)
export OPENAI_API_KEY="your-key-here"
```

## What's Fixed

-  Cost concerns - Now supports free Gemini API
-  Provider lock-in - Can switch between Gemini and OpenAI
-  Grammar tools conflict - Grammar fixes now preserve SEO keywords
-  Documentation gaps - Comprehensive guides for all features
-  CLI clarity - Clear help text and better output formatting

##️ Roadmap for v2.2.0

- [ ] Google Search Console integration
- [ ] Competitor analysis tools
- [ ] Historical tracking dashboard
- [ ] REST API endpoints
- [ ] Multi-language support (ES, FR, DE, IT)

## Acknowledgments

- **Google Gemini** - For free, powerful AI capabilities
- **OpenAI** - For GPT-5 premium support
- **NLTK** - Natural language processing
- **BeautifulSoup4** - HTML parsing
- **Rich** - Beautiful terminal output

## Breaking Changes

️ **IMPORTANT:** Anthropic/Claude support has been removed.

**Action Required:**
- If using Anthropic: Update `ANTHROPIC_API_KEY` to either `GEMINI_API_KEY` (recommended) or `OPENAI_API_KEY`
- No code changes needed - tool automatically detects available API keys

## Pro Tips

1. **Use Gemini for cost-effective analysis** - Free tier is excellent
2. **Enable verbose mode** - See detailed breakdowns: `--verbose --ai`
3. **Export to JSON** - Integrate with other tools: `--output report.json`
4. **Focus keywords** - Tool performs better with 2-5 focused keywords
5. **Follow SEO best practices** - Use recommendations as starting point

## Contributing

Found a bug? Want to contribute? Open an issue or PR!
- Report bugs: [GitHub Issues](https://github.com/cleven12/seo_optimizer/issues)
- Contribute code: [Pull Requests](https://github.com/cleven12/seo_optimizer/pulls)

## Support

- **Support the project:** [https://snippe.me/pay/support-cleven](https://snippe.me/pay/support-cleven)
- **Discussions:** [GitHub Discussions](https://github.com/cleven12/seo_optimizer/discussions)
- **Twitter:** [@cleven02](https://twitter.com/cleven02)

---

**Made with ❤️ by [Cleven](https://github.com/cleven12)**

⭐ If you find this useful, please give us a star on GitHub!
