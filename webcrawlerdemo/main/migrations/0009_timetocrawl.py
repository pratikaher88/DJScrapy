# Generated by Django 2.0.12 on 2020-01-07 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_url_details_job_data_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeToCrawl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_data_id', models.IntegerField(blank=True, null=True)),
                ('domain_name', models.TextField()),
                ('time_to_crawl', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
