# Generated by Django 2.1.3 on 2019-05-10 02:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0008_remove_evaluacion_tiempo'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='tiempo',
            field=models.TimeField(default=datetime.datetime(2019, 5, 10, 2, 22, 2, 793668, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='tiempo_max',
            field=models.TimeField(default=datetime.datetime(2019, 5, 10, 2, 22, 2, 793668, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='tiempo_min',
            field=models.TimeField(default=datetime.datetime(2019, 5, 10, 2, 22, 2, 793668, tzinfo=utc)),
        ),
    ]
