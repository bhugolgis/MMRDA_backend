# Generated by Django 4.1.5 on 2023-09-11 12:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMonitoring', '0029_alter_constructionsitedetails_availabilityofdoctorphotographs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constructionsitedetails',
            name='documents',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), default=None, size=None),
            preserve_default=False,
        ),
    ]
