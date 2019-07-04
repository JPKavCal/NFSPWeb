# Generated by Django 2.2.1 on 2019-07-04 20:48

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gaugedata', '0002_auto_20190627_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catchment',
            fields=[
                ('dws_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('area', models.FloatField()),
                ('arf', models.FloatField()),
                ('lc', models.FloatField()),
                ('s1085', models.FloatField()),
                ('tc', models.FloatField()),
                ('dr2', models.IntegerField()),
                ('dr5', models.IntegerField()),
                ('dr10', models.IntegerField()),
                ('dr20', models.IntegerField()),
                ('dr50', models.IntegerField()),
                ('dr100', models.IntegerField()),
                ('dr200', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
    ]