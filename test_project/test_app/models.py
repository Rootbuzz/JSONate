from datetime import datetime, date
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User

class MyModel(models.Model):
    foreign_key = models.ForeignKey(User)
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
