# Generated by Django 2.0.12 on 2020-01-02 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200102_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='job_d_id',
            new_name='job_data_id',
        ),
    ]
