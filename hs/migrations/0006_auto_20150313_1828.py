# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hs', '0005_auto_20150313_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='result',
            field=models.CharField(choices=[('PEND', 'Pending'), ('WIN', 'Success'), ('LOSE', 'Fail'), ('SPECIAL', 'SPECIAL'), ('CANCEL', 'CANCELLED')], max_length=10, default='PEND'),
            preserve_default=True,
        ),
    ]
