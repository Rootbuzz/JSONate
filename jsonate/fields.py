try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.db import models

from .utils import jsonate
from .widgets import JsonateWidget
from .form_fields import JsonateFormField

class JsonateField(models.TextField):
    def _deserialize(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def from_db_value(self, value, expression, connection, context=None):
        return self._deserialize(value)

    def to_python(self, value):
        return self._deserialize(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value == "":
            return None

        if not isinstance(value, str):
            value = jsonate(value)

        return value

    def formfield(self, **kwargs):
        defaults = {
            'form_class': JsonateFormField,
            'widget': JsonateWidget
        }
        defaults.update(kwargs)

        return super(JsonateField, self).formfield(**defaults)