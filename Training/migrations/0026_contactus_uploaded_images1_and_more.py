# Generated by Django 4.1.5 on 2023-08-12 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training', '0025_remove_traning_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='uploaded_images1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='contactus',
            name='uploaded_images2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
