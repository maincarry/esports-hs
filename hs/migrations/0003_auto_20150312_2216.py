# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hs', '0002_auto_20150312_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 13, 14, 16, 41, 174196, tzinfo=utc), verbose_name='deadline'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 14, 16, 41, 174138, tzinfo=utc), verbose_name='date started'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contestants',
            name='score',
            field=models.FloatField(default=50),
            preserve_default=True,
        ),
    ]
