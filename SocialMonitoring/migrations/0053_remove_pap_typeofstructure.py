# Generated by Django 4.1.5 on 2024-09-18 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMonitoring', '0052_remove_labourcamp_distancefromsite_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pap',
            name='typeOfStructure',
        ),
    ]
