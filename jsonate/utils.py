try:
    import json
except ImportError:
    from django.utils import simplejson as json

from .json_encoder import JsonateEncoder

def jsonate(obj, *args, **kwargs):
    kwargs['cls'] = JsonateEncoder
    return json.dumps(obj, *args, **kwargs)