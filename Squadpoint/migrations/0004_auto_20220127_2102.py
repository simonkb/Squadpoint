# Generated by Django 3.2.7 on 2022-01-27 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Squadpoint', '0003_auto_20220127_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='match',
            name='is_held',
            field=models.BooleanField(default=False),
        ),
    ]