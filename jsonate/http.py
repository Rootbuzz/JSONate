from django.http import HttpResponse
from jsonate import jsonate

class JsonateResponse(HttpResponse):
    """
    Subclass of HttpResponse that turns just about anything into JSON
    via jsonate() and returns the result with mimetype "application/json"
    """
    def __init__(self, content,request=None, mimetype='application/json', *args, **kwargs):
        ret = jsonate(content)          #:MUST be JSON str
        callback = request.GET.get('callback',None ) if request else None
        if callback:
            ret = callback + "(%s);" % ret
        super(JsonateResponse, self).__init__(ret, mimetype, *args, **kwargs)
