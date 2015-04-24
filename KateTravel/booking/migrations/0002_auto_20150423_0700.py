# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='KTL_child',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='web_child',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2),
            preserve_default=True,
        ),
    ]
