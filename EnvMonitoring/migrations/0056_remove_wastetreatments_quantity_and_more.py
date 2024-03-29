# Generated by Django 4.1.5 on 2024-03-08 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnvMonitoring', '0055_alter_wastetreatments_documents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wastetreatments',
            name='quantity',
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='CCPCPaintSludgeQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='airFiltersQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='bioDegradableQuantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='bioMedicalQuantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='bottlesQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='constructionWasteQuantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='eWasteQuantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='metalScrapeQuantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='paperQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='plasticQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='rubberQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='usedCartridgesQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='wasteOilQnt',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastetreatments',
            name='woodQnt',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
