from django.template import Library
from django.template.defaultfilters import escape
from jsonate import jsonate

register = Library()

register.filter("jsonate", jsonate)

@register.filter
def jsonate_attr(obj):
    return escape(jsonate(obj))