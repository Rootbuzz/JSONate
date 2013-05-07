from django.db import models
from django.utils import simplejson as json
from jsonate.utils import jsonate
from jsonate.widgets import JsonateWidget
from jsonate.form_fields import JsonateFormField

class JsonateField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
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
        value = jsonate(value)
        return super(JsonateField, self).get_db_prep_save(value, *args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': JsonateFormField,
            'widget': JsonateWidget
        }
        defaults.update(kwargs)
        return super(JsonateField, self).formfield(**defaults)
    
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^jsonate\.fields\.JsonateField"])