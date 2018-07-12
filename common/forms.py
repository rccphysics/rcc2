from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import Site

class SiteForm(ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
