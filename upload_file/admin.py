from django.contrib import admin

from .models import Upload

class UploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at',)
    search_fields = ('file',)
    list_display_links = ('id', 'created_at',)

    class Meta:
        model = Upload
        fields = '__all__'


admin.site.register(Upload, UploadAdmin)
