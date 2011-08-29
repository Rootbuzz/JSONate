from django.http import HttpResponse
from jsonate import jsonate

class JsonateResponse(HttpResponse):
    """
    Subclass of HttpResponse that turns just about anything into JSON
    via jsonate() and returns the result with mimetype "application/json"
    """
    def __init__(self, content, mimetype='application/json', *args, **kwargs):
        super(JsonateResponse, self).__init__(jsonate(content), mimetype, *args, **kwargs)