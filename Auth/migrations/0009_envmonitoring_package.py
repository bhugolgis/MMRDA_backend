# Generated by Django 4.1.2 on 2022-11-15 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0008_alter_envqualitymonitoring_eqm_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='envmonitoring',
            name='package',
            field=models.CharField(choices=[('CA-07', 'CA-07'), ('CA-10', 'CA-10'), ('CA-09', 'CA-09')], default=None, max_length=255),
            preserve_default=False,
        ),
    ]