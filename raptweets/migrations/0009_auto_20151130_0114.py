# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptweets', '0008_auto_20151128_2212'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('artist', 'title')]),
        ),
    ]
