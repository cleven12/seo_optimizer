"""Admin interface for analyzer app."""

from django.contrib import admin
from .models import AnalysisReport, AnalysisDetail, SavedReport, APILog


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = ['url', 'status', 'overall_score', 'created_at', 'analysis_time']
    list_filter = ['status', 'created_at']
    search_fields = ['url', 'title']
    readonly_fields = ['created_at', 'analysis_time']
    
    fieldsets = (
        ('Analysis Info', {
            'fields': ('url', 'title', 'status', 'created_at')
        }),
        ('Scores', {
            'fields': ('overall_score', 'technical_score', 'content_score', 'structure_score', 'link_score')
        }),
        ('Results', {
            'fields': ('keywords', 'recommendations', 'analysis_data'),
            'classes': ('collapse',)
        }),
        ('Details', {
            'fields': ('analysis_time', 'error_message'),
        }),
    )


@admin.register(AnalysisDetail)
class AnalysisDetailAdmin(admin.ModelAdmin):
    list_display = ['report', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['report__url']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SavedReport)
class SavedReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report', 'session_id', 'created_at']
    list_filter = ['created_at', 'session_id']
    search_fields = ['name', 'report__url']
    readonly_fields = ['created_at']


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ['method', 'endpoint', 'status_code', 'response_time', 'ip_address', 'created_at']
    list_filter = ['method', 'status_code', 'created_at']
    search_fields = ['endpoint', 'ip_address']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False
