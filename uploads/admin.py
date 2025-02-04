from django.contrib import admin
from .models import Upload


class UploadAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'uploded_at']


admin.site.register(Upload, UploadAdmin)
