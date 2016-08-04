# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='attendee',
            name='roll',
            field=models.ForeignKey(default=None, to='create_roll.Roll'),
        ),
        migrations.AlterUniqueTogether(
            name='attendee',
            unique_together=set([('roll', 'name')]),
        ),
    ]
