try:
    import json
except ImportError:
    from simplejson import json
     
from jsonate.json_encoder import JsonateEncoder

def jsonate(obj):
    return json.dumps(obj, cls=JsonateEncoder)