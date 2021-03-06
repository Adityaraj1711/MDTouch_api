# Generated by Django 2.0.9 on 2018-11-03 08:52

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=50)),
                ('lastName', models.CharField(default='', max_length=50)),
                ('username', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Ambulance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default='ECNALUBMA', max_length=15)),
                ('driver', models.CharField(default='', max_length=25)),
                ('capacity', models.CharField(default='2', max_length=2)),
                ('contact', models.CharField(default='', max_length=12)),
                ('type', models.CharField(default='van', max_length=10)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(default='', max_length=2)),
                ('day', models.CharField(default='', max_length=2)),
                ('year', models.CharField(default='', max_length=4)),
                ('appttime', models.CharField(default='', max_length=5)),
                ('phase', models.CharField(default='', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='BloodBankCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('address', models.TextField(default='', max_length=200)),
                ('city', models.CharField(default='', max_length=40)),
                ('contact', models.IntegerField(default=0)),
                ('email', models.EmailField(blank=True, max_length=70, null=True, unique=True)),
                ('quantityAp', models.IntegerField(default=0)),
                ('quantityAm', models.IntegerField(default=0)),
                ('quantityBp', models.IntegerField(default=0)),
                ('quantityBm', models.IntegerField(default=0)),
                ('quantityABp', models.IntegerField(default=0)),
                ('quantityABm', models.IntegerField(default=0)),
                ('quantityOp', models.IntegerField(default=0)),
                ('quantityOm', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Dispensaries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regno', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=50)),
                ('lastName', models.CharField(default='', max_length=50)),
                ('username', models.CharField(default='', max_length=30)),
                ('specialization', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=50)),
                ('lastName', models.CharField(default='', max_length=50)),
                ('number', models.CharField(default='', max_length=13)),
                ('address', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('city', models.CharField(default='new city', max_length=25)),
                ('address', models.TextField(default='', max_length=80)),
                ('email', models.EmailField(blank=True, max_length=70, null=True, unique=True)),
                ('contact_number', models.CharField(default='', max_length=12)),
                ('ambulance_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Ambulance')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=40)),
                ('description', models.TextField(default='', max_length=600)),
                ('pic', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='pic_folder/')),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('address', models.CharField(default='', max_length=200)),
                ('city', models.CharField(default='', max_length=40)),
                ('state', models.CharField(default='', max_length=20)),
                ('pin', models.IntegerField(default=0)),
                ('contact', models.IntegerField(default=0)),
                ('email', models.EmailField(blank=True, max_length=70, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=30)),
                ('password', models.CharField(default='Password123!', max_length=30)),
                ('dept', models.CharField(default='NA', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='LogInInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=30)),
                ('password', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=40)),
                ('price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('batch', models.IntegerField(default=0)),
                ('manufacturedate', models.DateField(default=datetime.datetime(2018, 11, 3, 8, 52, 22, 601621, tzinfo=utc))),
                ('expirydate', models.DateField(default=datetime.datetime(2018, 11, 3, 8, 52, 22, 601621, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senderName', models.CharField(default='', max_length=50)),
                ('senderType', models.CharField(default='', max_length=50)),
                ('receiverName', models.CharField(default='', max_length=50)),
                ('viewed', models.BooleanField(default=False)),
                ('date', models.DateField(default=datetime.date(2018, 11, 3))),
                ('subjectLine', models.CharField(default='', max_length=50)),
                ('message', models.TextField(default='', max_length=500)),
                ('senderDelete', models.BooleanField(default=False)),
                ('receiverDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=50)),
                ('lastName', models.CharField(default='', max_length=50)),
                ('username', models.CharField(default='', max_length=30)),
                ('workplace', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=50)),
                ('lastName', models.CharField(default='', max_length=50)),
                ('number', models.CharField(default='', max_length=13)),
                ('address', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('provider', models.CharField(default='', max_length=100)),
                ('insuranceid', models.CharField(default='', max_length=12)),
                ('height', models.CharField(default='', max_length=7)),
                ('weight', models.CharField(default='', max_length=6)),
                ('allergies', models.TextField(default='', max_length=500)),
                ('gender', models.CharField(default='', max_length=23)),
                ('username', models.CharField(default='', max_length=30)),
                ('password', models.CharField(default='Password123!', max_length=25)),
                ('dept', models.CharField(default='PA', max_length=2)),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.EmergencyContact')),
                ('hospital', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('dosage', models.CharField(max_length=100)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('released', models.BooleanField(default=False)),
                ('testResults', models.FileField(blank=True, null=True, upload_to='tests')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='eventlocation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='workplace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Hospital'),
        ),
        migrations.AddField(
            model_name='dispensaries',
            name='medicine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Medicine'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Hospital'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Patient'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='workplace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MDTouch.Hospital'),
        ),
    ]
