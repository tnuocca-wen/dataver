# Generated by Django 5.0.4 on 2024-05-01 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='again',
            field=models.BooleanField(default=True),
        ),
    ]
