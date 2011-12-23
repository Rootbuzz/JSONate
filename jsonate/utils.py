from django.utils import simplejson as json
     
from jsonate.json_encoder import JsonateEncoder

def jsonate(obj):
    return json.dumps(obj, cls=JsonateEncoder)