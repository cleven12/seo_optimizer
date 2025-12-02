"""Django app configuration."""

from django.apps import AppConfig


class AnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seo_saas.analyzer'
    verbose_name = 'SEO Analyzer'
