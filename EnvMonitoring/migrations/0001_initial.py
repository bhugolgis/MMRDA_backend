# Generated by Django 4.1.2 on 2022-12-05 11:22

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Air',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.CharField(blank=True, choices=[('JAN-MAR 2022', 'JAN-MAR 2022'), ('APR-JUN 2022', 'APR-JUN 2022'), ('JULY-AUG 2022', 'JULY-AUG 2022')], max_length=255, null=True)),
                ('package', models.CharField(blank=True, choices=[('CA-08', 'CA-08'), ('CA-09', 'CA-09'), ('CA-10', 'CA-10'), ('CA-11', 'CA-11'), ('CA-12', 'CA-12'), ('CA-54', 'CA-54')], max_length=255, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('standard', models.FloatField(blank=True, max_length=255, null=True)),
                ('deviation', models.FloatField(blank=True, max_length=255, null=True)),
                ('trends', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MaterialSourcing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.CharField(blank=True, choices=[('JAN-MAR 2022', 'JAN-MAR 2022'), ('APR-JUN 2022', 'APR-JUN 2022'), ('JULY-AUG 2022', 'JULY-AUG 2022')], max_length=255, null=True)),
                ('package', models.CharField(blank=True, choices=[('CA-08', 'CA-08'), ('CA-09', 'CA-09'), ('CA-10', 'CA-10'), ('CA-11', 'CA-11'), ('CA-12', 'CA-12'), ('CA-54', 'CA-54')], max_length=255, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('approvals', models.FileField(blank=True, null=True, upload_to='')),
                ('source_of_quary', models.CharField(choices=[('Mines', 'Mines'), ('Blast', 'Blast')], max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Noise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.CharField(blank=True, choices=[('JAN-MAR 2022', 'JAN-MAR 2022'), ('APR-JUN 2022', 'APR-JUN 2022'), ('JULY-AUG 2022', 'JULY-AUG 2022')], max_length=255, null=True)),
                ('package', models.CharField(blank=True, choices=[('CA-08', 'CA-08'), ('CA-09', 'CA-09'), ('CA-10', 'CA-10'), ('CA-11', 'CA-11'), ('CA-12', 'CA-12'), ('CA-54', 'CA-54')], max_length=255, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('noise_level', models.CharField(blank=True, max_length=255, null=True)),
                ('Monitoring_Period', models.CharField(blank=True, choices=[('1 hour', '1 hour'), ('3 hours', '3 hours'), ('6 hours', '6 hours')], max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TreeManagment',
            fields=[
                ('tree_no', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('quarter', models.CharField(blank=True, choices=[('JAN-MAR 2022', 'JAN-MAR 2022'), ('APR-JUN 2022', 'APR-JUN 2022'), ('JULY-AUG 2022', 'JULY-AUG 2022')], max_length=255, null=True)),
                ('package', models.CharField(blank=True, choices=[('CA-08', 'CA-08'), ('CA-09', 'CA-09'), ('CA-10', 'CA-10'), ('CA-11', 'CA-11'), ('CA-12', 'CA-12'), ('CA-54', 'CA-54')], max_length=255, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('common_name', models.CharField(blank=True, max_length=255, null=True)),
                ('botanical_name', models.CharField(blank=True, max_length=255, null=True)),
                ('condition', models.CharField(blank=True, max_length=255, null=True)),
                ('survey_date', models.DateField(blank=True, null=True)),
                ('survey_time', models.TimeField(blank=True, null=True)),
                ('planted', models.BooleanField()),
                ('planted_details', models.CharField(blank=True, max_length=255, null=True)),
                ('No_of_trees_cut', models.IntegerField(blank=True, null=True)),
                ('Cutting_details', models.CharField(blank=True, max_length=255, null=True)),
                ('transplanted', models.BooleanField()),
                ('transplanted_details', models.CharField(blank=True, max_length=255, null=True)),
                ('Management', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WasteTreatments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.CharField(blank=True, choices=[('JAN-MAR 2022', 'JAN-MAR 2022'), ('APR-JUN 2022', 'APR-JUN 2022'), ('JULY-AUG 2022', 'JULY-AUG 2022')], max_length=255, null=True)),
                ('package', models.CharField(blank=True, choices=[('CA-08', 'CA-08'), ('CA-09', 'CA-09'), ('CA-10', 'CA-10'), ('CA-11', 'CA-11'), ('CA-12', 'CA-12'), ('CA-54', 'CA-54')], max_length=255, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('waste_type', models.CharField(choices=[('Hazardous Waste', 'Hazardous'), ('Bio Waste', 'Bio'), ('electronic waste', 'Electronic')], max_length=255)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('waste_handled', models.CharField(blank=True, choices=[('disposal', 'disposal'), ('Dumped', 'Dumped'), ('Transported to another location', 'Transported to another location'), ('recycle', 'recycle')], max_length=255, null=True)),
                ('waste_handled_details', models.CharField(blank=True, max_length=255, null=True)),
                ('photographs', models.ImageField(blank=True, null=True, upload_to='')),
                ('documents', models.FileField(blank=True, null=True, upload_to='')),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='water',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.CharField(blank=True, choices=[('JAN-MAR 2022', 'JAN-MAR 2022'), ('APR-JUN 2022', 'APR-JUN 2022'), ('JULY-AUG 2022', 'JULY-AUG 2022')], max_length=255, null=True)),
                ('package', models.CharField(blank=True, choices=[('CA-08', 'CA-08'), ('CA-09', 'CA-09'), ('CA-10', 'CA-10'), ('CA-11', 'CA-11'), ('CA-12', 'CA-12'), ('CA-54', 'CA-54')], max_length=255, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('date', models.DateField(auto_now=True, null=True)),
                ('quality_of_water', models.CharField(blank=True, max_length=255, null=True)),
                ('source_of_water', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]