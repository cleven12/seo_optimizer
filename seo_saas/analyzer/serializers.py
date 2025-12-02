"""Serializers for REST API."""

from rest_framework import serializers
from .models import AnalysisReport, AnalysisDetail, SavedReport


class AnalysisReportSerializer(serializers.ModelSerializer):
    """Serializer for AnalysisReport model"""
    
    scores = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalysisReport
        fields = [
            'id', 'url', 'title', 'status', 'overall_score', 
            'scores', 'keywords', 'recommendations', 'created_at', 
            'analysis_time'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_scores(self, obj):
        """Return all scores in a nested structure"""
        return {
            'overall': obj.overall_score,
            'technical': obj.technical_score,
            'content': obj.content_score,
            'structure': obj.structure_score,
            'links': obj.link_score,
        }


class AnalysisDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed analysis results"""
    
    report = AnalysisReportSerializer(read_only=True)
    
    class Meta:
        model = AnalysisDetail
        fields = [
            'id', 'report', 'technical_details', 'content_details',
            'structure_details', 'link_details', 'ai_recommendations',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SavedReportSerializer(serializers.ModelSerializer):
    """Serializer for SavedReport model"""
    
    report = AnalysisReportSerializer(read_only=True)
    
    class Meta:
        model = SavedReport
        fields = ['id', 'report', 'name', 'description', 'tags', 'created_at']
        read_only_fields = ['id', 'created_at']


class AnalysisRequestSerializer(serializers.Serializer):
    """Serializer for analysis requests"""
    
    url = serializers.URLField(required=True, help_text="URL to analyze")
    keywords = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Optional keywords for analysis"
    )
    include_ai = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Include AI recommendations (if available)"
    )
    
    def validate_url(self, value):
        """Validate URL format"""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("URL must start with http:// or https://")
        return value
    
    def validate_keywords(self, value):
        """Validate keywords list"""
        if value and len(value) > 10:
            raise serializers.ValidationError("Maximum 10 keywords allowed")
        return value
