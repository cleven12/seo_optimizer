# SEO Optimizer - SaaS Application Setup Guide

## Overview

SEO Optimizer has been transformed into a Django-based SaaS (Software as a Service) application. This guide covers installation, configuration, and deployment.

## Table of Contents

1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [API Documentation](#api-documentation)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## Features

### Core Capabilities

- ✅ **Web-Based Interface** - Modern, responsive UI built with Tailwind CSS
- ✅ **Real-time Analysis** - Background processing with status polling
- ✅ **No Authentication Required** - Session-based report tracking
- ✅ **No Data Storage** - Stateless analysis (reports stored in DB but no personal data)
- ✅ **PDF Export** - Download professional analysis reports
- ✅ **Chart Visualizations** - Interactive charts with Chart.js
- ✅ **REST API** - Complete API for programmatic access
- ✅ **AI Recommendations** (Optional) - Gemini or OpenAI integration
- ✅ **Multiple Analysis Categories** - Technical, Content, Structure, Links
- ✅ **Google Search Guidelines** - Aligned with official SEO best practices

### Analysis Modules

1. **Technical SEO** (25% weight)
   - Title tag optimization
   - Meta description quality
   - Header tag hierarchy
   - Canonical tags
   - Open Graph tags
   - HTTPS/Security

2. **Content Quality** (35% weight)
   - Keyword optimization
   - Word count and depth
   - Content freshness
   - User intent alignment
   - Unique content detection

3. **Structure & Markup** (20% weight)
   - Semantic HTML validation
   - Schema markup detection
   - Heading hierarchy
   - Accessibility features

4. **Link Quality** (20% weight)
   - Internal linking strategy
   - External link quality
   - Anchor text analysis
   - Broken link detection

---

## System Requirements

### Minimum

- **Python 3.9+**
- **RAM**: 512MB
- **Disk Space**: 1GB
- **Database**: SQLite (included) or PostgreSQL (recommended for production)

### Recommended

- **Python 3.11+**
- **RAM**: 2GB+
- **Disk Space**: 5GB+
- **OS**: Linux, macOS, or Windows with WSL2

---

## Installation

### 1. Clone and Setup Virtual Environment

```bash
# Navigate to project
cd /path/to/seo_optimizer

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Download NLTK data (required for keyword processing)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 3. Database Setup

```bash
# Navigate to Django project
cd seo_saas

# Run migrations
python manage.py migrate

# Create superuser (for admin access)
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic --noinput
```

### 4. Configure Environment Variables

Create `.env` file in project root:

```bash
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# AI Configuration (Optional)
USE_AI=False
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key

# Database (Optional for production)
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

---

## Configuration

### Django Settings

Key settings in `seo_saas/settings.py`:

```python
# Debug Mode
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Allowed Hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# AI Configuration
AI_CONFIG = {
    'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
    'USE_AI': os.getenv('USE_AI', 'False') == 'True',
}

# Analyzer Configuration
SEO_ANALYZER_CONFIG = {
    'MAX_CONTENT_SIZE': 5242880,  # 5MB
    'TIMEOUT': 15,  # seconds
}
```

### Database Configuration

**Development (SQLite - default):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL recommended):**
```bash
# Install psycopg2
pip install psycopg2-binary

# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seo_optimizer',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Running the Application

### Development Server

```bash
cd seo_saas

# Run Django development server
python manage.py runserver

# Access at: http://localhost:8000
```

### Production Server

```bash
# Using Gunicorn (recommended)
pip install gunicorn

# Run with Gunicorn
gunicorn seo_saas.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2 \
    --worker-class gthread
