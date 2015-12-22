# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonate.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModelWithJsonateField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('some_name', models.CharField(max_length=255)),
                ('some_json_data', jsonate.fields.JsonateField(null=True, blank=True)),
            ],
        ),
    ]
