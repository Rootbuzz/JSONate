import json
     
from jsonate.json_encoder import JsonateEncoder

def jsonate(obj, *args, **kwargs):
    kwargs['cls'] = JsonateEncoder
    return json.dumps(obj, *args, **kwargs)