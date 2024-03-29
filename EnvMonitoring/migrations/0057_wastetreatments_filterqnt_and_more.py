# Generated by Django 4.1.5 on 2024-03-13 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnvMonitoring', '0056_remove_wastetreatments_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wastetreatments',
            name='filterQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isCCPCPaintSludgeQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isairFiltersQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isbioDegradableQuantity',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isbioMedicalQuantity',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isbottlesQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isconstructionWasteQuantity',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='iseWasteQuantity',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isfilterQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='ismetalScrapeQuantity',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='ispaperQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isplasticQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isrubberQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='isusedCartridgesQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='iswasteOilQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='iswoodQnt',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
