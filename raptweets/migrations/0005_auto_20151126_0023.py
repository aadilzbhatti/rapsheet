# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptweets', '0004_auto_20151126_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='sales',
            new_name='popularity',
        ),
    ]
