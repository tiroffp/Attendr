# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('create_roll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='order',
            field=models.IntegerField(null=True, blank=True, default=None),
        ),
    ]
