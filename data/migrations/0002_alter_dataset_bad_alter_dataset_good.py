# Generated by Django 5.0.4 on 2024-04-30 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='bad',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='good',
            field=models.IntegerField(default=0),
        ),
    ]
