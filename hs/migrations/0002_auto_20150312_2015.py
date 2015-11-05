# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='expire_date',
            field=models.DateTimeField(verbose_name='deadline', default=datetime.datetime(2015, 3, 13, 12, 15, 10, 264994, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='result',
            field=models.CharField(choices=[('WIN', 'Success'), ('LOSE', 'Fail'), ('SPECIAL', 'SPECIAL'), ('PEND', 'Pending'), (None, 'None')], default='PEND', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='start_date',
            field=models.DateTimeField(verbose_name='date started', default=datetime.datetime(2015, 3, 12, 12, 15, 10, 264911, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contestants',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=7, default=50),
            preserve_default=True,
        ),
    ]
