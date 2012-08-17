from django.db import models
from django.utils import simplejson as json
from jsonate.utils import jsonate

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
    