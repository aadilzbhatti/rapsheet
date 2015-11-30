# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptweets', '0009_auto_20151130_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='popularity',
        ),
    ]
