# Generated by Django 5.0.4 on 2024-05-01 16:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_remove_dataset_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 1, 16, 21, 49, 994375, tzinfo=datetime.timezone.utc)),
        ),
    ]
