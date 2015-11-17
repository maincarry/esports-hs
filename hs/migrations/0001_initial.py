# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('start_date',
                 models.DateTimeField(default=datetime.datetime(2015, 3, 12, 10, 17, 29, 827054, tzinfo=utc),
                                      verbose_name='date started')),
                ('expire_date',
                 models.DateTimeField(default=datetime.datetime(2015, 3, 13, 10, 17, 29, 827102, tzinfo=utc),
                                      verbose_name='deadline')),
                ('result', models.CharField(default=None,
                                            choices=[('WIN', 'Success'), ('LOSE', 'Fail'), ('SPECIAL', 'SPECIAL'),
                                                     (None, 'None')], max_length=10)),
                ('remark', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contestants',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('score', models.DecimalField(decimal_places=2, max_digits=7)),
                ('phone', models.CharField(max_length=15, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='challenge',
            name='attacker',
            field=models.ForeignKey(related_name='attacks', to='hs.Contestants'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='challenge',
            name='defender',
            field=models.ForeignKey(related_name='defends', to='hs.Contestants'),
            preserve_default=True,
        ),
    ]
