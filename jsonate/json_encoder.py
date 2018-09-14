from datetime import datetime, date
from decimal import Decimal
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from .django_ver import django_19
if django_19:
    from django.db.models.query import ModelIterable
else:
    from django.db.models.query import ValuesQuerySet

from django.db.models.query import QuerySet
from django.db.models import Model, Manager
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import FieldFile

from .exceptions import CouldntSerialize

# Custom encoder using a list of mapping functions
type_map = []
class JsonateEncoder(json.JSONEncoder):
    def default(self, obj):
        for obj_type, mapper in type_map:
            if isinstance(obj, obj_type):
                # recurse until we get to an object the encoder
                # can handle natively
                try:
                    return self.default(mapper(obj))
                except CouldntSerialize:
                    pass
        try:
            # this will handle the non-string things that
            # the default encoder can handle (like numbers, booleans etc)
            return super(JsonateEncoder, self).default(obj)
        except TypeError:
            return obj
                

# Decorator for registering mapping functions
def register_typemap(obj_type):
    def wrapper(fn):
        type_map.append((obj_type, fn))
        return fn
    return wrapper


# helper function for getting the correct fields to serialize
def jsonate_fields(model):
    all_fields = tuple(f.name for f in model._meta.fields)
    
    excluded = getattr(model._meta, "jsonate_exclude", ())
    fields = getattr(model._meta, 'jsonate_fields', all_fields)
    
    serialize = set(fields).difference(set(excluded))

    # Getting all fields, including hidden fields as options
    return tuple(field for field in model._meta.get_fields()
                    if field.name in serialize)
    
#########################
##  Mapping functions  ##
#########################

# If the object knows how to serialize itself... let
# it do it's thing
@register_typemap(object)
def map_object(obj):
    to_json = getattr(obj, "to_json", getattr(obj, "toJSON", None))
    if to_json is None: 
        raise CouldntSerialize
    return to_json()


if not django_19:
    # Must come before map_queryset because ValuesQuerySet is
    # a subclass of Queryset and will cause an infinite loop :(
    @register_typemap(ValuesQuerySet)
    def map_values_queryset(obj):
        return list(obj)

@register_typemap(QuerySet)
def map_queryset(obj):
    # if the model wants to serialize itself, go with that...
    if hasattr(obj.model, 'to_json') or hasattr(obj.model, 'toJSON'):
        return list(obj)

    # otherwise using values is faster
    if django_19:
        if obj._iterable_class == ModelIterable:

            fields = jsonate_fields(obj.model)
            obj = obj.values(*[field.name for field in fields])

        return list(obj)

    else:
        fields = jsonate_fields(obj.model)
        return obj.values(*[field.name for field in fields])

# Managers are typically hidden fields, and must be specified via meta fields
@register_typemap(Manager)
def map_manager(obj):
    return obj.get_queryset()

@register_typemap(Model)
def map_model_instance(obj):
    d = {}
    for field in jsonate_fields(obj):
        value = getattr(obj, field.name)
        if isinstance(field, ForeignKey) and value is not None:
            value = value._get_pk_val()
        d[field.name] = value
    return d

@register_typemap(set)
def map_set(obj):
    return list(obj)

@register_typemap(FieldFile)
def map_filefield_file(obj):
    return obj.name

@register_typemap(date)
@register_typemap(datetime)
def map_datetime(obj):
    return obj.isoformat()

@register_typemap(Decimal)
def map_decimal(obj):
    return float(obj)