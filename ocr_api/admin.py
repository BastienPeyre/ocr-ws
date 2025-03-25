from django.contrib import admin
from .models import Document, OCRResult


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'upload_date', 'processed')
    list_filter = ('processed', 'upload_date')
    search_fields = ('id',)
    readonly_fields = ('upload_date',)
    date_hierarchy = 'upload_date'


@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'confidence', 'processing_time', 'date_processed')
    list_filter = ('date_processed',)
    search_fields = ('document__id', 'text')
    readonly_fields = ('date_processed',)
    date_hierarchy = 'date_processed'
