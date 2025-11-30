# Contributing to SEO Optimizer

Thank you for your interest in contributing! This guide will help you get started.

## 🎯 Getting Started

### Prerequisites
- Python 3.8+
- Git
- pip (Python package manager)

### Setup Development Environment

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

## 🚀 Making Changes

### Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance

### Example Commit Message

```
feat: add support for additional ai models

- Add support for Anthropic Claude models
- Add fallback mechanism for model failures
- Update documentation with new model options

Closes #123
```

## 🔄 Collaboration

### Pair Programming

For pair programming sessions, use the Co-authored-by trailer:

```bash
git commit -m "feat: add new feature

Co-authored-by: Name <email@example.com>"
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Commit with clear messages
5. Push to your fork
6. Create a Pull Request

## 📝 Code Style

- Use PEP 8 for Python code
- Keep functions small and focused
- Add docstrings for all functions
- Write meaningful variable names

## 🧪 Testing

Before submitting a PR:

```bash
# Run tests
pytest

# Check code quality
flake8 src/
black --check src/
```

## 📚 Documentation

- Update README.md for user-facing changes
- Update NOTES.md for technical changes
- Add docstrings to new functions
- Include examples in documentation

## 🎉 Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- GitHub contributors page
- Release notes

## ❓ Questions?

- Open an issue for bugs
- Start a discussion for ideas
- Check existing issues first

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making SEO Optimizer better! 🙏**
