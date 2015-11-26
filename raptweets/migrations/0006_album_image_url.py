# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptweets', '0005_auto_20151126_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='image_url',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
