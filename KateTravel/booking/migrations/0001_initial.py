# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=300)),
                ('during_time', models.CharField(max_length=50)),
                ('web_adult', models.DecimalField(max_digits=6, decimal_places=2)),
                ('web_child', models.DecimalField(max_digits=6, decimal_places=2)),
                ('KTL_adult', models.DecimalField(max_digits=6, decimal_places=2)),
                ('KTL_child', models.DecimalField(max_digits=6, decimal_places=2)),
                ('deposit', models.BooleanField(default=False)),
                ('deposit_adult', models.DecimalField(max_digits=6, null=True, decimal_places=2)),
                ('deposit_child', models.DecimalField(max_digits=6, null=True, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True)),
                ('comment', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('timeslot', models.CharField(max_length=10)),
                ('activity_id', models.ForeignKey(to='booking.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='company',
            field=models.ForeignKey(to='booking.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.ForeignKey(to='booking.Location'),
            preserve_default=True,
        ),
    ]