```

### With Nginx (Recommended for Production)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 5M;

    location /static/ {
        alias /path/to/seo_optimizer/seo_saas/staticfiles/;
    }

    location /media/ {
        alias /path/to/seo_optimizer/seo_saas/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

---

## API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Authentication

- Currently **no authentication required**
- Session-based tracking via `session_id`
- For future subscription features: Token-based authentication

### Endpoints

#### 1. Analyze Website

**POST** `/api/reports/analyze/`

Request:
```json
{
    "url": "https://example.com",
    "keywords": ["seo", "optimization"],
    "include_ai": false
}
```

Response:
```json
{
    "id": 1,
    "url": "https://example.com",
    "status": "pending",
    "overall_score": 0,
    "created_at": "2024-12-02T10:30:00Z",
    "analysis_time": 0.0
}
```

#### 2. Get Report

**GET** `/api/reports/{id}/`

Response:
```json
{
    "id": 1,
    "url": "https://example.com",
    "title": "Example Website",
    "status": "completed",
    "overall_score": 75,
    "scores": {
        "overall": 75,
        "technical": 80,
        "content": 70,
        "structure": 75,
        "links": 70
    },
    "keywords": [...],
    "recommendations": [...],
    "created_at": "2024-12-02T10:30:00Z"
}
```

#### 3. Get Report Details

**GET** `/api/reports/{id}/details/`

Returns detailed analysis for each category.

#### 4. Save Report

**POST** `/api/reports/{id}/save/`

Request:
```json
{
    "name": "My First Analysis",
    "description": "Website analysis for SEO optimization"
}
```

#### 5. Export as PDF

**GET** `/api/reports/{id}/export_pdf/`

Returns PDF file download.

#### 6. List Saved Reports

**GET** `/api/saved/`

Returns paginated list of saved reports for current session.

#### 7. Get Statistics

**GET** `/api/stats/`

Returns aggregated analytics:
```json
{
    "total_analyses": 150,
    "completed_analyses": 145,
    "average_score": 72.5,
    "recent_analyses": [...]
}
```

#### 8. SEO Guide

**GET** `/api/guide/`

Returns full SEO Guidelines documentation as JSON.

### Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Web Interface

### Pages

1. **Home** (`/`) - Overview and statistics
2. **Analyzer** (`/analyzer/`) - Main analysis tool
3. **Reports** (`/reports/`) - View saved reports
4. **Guide** (`/guide/`) - SEO guidelines documentation

### Features

- Real-time analysis with loading indicator
- Interactive score visualization with Chart.js
- Radar chart showing SEO profile
- Save reports with custom names
- Export reports as PDF
- Responsive design (mobile-friendly)

---

## Deployment

### Heroku Deployment

```bash
# Create Procfile
echo "web: gunicorn seo_saas.wsgi --log-file -" > Procfile

# Create runtime.txt
echo "python-3.11.7" > runtime.txt

# Initialize git and push
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python seo_saas/manage.py collectstatic --noinput

CMD ["gunicorn", "seo_saas.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:

```bash
docker build -t seo-optimizer .
docker run -p 8000:8000 seo-optimizer
```

### AWS Deployment

```bash
# Using Elastic Beanstalk
eb init
eb create seo-optimizer-env
eb deploy
```

---

## Troubleshooting

### Common Issues

#### 1. Module Import Errors

```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Database Migration Errors

```bash
# Reset database (development only)
python manage.py flush
python manage.py migrate

# Or check migration status
python manage.py showmigrations
```

#### 3. Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# In DEBUG=False, serve with whitenoise or Nginx
pip install whitenoise
```

#### 4. Analysis Timeout

```python
# Increase timeout in settings.py
SEO_ANALYZER_CONFIG = {
    'TIMEOUT': 30,  # Increase from 15 to 30 seconds
}
```

#### 5. NLTK Data Missing

```bash
# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Performance Optimization

1. **Enable Caching**
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       }
   }
   ```

2. **Database Indexing**
   - Already configured in models
   - Add custom indexes as needed

3. **API Pagination**
   ```python
   REST_FRAMEWORK = {
       'PAGE_SIZE': 10,
   }
   ```

4. **Async Analysis**
   - Implemented with threading
   - Can upgrade to Celery for larger scale

---

## Future Enhancements

### Planned Features

- [ ] User Authentication & Accounts
- [ ] Subscription Plans (Free, Pro, Enterprise)
- [ ] Scheduled Analysis & Monitoring
- [ ] Competitor Comparison
- [ ] Historical Tracking Dashboard
- [ ] API Rate Limiting
- [ ] Advanced Filtering & Search
- [ ] Batch URL Analysis
- [ ] Browser Extension
- [ ] WordPress Plugin Integration
- [ ] Google Search Console Integration
- [ ] Email Notifications
- [ ] Mobile App

---

## Support & Documentation

- **SEO Guide**: `/guide/` - Comprehensive SEO best practices
- **API Docs**: `/api/` - Interactive API browser
- **Admin Panel**: `/admin/` - Django admin interface
- **Issues**: Report bugs on GitHub

---

## License

MIT License - See LICENSE file for details

---

**Last Updated**: December 2, 2024
**Version**: 1.0.0 - SaaS Release
