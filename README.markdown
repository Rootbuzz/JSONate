## Installation ##

 1. Install lib with pip:
 
    `pip install jsonate`
   
    **- OR -**

    Put the "jsonate" directory somewhere in your python path

 2. Add "jsonate" to your installed apps (in the settings.py file)


## Usage ##

### In templates

    {% load jsonate_tags %}

    {{ anything|jsonate }}

This is especially useful for embedding data in in data attributes for
use with javascript libraries like jQuery (note jsonate-attr is identical to jsonate|escape):

    <div id="user-widget" data-user="{{ user|jsonate_attr }}"></div>

	<script>
		...
    	user_data = $("#user-widget").data('user');
    	...
    </script>
    
Or just use it directly in javascript...

    <script>
		var user_data = {{ user|jsonate }};
    </script>

### In Python

    from jsonate import jsonate
    
    # querysets
    json = jsonate(User.objects.all())
    
    # values 
    json = jsonate(User.objects.values())
    
    # model instances
    json = jsonate(User.objects.get(email="my_email@gmail.com"))
    
Jsonate turns datetimes into iso format for easy parsing in javascript

	# formatted response for ease of reading...
    >>> print jsonate(User.objects.all()[0])
    {
    	"username": "asdfasdf", 
    	"first_name": "asdf", 
    	"last_name": "asdf", 
    	"is_active": false, 
    	"email": "asdf@example.com", 
    	"is_superuser": false, 
    	"is_staff": false, 
    	"last_login": "2011-08-22T19:14:50.603531",  
    	"id": 5, 
    	"date_joined": "2011-08-22T19:14:50.220049"
    }
    
## Fields / Exclude options

You may specify which fields should be serialized in the meta options of
your models. This affects the serialization of model instances, and querysets,
just like the Admin!

Example
	
	class MyModel(models.Model):
		normal_info = models.CharField(max_length=10)
		sensitive_info = models.CharField(max_length=10)
		
		class Meta:
			jsonate_exclude = ('sensitive_info',)
			# this would also work:
			# jsonate_fields = ('normal_info',)

By default the User model in `django.contrib.auth.models` is monkey-patched
to exclude the password field when serializing querysets or instances

If you want to specify which fields will be serialized on a per-case basis,
use `values()` instead. like so

    >>> jsonate(User.objects.values("username", "password"))
    ... '[{"username": "someuser", "password": "sha1$f26b2$d03a6123487fce20aabcdef0987654321abcdef0"}]'

note: this is obviously not a real password or salt :)

## The JsonateResponse

`JsonateResponse` is a subclass of HttpResponse that works almost exactly
the same, except that it accepts any object as it's data rather than just 
strings. It returns the resulting json as mimetype "application/json"

example:

	from jsonate.http import JsonateResponse

	def my_view(request):
		...
		return JsonateResponse(request.user)
		
	# response contains:
	{"username": "asdfasdf", "first_name": "asdf", "last_name": "asdf", "is_active": false, "email": "asdf@example.com", "is_superuser": false, "is_staff": false, "last_login": "2011-08-22T19:14:50.603531", "id": 5, "date_joined": "2011-08-22T19:14:50.220049"}


## Decorator

The `JsonateResponse` is great, but life could get even easier! The 
`@jsonate_request` decorator (inspired by the ajax_request decorator
in django-annoying) will try to serialize anything a view returns
(via JsonateResponse) return it in an HttpResponse with mimetype
"application/json"

The only thing it will *not* try to serialize is an HttpResponse.

example:

	@jsonate_request
	def my_view(request):
		form = MyForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/some/path/")
		else:
			return form.errors
			
With valid input, the HttpResponseRedirect passes through, untouched.

If there are form errors the response comes back looking something like
this:

	{
	  "username": [
	    "This username is already taken"
	  ], 
	  "email": [
	    "Please enter a valid email."
	  ]
	}
