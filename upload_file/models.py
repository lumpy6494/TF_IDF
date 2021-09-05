from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
from django.urls import reverse


class Upload(models.Model):
    file = models.FileField(upload_to='upload/%Y/%m/%d', verbose_name='Загрузка файла', validators=[FileExtensionValidator(['txt',])] )
    json = models.JSONField(blank=True, verbose_name='JSON текста')
    doc_list = models.JSONField(blank=True, verbose_name='Список текста',null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки', blank =True, null=True)


    def __str__(self):
        return " Загрузка файла + JSON "

    def get_absolute_url(self):
        return reverse('home')

