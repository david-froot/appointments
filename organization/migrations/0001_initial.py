# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisitRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('window_start', models.DateField()),
                ('window_end', models.DateField()),
                ('address', models.CharField(max_length=1000, verbose_name='Address')),
                ('city', models.CharField(max_length=1000, verbose_name='City')),
                ('state', models.CharField(max_length=2, verbose_name='State')),
                ('zipcode', models.CharField(max_length=7, verbose_name='Zip Code')),
                ('start', models.TimeField(verbose_name='Start Time (HH:MM)')),
                ('end', models.TimeField(verbose_name='End Time (HH:MM)')),
                ('details', models.TextField(max_length=1000, null=True, verbose_name='Details (Will be shown to patients).  I.e. come to the conference room', blank=True)),
                ('status', models.CharField(max_length=100, choices=[('Confirmed', 'Confirmed'), ('Rejected', 'Rejected'), ('Pending', 'Pending')])),
                ('organization', models.ForeignKey(to='organization.Organization')),
            ],
        ),
    ]
