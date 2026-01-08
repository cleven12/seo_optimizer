# Contributing to SEO Analyzer

First off, thank you for considering contributing to SEO Analyzer! It's people like you that make SEO Analyzer such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, URLs, screenshots)
- **Describe the behavior you observed** and what you expected
- **Include your environment details** (OS, Python version, dependencies)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful** to most users
- **List any similar features** in other tools if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** (PEP 8 for Python)
3. **Write clear commit messages** following conventional commits
4. **Add tests** for any new functionality
5. **Update documentation** as needed
6. **Ensure all tests pass** before submitting

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip and virtualenv
- Git

### Setup Instructions

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/seo_optimizer.git
cd seo_optimizer

# Add upstream remote
git remote add upstream https://github.com/cleven12/seo_optimizer.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py
```

### Code Style

We follow PEP 8 with some modifications:

```bash
# Format code with black
black src/ tests/

# Check with flake8
flake8 src/ tests/

# Type checking with mypy (optional)
mypy src/
```

## Project Structure

```
seo_optimizer/
├── src/
│   ├── analyzers/       # Analysis modules
│   ├── core/           # Core functionality
│   ├── utils/          # Utility functions
│   └── config.py       # Configuration
├── tests/              # Test files
├── examples/           # Usage examples
├── docs/               # Documentation
└── main.py            # CLI entry point
```

## Coding Guidelines

### Python Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Write docstrings for all public functions and classes
- Keep functions focused and small (< 50 lines ideally)
- Use type hints where applicable

### Example Function

```python
def analyze_keyword_density(
    content: str,
    keyword: str,
    min_density: float = 1.0,
    max_density: float = 3.0
) -> dict:
    """
    Analyze keyword density in content.
    
    Args:
        content: The text content to analyze
        keyword: The target keyword to search for
        min_density: Minimum optimal density (default: 1.0%)
        max_density: Maximum optimal density (default: 3.0%)
    
    Returns:
        Dictionary containing density metrics and status
    
    Example:
        >>> analyze_keyword_density("Python is great. Python rocks!", "python")
        {'density': 2.5, 'count': 2, 'optimal': True}
    """
    # Implementation here
    pass
```

### Commit Message Format

We use Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(analyzer): add meta description length validation
fix(keyword): resolve stemming issue with plural forms
docs(readme): update installation instructions
test(core): add unit tests for keyword processor
```

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Aim for high code coverage (>80%)
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies (API calls, web requests)

### Test Example

```python
import pytest
from src.analyzers.keyword_analyzer import KeywordAnalyzer

class TestKeywordAnalyzer:
    def test_keyword_in_title_returns_true(self):
        """Test that keyword detection in title works correctly."""
        analyzer = KeywordAnalyzer()
        result = analyzer.check_keyword_in_title(
            title="Learn Python Programming",
            keyword="python"
        )
        assert result is True
    
    def test_keyword_not_in_title_returns_false(self):
        """Test that missing keyword is correctly detected."""
        analyzer = KeywordAnalyzer()
        result = analyzer.check_keyword_in_title(
            title="Learn Java Programming",
            keyword="python"
        )
        assert result is False
```

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use Google-style or NumPy-style docstrings
- Include examples in docstrings when helpful
- Keep documentation up-to-date with code changes

### User Documentation

- Update README.md for user-facing changes
- Add examples to the examples/ directory
- Update RELEASE_NOTES.md with changes
- Create detailed documentation in docs/ for complex features

## Feature Development Workflow

1. **Discuss First** - Open an issue to discuss major changes
2. **Create Branch** - Use descriptive branch names: `feature/add-backlink-analyzer`
3. **Implement** - Write code following our guidelines
4. **Test** - Add comprehensive tests
5. **Document** - Update relevant documentation
6. **Submit PR** - Create a pull request with clear description

## AI Features Development

When adding or modifying AI features:

- Ensure both Gemini and OpenAI implementations work
- Add proper error handling for API failures
- Include API rate limiting considerations
- Test with both free and paid API tiers
- Document API requirements clearly

## Performance Considerations

- Profile code for performance bottlenecks
- Avoid unnecessary web requests
- Cache results when appropriate
- Consider memory usage for large content
- Optimize regex patterns and string operations

## Security Guidelines

- Never commit API keys or secrets
- Validate and sanitize all user inputs
- Use environment variables for sensitive data
- Be cautious with eval() and exec()
- Review dependencies for vulnerabilities

## Getting Help

- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Join our Discord community
- Email maintainers for urgent issues

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in relevant documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Quick Contribution Checklist

Before submitting your PR, ensure:

- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass (`pytest`)
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventional commits
- [ ] Branch is up-to-date with main
- [ ] No merge conflicts
- [ ] API keys and secrets not included
- [ ] PR description is clear and detailed

---

Thank you for contributing to SEO Analyzer! 🚀

**Questions?** Open an issue or reach out to [@cleven12](https://github.com/cleven12)
