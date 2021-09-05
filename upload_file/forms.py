from django import forms
from .models import Upload


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['file']

        widgets = {
            'file':forms.FileInput(attrs={'class':'form-input has-value form-submit', 'type':'file',})
        }
