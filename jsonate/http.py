from django.http import HttpResponse
from jsonate import jsonate

class JsonateResponse(HttpResponse):
    """
    Subclass of HttpResponse that turns just about anything into JSON
    via jsonate() and returns the result with mimetype "application/json"
    """
    def __init__(self, data):
        super(JsonateResponse, self).__init__(content=jsonate(data), mimetype='application/json')