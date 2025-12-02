"""Django models for SEO Analyzer application."""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
import json
from datetime import datetime


class AnalysisReport(models.Model):
    """Store SEO analysis reports (no user association - stateless)"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Basic Info
    url = models.URLField(validators=[URLValidator()])
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Analysis Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Scores
    overall_score = models.IntegerField(default=0)
    technical_score = models.IntegerField(default=0)
    content_score = models.IntegerField(default=0)
    structure_score = models.IntegerField(default=0)
    link_score = models.IntegerField(default=0)
    
    # Analysis Data (stored as JSON)
    analysis_data = models.JSONField(default=dict, blank=True)
    keywords = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    
    # Metadata
    analysis_time = models.FloatField(default=0)  # seconds
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.url} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def to_dict(self):
        """Convert report to dictionary for API responses"""
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'scores': {
                'overall': self.overall_score,
                'technical': self.technical_score,
                'content': self.content_score,
                'structure': self.structure_score,
                'links': self.link_score,
            },
            'keywords': self.keywords,
            'recommendations': self.recommendations[:10],  # Top 10
            'analysis_time': self.analysis_time,
        }


class AnalysisDetail(models.Model):
    """Detailed analysis results for each SEO category"""
    
    report = models.OneToOneField(AnalysisReport, on_delete=models.CASCADE, related_name='details')
    
    # Technical SEO Details
    technical_details = models.JSONField(default=dict)
    
    # Content Analysis Details
    content_details = models.JSONField(default=dict)
    
    # Structure Analysis Details
    structure_details = models.JSONField(default=dict)
    
    # Link Analysis Details
    link_details = models.JSONField(default=dict)
    
    # AI Analysis (if available)
    ai_recommendations = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Details for {self.report.url}"


class SavedReport(models.Model):
    """Save analysis reports for future reference (no user login required)"""
    
    # Report
    report = models.OneToOneField(AnalysisReport, on_delete=models.CASCADE, related_name='saved')
    
    # Reference Info
    name = models.CharField(max_length=255, help_text="Custom name for this report")
    description = models.TextField(blank=True, help_text="Optional notes about this analysis")
    
    # Session-based tracking (IP or session ID)
    session_id = models.CharField(max_length=255, blank=True, help_text="For tracking without login")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.report.url}"


class APILog(models.Model):
    """Log API requests for monitoring and debugging"""
    
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)  # GET, POST, etc.
    status_code = models.IntegerField()
    
    # Request Data
    request_data = models.JSONField(blank=True, null=True)
    response_time = models.FloatField()  # milliseconds
    
    # Client Info
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['endpoint']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code}"
