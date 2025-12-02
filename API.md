# SEO Optimizer API Documentation

Complete REST API reference for the SEO Optimizer SaaS application.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

Currently, the API does **not require authentication**. Session-based tracking uses `session_id` for report association.

### Future Authentication
- Token-based authentication (coming in v2.0)
- OAuth2 integration (planned)
- API key authentication (planned)

---

## Content Type

All requests and responses use `application/json`.

---

## Error Handling

### Standard Error Response

```json
{
    "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Internal error |

---

## Endpoints

### 1. Analyze Website

Initiate a new SEO analysis for a URL.

**Endpoint:**
```
POST /api/reports/analyze/
```

**Request Body:**
```json
{
    "url": "https://example.com",
    "keywords": ["optional", "keywords"],
    "include_ai": false
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | Full URL including https:// |
| `keywords` | array | No | List of keywords to analyze (max 10) |
| `include_ai` | boolean | No | Enable AI recommendations (default: false) |

**Response (201 Created):**
```json
{
    "id": 1,
    "url": "https://example.com",
    "title": null,
    "status": "pending",
    "overall_score": 0,
    "scores": {
        "overall": 0,
        "technical": 0,
        "content": 0,
        "structure": 0,
        "links": 0
    },
    "keywords": [],
    "recommendations": [],
    "created_at": "2024-12-02T10:30:00Z",
    "analysis_time": 0.0
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/reports/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "keywords": ["seo", "optimization"],
    "include_ai": false
  }'
```

**Status Values:**
- `pending` - Analysis in progress
- `completed` - Analysis finished successfully
- `failed` - Analysis encountered an error

---

### 2. Get Report

Retrieve analysis results for a specific report.

**Endpoint:**
```
GET /api/reports/{id}/
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Report ID |

**Response (200 OK):**
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
    "keywords": [
        {
            "keyword": "seo",
            "score": 85,
            "cluster": "primary"
        }
    ],
    "recommendations": [
        "Improve meta description length to 150-160 characters",
        "Add more relevant keywords to content"
    ],
    "created_at": "2024-12-02T10:30:00Z",
    "analysis_time": 8.5
}
```

**Example:**
```bash
curl http://localhost:8000/api/reports/1/
```

---

### 3. Get Detailed Analysis

Retrieve comprehensive analysis details for each category.

**Endpoint:**
```
GET /api/reports/{id}/details/
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Report ID |

**Response (200 OK):**
```json
{
    "id": 1,
    "report": {
        "id": 1,
        "url": "https://example.com",
        "title": "Example Website",
        ...
    },
    "technical_details": {
        "score": 80,
        "status": "good",
        "details": {
            "title": "50 characters - Good length",
            "meta_description": "Present - 155 characters",
            "h1_tags": "Single H1 - Optimal",
            "canonical": "Present - Correct"
        },
        "recommendations": [
            "Improve H1 tag relevance"
        ]
    },
    "content_details": {
        "score": 70,
        "status": "fair",
        "details": {
            "word_count": 1200,
            "keyword_density": 1.8,
            "keyword_placement": "Good"
        },
        "recommendations": [
            "Increase content depth to 1500+ words"
        ]
    },
    "structure_details": {
        "score": 75,
        "status": "good",
        "details": {
            "semantic_html": "Good",
            "header_hierarchy": "Proper",
            "schema_markup": "Not present"
        },
        "recommendations": [
            "Add schema markup for better SERP features"
        ]
    },
    "link_details": {
        "score": 70,
        "status": "fair",
        "details": {
            "internal_links": 45,
            "external_links": 12,
            "broken_links": 0
        },
        "recommendations": [
            "Add more relevant internal links"
        ]
    },
    "ai_recommendations": [
        "AI recommendation 1",
        "AI recommendation 2"
    ],
    "created_at": "2024-12-02T10:30:00Z",
    "updated_at": "2024-12-02T10:30:00Z"
}
```

**Example:**
```bash
curl http://localhost:8000/api/reports/1/details/
```

---

### 4. Save Report

Save an analysis report with a custom name and description.

**Endpoint:**
```
POST /api/reports/{id}/save/
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Report ID |
| `name` | string | No | Custom name for report |
| `description` | string | No | Description/notes |

**Request Body:**
```json
{
    "name": "Example.com - Q4 Analysis",
    "description": "Quarterly SEO audit for website optimization"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "report": {
        "id": 1,
        ...
    },
    "name": "Example.com - Q4 Analysis",
    "description": "Quarterly SEO audit for website optimization",
    "tags": [],
    "created_at": "2024-12-02T10:35:00Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/reports/1/save/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Analysis",
    "description": "Website optimization report"
  }'
```

---

### 5. Export as PDF

Download analysis report as a professionally formatted PDF.

**Endpoint:**
```
GET /api/reports/{id}/export_pdf/
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Report ID |

**Response:**
- PDF file download
- Content-Type: `application/pdf`
- Filename: `{domain}-report.pdf`

**Example:**
```bash
curl -o report.pdf http://localhost:8000/api/reports/1/export_pdf/
```

---

### 6. List Reports

Retrieve all analysis reports (paginated).

**Endpoint:**
```
GET /api/reports/
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number (default: 1) |
| `status` | string | Filter by status: `pending`, `completed`, `failed` |
| `url` | string | Filter by URL |
| `ordering` | string | Sort by field: `created_at`, `overall_score` |

**Response (200 OK):**
```json
{
    "count": 150,
    "next": "http://localhost:8000/api/reports/?page=2",
    "previous": null,
    "results": [
        {
            "id": 5,
            "url": "https://example.com",
            "status": "completed",
            "overall_score": 82,
            ...
        },
        ...
    ]
}
```

**Example:**
```bash
# Get first page
curl http://localhost:8000/api/reports/

# Get completed reports
curl http://localhost:8000/api/reports/?status=completed

# Sort by score
curl http://localhost:8000/api/reports/?ordering=-overall_score
```

---

### 7. List Saved Reports

Retrieve saved reports for current session.

**Endpoint:**
```
GET /api/saved/
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number (default: 1) |
| `ordering` | string | Sort by: `created_at`, `name` |

**Response (200 OK):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "report": {
                "id": 1,
                ...
            },
            "name": "Example.com Analysis",
            "description": "Q4 audit",
            "tags": ["q4", "priority"],
            "created_at": "2024-12-02T10:35:00Z"
        },
        ...
    ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/saved/
```

---

### 8. Get Statistics

Retrieve aggregated analytics and statistics.

**Endpoint:**
```
GET /api/stats/
```

**Response (200 OK):**
```json
{
    "total_analyses": 150,
    "completed_analyses": 145,
    "average_score": 72.5,
    "recent_analyses": [
        {
            "id": 10,
            "url": "https://example.com",
            "overall_score": 85,
            "created_at": "2024-12-02T10:30:00Z"
        },
        ...
    ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/stats/
```

---

### 9. Get SEO Guide

Retrieve comprehensive SEO guidelines and documentation.

**Endpoint:**
```
GET /api/guide/
```

**Response (200 OK):**
```json
{
    "success": true,
    "content": "# SEO Optimizer Guide...",
    "title": "SEO Optimizer Guide - Google Search Essential Techniques"
}
```

**Example:**
```bash
curl http://localhost:8000/api/guide/
```

---

## Common Use Cases

### Use Case 1: Analyze a Website and Get Results

```bash
# Step 1: Start analysis
REPORT_ID=$(curl -s -X POST http://localhost:8000/api/reports/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' | jq '.id')

# Step 2: Poll for results (with simple sleep)
sleep 10

# Step 3: Retrieve results
curl http://localhost:8000/api/reports/$REPORT_ID/

# Step 4: Get detailed analysis
curl http://localhost:8000/api/reports/$REPORT_ID/details/

# Step 5: Export as PDF
curl -o report.pdf http://localhost:8000/api/reports/$REPORT_ID/export_pdf/
```

### Use Case 2: Analyze with Keywords

```bash
curl -X POST http://localhost:8000/api/reports/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "keywords": ["python tutorial", "learn python", "python guide"],
    "include_ai": false
  }'
```

### Use Case 3: Save and Retrieve Report

```bash
# Save report with name
curl -X POST http://localhost:8000/api/reports/1/save/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Q4 2024 Analysis", "description": "Quarterly review"}'

# List all saved reports
curl http://localhost:8000/api/saved/
```

### Use Case 4: Batch Analysis with Filtering

```bash
# Get all completed analyses
curl http://localhost:8000/api/reports/?status=completed

# Sort by score (highest first)
curl http://localhost:8000/api/reports/?ordering=-overall_score

# Filter by URL pattern
curl "http://localhost:8000/api/reports/?url=example.com"
```

---

## Rate Limiting

Currently, rate limiting is **not implemented** but will be added in future versions.

**Future Plan:**
- 100 requests per minute (free tier)
- 1000 requests per minute (pro tier)
- Unlimited (enterprise tier)

---

## Pagination

List endpoints use pagination with default page size of 10.

```json
{
    "count": 150,
    "next": "http://localhost:8000/api/reports/?page=2",
    "previous": null,
    "results": [...]
}
```

**Access specific page:**
```bash
curl http://localhost:8000/api/reports/?page=2
```

---

## Filtering & Ordering

### Filtering

Available filters vary by endpoint:

```bash
# Filter by status
/api/reports/?status=completed

# Filter by URL
/api/reports/?url=example.com
```

### Ordering

Use `ordering` parameter to sort results:

```bash
# Newest first (default)
/api/reports/?ordering=-created_at

# Oldest first
/api/reports/?ordering=created_at

# Highest score first
/api/reports/?ordering=-overall_score

# Lowest score first
/api/reports/?ordering=overall_score
```

---

## Webhooks

**Coming in v2.0** - Webhooks for:
- Analysis completion
- Report saved
- Errors/failures
- Scheduled monitoring

---

## SDK & Client Libraries

### JavaScript/TypeScript
```javascript
// Coming soon
import { SEOOptimizer } from 'seo-optimizer-sdk';

const client = new SEOOptimizer();
const report = await client.analyze('https://example.com');
```

### Python
```python
# Coming soon
from seo_optimizer import SEOOptimizer

client = SEOOptimizer()
report = client.analyze('https://example.com')
```

---

## Migration from CLI

If migrating from the CLI tool:

```bash
# Old CLI command
python main.py --url "https://example.com" --keywords "seo,optimization"

# New API equivalent
curl -X POST http://localhost:8000/api/reports/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "keywords": ["seo", "optimization"]
  }'
```

---

## Changelog

### v1.0.0 (Current)
- ✅ Core endpoints
- ✅ Session-based tracking
- ✅ PDF export
- ✅ Statistics
- ✅ Guide endpoint

### v2.0 (Planned)
- [ ] Authentication
- [ ] API keys
- [ ] Webhooks
- [ ] Rate limiting
- [ ] Batch operations
- [ ] Scheduled analysis
- [ ] Client SDKs

---

## Support

For API issues or questions:
1. Check [Troubleshooting](./SAAS_SETUP_GUIDE.md#troubleshooting)
2. Review [SEO Guidelines](./GUIDE_DOCUMENTATION.md)
3. Open an issue on GitHub
4. Contact support

---

**Last Updated**: December 2, 2024
**API Version**: 1.0.0
**Status**: Production Ready
