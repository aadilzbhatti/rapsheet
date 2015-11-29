# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptweets', '0007_auto_20151128_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='text',
            field=models.CharField(max_length=140, unique=True),
        ),
    ]
