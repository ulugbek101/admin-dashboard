# Generated by Django 5.0.1 on 2024-11-05 23:21

import app_main.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pupil',
            name='group_payment',
            field=models.IntegerField(default=0, validators=[app_main.validators.min_value_validator], verbose_name="To'lov miqdori"),
        ),
        migrations.AddField(
            model_name='pupil',
            name='is_preferential',
            field=models.BooleanField(default=False, verbose_name="O'quvchi uchun imtiyozli to'lov"),
        ),
    ]