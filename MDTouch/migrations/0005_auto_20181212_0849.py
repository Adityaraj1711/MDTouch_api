# Generated by Django 2.0.9 on 2018-12-12 03:19

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MDTouch', '0004_auto_20181212_0818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='day',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='month',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='year',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointmentdate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ambulancebilling',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 12, 8, 49, 42, 154967)),
        ),
    ]
