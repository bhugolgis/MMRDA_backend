# Generated by Django 4.1.5 on 2024-03-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training', '0034_constructionstage_authorizationforcollectiondisposalmanagementdocuments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preconstructionstage',
            name='CRZClearanceDocuments',
            field=models.FileField(blank=True, null=True, upload_to='pre_construction/'),
        ),
        migrations.AlterField(
            model_name='preconstructionstage',
            name='ForestClearanceDocuments',
            field=models.FileField(blank=True, null=True, upload_to='pre_construction/'),
        ),
        migrations.AlterField(
            model_name='preconstructionstage',
            name='PermissionForFellingOfTreesDocuments',
            field=models.FileField(blank=True, null=True, upload_to='pre_construction/'),
        ),
        migrations.AlterField(
            model_name='preconstructionstage',
            name='ShiftingofUtilitiesDocuments',
            field=models.FileField(blank=True, null=True, upload_to='pre_construction/'),
        ),
    ]