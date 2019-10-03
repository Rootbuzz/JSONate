# -*- coding: utf-8 -*-
from django.db import models, migrations
import jsonate.fields
import test_app.models

class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_mymodelwithjsonatefield'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithJsonateFieldExpectingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('some_name', models.CharField(max_length=255)),
                ('some_json_data', jsonate.fields.JsonateField(default=list, validators=[test_app.models.validate_list])),
            ],
        ),
    ]
