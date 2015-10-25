# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptweets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='date',
            new_name='pub_date',
        ),
        migrations.AlterField(
            model_name='tweet',
            name='sentiment',
            field=models.FloatField(),
        ),
    ]
