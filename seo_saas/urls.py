"""Main URL configuration for seo_saas project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from seo_saas.analyzer import views

# Create router for API viewsets
router = DefaultRouter()
router.register(r'reports', views.AnalysisReportViewSet, basename='report')
router.register(r'saved', views.SavedReportViewSet, basename='saved-report')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Web interface routes
    path('', views.IndexView.as_view(), name='index'),
    path('analyzer/', views.AnalyzerView.as_view(), name='analyzer'),
    path('reports/', views.ReportListView.as_view(), name='reports'),
    path('guide/', views.GuideView.as_view(), name='guide'),
    
    # API routes
    path('api/', include(router.urls)),
    path('api/guide/', views.guide_api, name='api-guide'),
    path('api/stats/', views.stats_api, name='api-stats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
