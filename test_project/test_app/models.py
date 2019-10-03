from datetime import datetime, date
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User

from jsonate.fields import JsonateField

class MyModel(models.Model):
    foreign_key = models.ForeignKey(User, on_delete=models.CASCADE)
    normal_field1 = models.CharField(max_length=25, default="field1")
    normal_field2 = models.CharField(max_length=25, default='field2')
    
    sensitive_field1 = models.CharField(max_length=25, default='sensitive')
    
    datetime_field = models.DateTimeField(default=datetime(2011, 1, 11, 11, 11, 11))
    date_field = models.DateField(default=date(2011, 1, 11))
    
    decimal_field = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('32.25'))
    float_field = models.FloatField(default=32.25)
    
    file_field = models.FileField(upload_to="files")
    image_field = models.ImageField(upload_to="images")
    
    boolean_field = models.BooleanField(default=True)
    null_field = models.NullBooleanField(default=None)
    
    class Meta:
        jsonate_exclude = ('sensitive_field1',)

class MyModelWithRelation(models.Model):
    name = models.CharField(max_length=100)
    to_many = models.ManyToManyField(MyModel, related_name="many_to_my_model")

class MyModelWithJsonateField(models.Model):
    some_name = models.CharField(max_length=255)
    some_json_data = JsonateField(null=True, blank=True)

def validate_list(is_this_list):
    from django.core.exceptions import ValidationError

    if not isinstance(is_this_list, list):
        raise ValidationError("Must be a list")

class WithJsonateFieldExpectingList(models.Model):
    some_name = models.CharField(max_length=255)
    some_json_data = JsonateField(default=[], validators=[validate_list,])
