# Generated by Django 4.1.5 on 2024-05-23 11:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMonitoring', '0039_remove_pap_cadastralmapdocuments_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pap',
            name='cadastralMapDocuments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), default=[], size=None),
            preserve_default=False,
        ),
    ]