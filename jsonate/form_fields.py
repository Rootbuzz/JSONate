try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.forms import CharField, ValidationError

from .widgets import JsonateWidget


def JsonateValidator(value):
    try: 
        json.loads(value)
    except: 
        raise ValidationError("Not Valid JSON")


class JsonateFormField(CharField):
    widget = JsonateWidget
    
    def __init__(self, *args, **kwargs):
        super(JsonateFormField, self).__init__(*args, **kwargs)
        self.validators.append(JsonateValidator)
