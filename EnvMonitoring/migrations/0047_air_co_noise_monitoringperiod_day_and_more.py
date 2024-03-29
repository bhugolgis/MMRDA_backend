# Generated by Django 4.1.5 on 2024-01-30 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnvMonitoring', '0046_alter_materialmanegmanet_approvals'),
    ]

    operations = [
        migrations.AddField(
            model_name='air',
            name='CO',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='noise',
            name='monitoringPeriod_day',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='noise',
            name='monitoringPeriod_night',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='noise',
            name='noiseLevel_day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='noise',
            name='noiseLevel_night',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='noise',
            name='typeOfArea',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='existingtreemanagment',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='existingTree_documents/'),
        ),
        migrations.AlterField(
            model_name='existingtreemanagment',
            name='photographs',
            field=models.ImageField(blank=True, null=True, upload_to='Existingtree_photos/'),
        ),
        migrations.AlterField(
            model_name='materialmanegmanet',
            name='approvals',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='materialmanegmanet',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='MaterialManegment/materialsourcing_documents'),
        ),
        migrations.AlterField(
            model_name='materialmanegmanet',
            name='materialStoragePhotograph',
            field=models.ImageField(blank=True, null=True, upload_to='MaterialManegment/materailStorage_Photograph'),
        ),
        migrations.AlterField(
            model_name='materialmanegmanet',
            name='photographs',
            field=models.ImageField(blank=True, null=True, upload_to='MaterialManegment/materialsourcing_photographs/'),
        ),
        migrations.AlterField(
            model_name='newtreemanagement',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='newTree_documents/'),
        ),
        migrations.AlterField(
            model_name='newtreemanagement',
            name='photographs',
            field=models.ImageField(blank=True, null=True, upload_to='newTree_photographs/'),
        ),
        migrations.AlterField(
            model_name='wastetreatments',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='waste_documents'),
        ),
        migrations.AlterField(
            model_name='wastetreatments',
            name='photographs',
            field=models.ImageField(blank=True, null=True, upload_to='waste_photographs/'),
        ),
    ]
