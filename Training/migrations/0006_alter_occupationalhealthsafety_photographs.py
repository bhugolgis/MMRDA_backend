# Generated by Django 4.1.2 on 2023-01-03 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training', '0005_alter_occupationalhealthsafety_compensationpaid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupationalhealthsafety',
            name='photographs',
            field=models.ImageField(blank=True, null=True, upload_to='OccupationalHealth&Safety/'),
        ),
    ]