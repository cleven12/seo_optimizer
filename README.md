# SEO Optimizer SaaS

Professional web-based SEO analysis platform built with Django, REST API, and real-time visualizations.

## Overview

**SEO Optimizer SaaS** is a production-ready web application that analyzes websites for SEO optimization. It provides:

- 🌐 **Web Interface** - Responsive UI with Tailwind CSS
- 📊 **Real-time Analytics** - Chart.js visualizations with radar charts and score breakdowns
- 🔗 **REST API** - 9+ endpoints for programmatic access
- 📄 **PDF Reports** - Professional report generation with ReportLab
- ⚡ **Fast Analysis** - Background threading for non-blocking requests
- 🎯 **Optional Keywords** - Analyze URLs with or without focus keywords
- 🤖 **AI Integration** - Optional AI-powered recommendations (Gemini/OpenAI)
- 📈 **Score Tracking** - Track historical reports and improvements

## Features

### Analysis Categories

1. **Technical SEO** - Meta tags, canonicals, headers, robots.txt, SSL
2. **Content Quality** - Keyword optimization, readability, length, freshness
3. **Structure** - Semantic HTML, schema markup, hierarchy
4. **Links** - Internal/external links, anchor text quality
5. **AI Insights** - Smart recommendations (optional)

### Web Interface

- **Analyzer Tool** - Input URL and optional keywords, get instant analysis
- **Reports Dashboard** - View, filter, and export saved reports
- **SEO Guide** - 24-section comprehensive SEO documentation
- **Admin Panel** - Django admin for monitoring

### REST API

```
POST   /api/reports/analyze/        - Start analysis
GET    /api/reports/                - List reports
GET    /api/reports/{id}/           - Get report
GET    /api/reports/{id}/details/   - Detailed analysis
POST   /api/reports/{id}/save/      - Save report
GET    /api/reports/{id}/export_pdf/ - Export PDF
GET    /api/stats/                  - Statistics
GET    /api/guide/                  - SEO guidelines
```

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Setup (1 minute)

```bash
bash quickstart.sh
cd seo_saas
python manage.py runserver
```

Open http://localhost:8000

### Manual Setup

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

cd seo_saas
python manage.py migrate
python manage.py createsuperuser  # Optional admin
python manage.py runserver
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django
DEBUG=False
SECRET_KEY=your-secure-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Analysis
USE_AI=False
GEMINI_API_KEY=optional-api-key
OPENAI_API_KEY=optional-api-key

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Django Settings

Key settings in `seo_saas/settings.py`:

```python
SEO_ANALYZER_CONFIG = {
    'timeout': 10,  # Request timeout in seconds
    'max_content_size': 10 * 1024 * 1024,  # 10MB max
    'enable_ai': False,
}
```

## Project Structure

```
seo_saas/                    # Django application
├── manage.py               # Django management
├── settings.py             # Configuration
├── urls.py                 # URL routing
├── asgi.py                 # ASGI (async)
├── wsgi.py                 # WSGI (production)
└── analyzer/               # Main app
    ├── models.py           # Database schemas
    ├── views.py            # Web & API views
    ├── serializers.py      # REST serializers
    ├── analyzer_service.py # Analysis logic
    ├── urls.py             # App URLs
    └── admin.py            # Admin panel

src/                         # Analysis core (shared)
├── analyzers/              # Analysis modules
│   ├── technical_seo.py
│   ├── content_analyzer.py
│   ├── structure_analyzer.py
│   ├── link_analyzer.py
│   └── ai_analyzer.py      # Optional
├── core/                   # Core functionality
│   ├── orchestrator.py     # Analysis orchestration
│   ├── fetcher.py          # Web content fetching
│   ├── keyword_processor.py
│   └── scoring.py
└── utils/                  # Utilities

templates/                   # Web interface
├── base.html               # Base layout
├── analyzer/
│   ├── index.html          # Home page
│   ├── analyzer.html       # Main tool
│   └── reports.html        # Reports dashboard
```

## API Examples

### Analyze a URL

```bash
curl -X POST http://localhost:8000/api/reports/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "keywords": ["seo", "optimization"]
  }'
```

