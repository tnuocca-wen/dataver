# Generated by Django 5.0.4 on 2024-05-01 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_alter_dataset_dt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='dt',
        ),
    ]
