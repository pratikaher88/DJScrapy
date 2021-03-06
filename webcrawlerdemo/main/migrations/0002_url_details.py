# Generated by Django 2.0.12 on 2019-12-01 20:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='URL_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=500, validators=[django.core.validators.URLValidator()])),
                ('total_violations', models.CharField(blank=True, max_length=100)),
                ('total_verify', models.CharField(blank=True, max_length=100)),
                ('total_pass', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
