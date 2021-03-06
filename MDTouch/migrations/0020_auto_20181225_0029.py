# Generated by Django 2.0.9 on 2018-12-24 18:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MDTouch', '0019_auto_20181224_0447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcentre',
            name='tests',
        ),
        migrations.AddField(
            model_name='message',
            name='receiverid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='testcentre',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Login'),
        ),
        migrations.AddField(
            model_name='testservices',
            name='testcenterid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.TestCentre'),
        ),
        migrations.AlterField(
            model_name='ambulancebilling',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 25, 0, 29, 10, 105951)),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 25, 0, 29, 10, 104031)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='qualification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Qualification'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Specialization'),
        ),
        migrations.AlterField(
            model_name='event',
            name='pic',
            field=models.CharField(default='no image', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 25, 0, 29, 10, 102959)),
        ),
    ]
