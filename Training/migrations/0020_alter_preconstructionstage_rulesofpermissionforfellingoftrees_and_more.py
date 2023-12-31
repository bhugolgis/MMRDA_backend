# Generated by Django 4.1.5 on 2023-08-02 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training', '0019_rename_images_contactusimage_images1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preconstructionstage',
            name='RulesOfPermissionForFellingOfTrees',
            field=models.CharField(blank=True, default='Forest Conservation Act 1980, Guideline as per the department of Environment, Govt. of Maharashtra. Maharashtra (Urban Area) Protection of trees Act 1975', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='preconstructionstage',
            name='RulesOfShiftingofUtilities',
            field=models.CharField(default='High tension power line, water supply pipeline, sewer line, gas pipeline etc. as per MCGM guide lines', max_length=255),
        ),
    ]
