# Generated by Django 4.1.5 on 2023-09-11 08:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMonitoring', '0022_alter_labourcamp_documents_alter_labourcamp_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labourcamp',
            name='drinkingWaterPhotographs',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), size=None), default=None, size=None),
            preserve_default=False,
        ),
    ]
