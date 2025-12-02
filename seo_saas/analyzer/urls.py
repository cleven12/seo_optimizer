"""URL routing for analyzer app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for viewsets
router = DefaultRouter()
router.register(r'reports', views.AnalysisReportViewSet, basename='report')
router.register(r'saved', views.SavedReportViewSet, basename='saved-report')

app_name = 'analyzer'

urlpatterns = [
    # Web interface routes
    path('', views.IndexView.as_view(), name='index'),
    path('analyzer/', views.AnalyzerView.as_view(), name='analyzer'),
    path('reports/', views.ReportListView.as_view(), name='reports'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
    path('guide/', views.GuideView.as_view(), name='guide'),
    
    # API routes
    path('api/', include(router.urls)),
    path('api/guide/', views.guide_api, name='api-guide'),
    path('api/stats/', views.stats_api, name='api-stats'),
]
