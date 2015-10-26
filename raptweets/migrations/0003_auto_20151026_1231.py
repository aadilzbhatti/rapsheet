# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptweets', '0002_auto_20151025_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='album',
            field=models.ForeignKey(to='raptweets.Album', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tweet',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
