# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20150423_0700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetable',
            old_name='activity_id',
            new_name='activity',
        ),
        migrations.AlterField(
            model_name='timetable',
            name='timeslot',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