Response:
```json
{
  "id": 1,
  "url": "https://example.com",
  "status": "processing",
  "overall_score": 0,
  "created_at": "2025-12-02T10:30:00Z"
}
```

### Get Report Status

```bash
curl http://localhost:8000/api/reports/1/
```

### Get Detailed Analysis

```bash
curl http://localhost:8000/api/reports/1/details/
```

### Export as PDF

```bash
curl -o report.pdf http://localhost:8000/api/reports/1/export_pdf/
```

### Save Report

```bash
curl -X POST http://localhost:8000/api/reports/1/save/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Homepage Analysis"}'
```

## Deployment

### Linux / Ubuntu

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip nginx postgresql

# Setup
pip install gunicorn
python manage.py collectstatic
python manage.py migrate

# Run with Gunicorn
gunicorn seo_saas.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Docker

```bash
docker build -t seo-optimizer .
docker run -p 8000:8000 seo-optimizer
```

### Heroku

```bash
heroku create app-name
git push heroku saas/production-v1:main
heroku run python manage.py migrate
```

See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for detailed instructions.

## Optional Features

### AI Recommendations

Enable AI-powered analysis using Google Gemini or OpenAI:

1. Set `USE_AI=True` in `.env`
2. Add API key: `GEMINI_API_KEY` or `OPENAI_API_KEY`
3. Re-analyze URLs to get AI insights

### Keyword-Based Analysis

Analyze with or without keywords:

- **With Keywords**: More focused analysis on specific terms
- **Without Keywords**: General SEO assessment based on page content

Both modes work seamlessly - the system defaults to content-based analysis if no keywords provided.

## Technology Stack

**Backend:**
- Django 4.2+ - Web framework
- Django REST Framework - REST API
- PostgreSQL/SQLite - Database
- Gunicorn - Production server

**Frontend:**
- HTML5 & Tailwind CSS - Responsive design
- Chart.js - Interactive visualizations
- Vanilla JavaScript - Real-time polling

**Analysis:**
- NLTK - Natural language processing
- BeautifulSoup - HTML parsing
- Requests - HTTP client
- ReportLab - PDF generation

**Optional:**
- Google Gemini API - AI recommendations
- OpenAI API - AI recommendations

## Monitoring & Logging

### View Logs

**Development:**
```bash
python manage.py runserver  # Logs to console
```

**Production:**
```bash
sudo journalctl -u seo-optimizer -f
tail -f logs/django.log
```

### Database Inspection

```bash
python manage.py dbshell
python manage.py shell
```

### Performance

```bash
python manage.py check --deploy  # Security checks
```

## Troubleshooting

### Issue: Port 8000 already in use
```bash
lsof -i :8000
kill -9 <PID>
```

### Issue: Database migration errors
```bash
python manage.py flush  # Reset database
python manage.py migrate
```

### Issue: Missing NLTK data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Issue: Static files not loading
```bash
python manage.py collectstatic --noinput
```

## Documentation

- [SAAS_SETUP_GUIDE.md](SAAS_SETUP_GUIDE.md) - Detailed setup instructions
- [API.md](API.md) - Complete API reference
- [FEATURE_OVERVIEW.md](FEATURE_OVERVIEW.md) - Feature documentation
- [GUIDE_DOCUMENTATION.md](GUIDE_DOCUMENTATION.md) - SEO guidelines
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Deployment steps
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Documentation hub

## Performance

- **Light URL**: < 2 seconds
- **Medium URL**: 2-5 seconds
- **Large URL**: 5-10 seconds
- **With AI**: +2-5 seconds

Concurrent analysis using background threading supports 100+ simultaneous requests.

## Security

- CSRF protection enabled
- XSS protection via template escaping
- SQL injection prevention via ORM
- CORS configured for API access
- Secure headers configured
- Password hashing for admin accounts

## Contributing

This is a production SaaS application. For modifications:

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes following Django/DRF conventions
3. Test thoroughly before deployment
4. Commit with clear messages
5. Deploy to production following checklist

## License

See [LICENSE](../LICENSE) file.

## Support

For issues, questions, or feature requests, refer to the documentation or code comments.

---

**Version:** 1.0.0  
**Last Updated:** December 2, 2025  
**Status:** Production Ready

Ready to deploy! Start with `bash quickstart.sh`
