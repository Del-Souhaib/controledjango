# Generated by Django 4.0.4 on 2022-05-05 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allout_souhaib', '0002_patient_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='password',
        ),
    ]
