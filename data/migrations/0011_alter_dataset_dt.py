# Generated by Django 5.0.4 on 2024-05-01 16:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_dataset_dt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='dt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
