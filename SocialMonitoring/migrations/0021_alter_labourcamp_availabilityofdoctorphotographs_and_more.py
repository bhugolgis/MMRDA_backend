# Generated by Django 4.1.5 on 2023-09-11 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMonitoring', '0020_alter_constructionsitedetails_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labourcamp',
            name='availabilityOfDoctorPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='demarkationOfPathwaysPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='drinkingWaterPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='fireExtinguishPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='firstAidKitPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='kitchenAreaPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='regularHealthCheckupPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='roomsOrDomsPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='segregationOfWastePhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='signagesLabelingPhotographs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='labourcamp',
            name='toiletPhotograph',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]