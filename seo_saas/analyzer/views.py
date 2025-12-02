"""Views for SEO Analyzer application."""

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import json
import time
from datetime import datetime
import threading

from .models import AnalysisReport, AnalysisDetail, SavedReport
from .serializers import (
    AnalysisReportSerializer, AnalysisDetailSerializer,
    SavedReportSerializer, AnalysisRequestSerializer
)
from .analyzer_service import run_seo_analysis, generate_pdf_report


class IndexView(TemplateView):
    """Home page view"""
    template_name = 'analyzer/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_analyses'] = AnalysisReport.objects.count()
        context['recent_analyses'] = AnalysisReport.objects.filter(
            status='completed'
        ).order_by('-created_at')[:5]
        return context


class AnalyzerView(TemplateView):
    """Main analyzer interface"""
    template_name = 'analyzer/analyzer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guide_url'] = '/api/guide/'
        return context


class ReportListView(ListView):
    """List of saved reports"""
    model = SavedReport
    template_name = 'analyzer/reports.html'
    context_object_name = 'reports'
    paginate_by = 10
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """Get reports, optionally filtered by session"""
        session_id = self.request.session.session_key
        queryset = SavedReport.objects.all().order_by('-created_at')
        
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        
        return queryset


class ReportDetailView(DetailView):
    """View detailed report"""
    model = SavedReport
    template_name = 'analyzer/report_detail.html'
    context_object_name = 'report'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'details'):
            context['details'] = self.object.details
        return context


class GuideView(TemplateView):
    """SEO Guidelines documentation view"""
    template_name = 'analyzer/guide.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open('GUIDE_DOCUMENTATION.md', 'r') as f:
            context['guide_content'] = f.read()
        return context


# ==================== REST API VIEWS ====================

class AnalysisReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for analysis reports
    
    - list: Get all reports
    - create: Create new analysis
    - retrieve: Get specific report
    - analyze: Run new analysis
    """
    
    queryset = AnalysisReport.objects.all()
    serializer_class = AnalysisReportSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['status', 'url']
    ordering_fields = ['created_at', 'overall_score']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def analyze(self, request):
        """
        Analyze a URL for SEO
        
        POST /api/reports/analyze/
        {
            "url": "https://example.com",
            "keywords": ["optional", "keywords"],
            "include_ai": false
        }
        """
        serializer = AnalysisRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        url = serializer.validated_data['url']
        keywords = serializer.validated_data.get('keywords', [])
        include_ai = serializer.validated_data.get('include_ai', False)
        
        # Create report
        report = AnalysisReport.objects.create(
            url=url,
            status='pending',
            keywords=keywords
        )
        
        # Run analysis in background thread to avoid timeout
        thread = threading.Thread(
            target=self._run_analysis,
            args=(report.id, keywords, include_ai)
        )
        thread.daemon = True
        thread.start()
        
        return Response(
            AnalysisReportSerializer(report).data,
            status=status.HTTP_201_CREATED
        )
    
    @staticmethod
    def _run_analysis(report_id, keywords, include_ai):
        """Run analysis in background"""
        try:
            report = AnalysisReport.objects.get(id=report_id)
            start_time = time.time()
            
            # Run the actual analysis
            analysis_result = run_seo_analysis(
                report.url,
                keywords,
                include_ai
            )
            
            # Update report with results
            report.status = 'completed'
            report.overall_score = analysis_result['overall_score']
            report.technical_score = analysis_result['scores'].get('technical', 0)
            report.content_score = analysis_result['scores'].get('content', 0)
            report.structure_score = analysis_result['scores'].get('structure', 0)
            report.link_score = analysis_result['scores'].get('links', 0)
            report.title = analysis_result.get('title', '')
            report.analysis_data = analysis_result.get('analysis_data', {})
            report.recommendations = analysis_result.get('recommendations', [])
            report.analysis_time = time.time() - start_time
            report.save()
            
            # Create details
            AnalysisDetail.objects.create(
                report=report,
                technical_details=analysis_result.get('technical_details', {}),
                content_details=analysis_result.get('content_details', {}),
                structure_details=analysis_result.get('structure_details', {}),
                link_details=analysis_result.get('link_details', {}),
                ai_recommendations=analysis_result.get('ai_recommendations', []),
            )
        
        except Exception as e:
            report = AnalysisReport.objects.get(id=report_id)
            report.status = 'failed'
            report.error_message = str(e)
            report.save()
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Get detailed analysis results"""
        report = self.get_object()
        
        try:
            details = report.details
            serializer = AnalysisDetailSerializer(details)
            return Response(serializer.data)
        except AnalysisDetail.DoesNotExist:
            return Response(
                {'error': 'Analysis details not yet available'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def save(self, request, pk=None):
        """Save report with custom name"""
        report = self.get_object()
        name = request.data.get('name', report.url)
        description = request.data.get('description', '')
        
        saved_report = SavedReport.objects.create(
            report=report,
            name=name,
            description=description,
            session_id=request.session.session_key or 'anonymous'
        )
        
        return Response(
            SavedReportSerializer(saved_report).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        """Export report as PDF"""
        report = self.get_object()
        
        if report.status != 'completed':
            return Response(
                {'error': 'Analysis not completed yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            pdf_content = generate_pdf_report(report)
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{report.url.split("/")[-1]}-report.pdf"'
            return response
        except Exception as e:
            return Response(
                {'error': f'PDF generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SavedReportViewSet(viewsets.ModelViewSet):
    """API endpoints for saved reports"""
    
    queryset = SavedReport.objects.all()
    serializer_class = SavedReportSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['created_at']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter reports by session"""
        session_id = self.request.session.session_key
        if session_id:
            return SavedReport.objects.filter(session_id=session_id)
        return SavedReport.objects.none()
    
    def perform_create(self, serializer):
        """Associate report with session"""
        serializer.save(session_id=self.request.session.session_key or 'anonymous')


@require_http_methods(["GET"])
def guide_api(request):
    """Serve SEO guide as JSON"""
    try:
        with open('GUIDE_DOCUMENTATION.md', 'r') as f:
            guide_content = f.read()
        
        return JsonResponse({
            'success': True,
            'content': guide_content,
            'title': 'SEO Optimizer Guide - Google Search Essential Techniques'
        })
    except FileNotFoundError:
        return JsonResponse({
            'success': False,
            'error': 'Guide not found'
        }, status=404)


@require_http_methods(["GET"])
def stats_api(request):
    """Serve general statistics"""
    return JsonResponse({
        'total_analyses': AnalysisReport.objects.count(),
        'completed_analyses': AnalysisReport.objects.filter(status='completed').count(),
        'average_score': AnalysisReport.objects.filter(
            status='completed'
        ).aggregate(avg_score=models.Avg('overall_score')).get('avg_score') or 0,
        'recent_analyses': list(
            AnalysisReport.objects.filter(status='completed').values(
                'id', 'url', 'overall_score', 'created_at'
            ).order_by('-created_at')[:10]
        )
    })
