# Generated by Django 4.1.5 on 2023-01-27 07:19

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ca10',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.FloatField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, dim=4, null=True, srid=0)),
            ],
            options={
                'db_table': 'ca-10',
                'managed': False,
            },
        ),
    ]