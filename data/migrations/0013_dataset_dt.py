# Generated by Django 5.0.4 on 2024-05-01 16:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_remove_dataset_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='dt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
