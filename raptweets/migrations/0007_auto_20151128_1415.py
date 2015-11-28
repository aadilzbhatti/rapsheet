# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptweets', '0006_album_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='image_url',
            field=models.CharField(max_length=500, default=''),
        ),
        migrations.AlterField(
            model_name='album',
            name='image_url',
            field=models.CharField(max_length=500, default=''),
        ),
    ]
