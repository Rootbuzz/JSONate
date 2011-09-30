from django.http import HttpResponse
from jsonate import jsonate

class JsonateResponse(HttpResponse):
    """
    Subclass of HttpResponse that turns just about anything into JSON
    via jsonate() and returns the result with mimetype "application/json"
    """
    def __init__(self, content, mimetype='application/json', jsonp_callback=False, *args, **kwargs):
        json_content = jsonate(content)
        if jsonp_callback:
            json_content = jsonp_callback + "(" + json_content + ");"
        
        super(JsonateResponse, self).__init__(json_content, mimetype, *args, **kwargs)