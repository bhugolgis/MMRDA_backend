# Generated by Django 4.1.5 on 2023-01-05 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EnvMonitoring', '0020_materialmanegmanet_storagetypeofmaterial_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materialmanegmanet',
            old_name='storageTypeOfMaterial',
            new_name='materialStorageType',
        ),
    ]
