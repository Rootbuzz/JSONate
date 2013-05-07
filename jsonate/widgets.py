from django import forms
from django.utils import simplejson as json
from jsonate.utils import jsonate

class JsonateWidget(forms.Textarea):
    
    def render(self, name, value, attrs=None):
        value = jsonate(value, indent=2)
        return super(JsonateWidget, self).render(name, value, attrs)