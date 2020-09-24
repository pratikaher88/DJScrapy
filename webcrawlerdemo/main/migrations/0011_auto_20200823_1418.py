# Generated by Django 2.0.12 on 2020-08-23 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200411_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recent_Runs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_data_id', models.IntegerField(blank=True, null=True)),
                ('site_name', models.CharField(max_length=1000, validators=[django.core.validators.URLValidator()])),
                ('average_score', models.CharField(blank=True, max_length=100)),
                ('average_time', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
    ]
