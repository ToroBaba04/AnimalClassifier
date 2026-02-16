from django.contrib import admin
from .models import Classification


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('prediction', 'confidence', 'created_at')
    list_filter = ('prediction', 'created_at')
    readonly_fields = ('prediction', 'confidence', 'created_at')
