# Generated by Django 4.0.5 on 2022-07-20 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawtool', '0002_alter_aoi_creation_date_alter_aoi_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aoi',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 20, 21, 40, 57, 528637)),
        ),
        migrations.AlterField(
            model_name='measure',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 20, 21, 40, 57, 529637)),
        ),
    ]
