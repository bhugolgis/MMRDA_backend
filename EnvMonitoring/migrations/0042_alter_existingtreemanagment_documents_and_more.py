# Generated by Django 4.1.5 on 2023-08-19 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnvMonitoring', '0041_sensors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='existingtreemanagment',
            name='documents',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='existingtreemanagment',
            name='photographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
