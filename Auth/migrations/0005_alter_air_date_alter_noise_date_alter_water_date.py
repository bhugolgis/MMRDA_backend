# Generated by Django 4.1.2 on 2022-11-15 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0004_alter_air_quarter_alter_noise_quarter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='air',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='noise',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='water',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]