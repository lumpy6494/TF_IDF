from django import template
from django.db.models import Count

from upload_file.models import Upload

register = template.Library()


@register.inclusion_tag('upload_file/count_files.html')
def count_files():
    count_files =  Upload.objects.all().count()
    return {'count_files': count_files}