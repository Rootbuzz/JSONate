from django.db import models
import json
from jsonate.utils import jsonate
from jsonate.widgets import JsonateWidget
from jsonate.form_fields import JsonateFormField

class JsonateField(models.TextField):
    def from_db_value(self, value, expression, connection, context):
        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None

        if not isinstance(value, basestring):
            value = jsonate(value)

        return super(JsonateField, self).get_db_prep_save(value, *args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': JsonateFormField,
            'widget': JsonateWidget
        }
        defaults.update(kwargs)
        return super(JsonateField, self).formfield(**defaults)