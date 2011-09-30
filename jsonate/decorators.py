from jsonate.http import JsonateResponse
from django.http import HttpResponse

try:
    from functools import wraps
except ImportError: 
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),
              updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner

def jsonate_request(func):
    """
    Serializes whatever the view returns to JSON and returns it with
    mimetype "application/json" (uses jsonate.http.JsonateResponse)
    
    If the view returns an HttpResponse, it will pass through without
    changes. 

    examples:
        
        @jsonate_request
        def my_view(request):
            return User.objects.all()
            
        @jsonate_request
        def my_view(request):
            form = MyForm(request.POST or None)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/some/url")
            else:
                return form.errors
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        resp = func(request, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        else:
            if request.GET.get("callback"):
                return JsonateResponse(resp, jsonp_callback=request.GET['callback'])
            return JsonateResponse(resp)
    return wrapper