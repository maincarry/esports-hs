# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('hs', '0004_auto_20150312_2230'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contestants',
            new_name='Contestant',
        ),
    ]
