# Generated by Django 5.0.4 on 2024-05-01 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_alter_dataset_bad_alter_dataset_good'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Dataset',
        ),
    ]
