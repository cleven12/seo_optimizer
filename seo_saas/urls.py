"""Main URL configuration for seo_saas project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from seo_saas.analyzer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('seo_saas.analyzer.urls')),
    path('', views.IndexView.as_view(), name='index'),
    path('analyzer/', views.AnalyzerView.as_view(), name='analyzer'),
    path('reports/', views.ReportListView.as_view(), name='reports'),
    path('guide/', views.GuideView.as_view(), name='guide'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
