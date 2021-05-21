from django import forms
from .models import URLdata


class URLdataForm(forms.ModelForm):
    class Meta:
        model = URLdata
        fields = ['url'] 

