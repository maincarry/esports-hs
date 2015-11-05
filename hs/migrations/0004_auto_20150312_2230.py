# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hs', '0003_auto_20150312_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='expire_date',
            field=models.DateTimeField(verbose_name='deadline'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='start_date',
            field=models.DateTimeField(verbose_name='date started'),
            preserve_default=True,
        ),
    ]
