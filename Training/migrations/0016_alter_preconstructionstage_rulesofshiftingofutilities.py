# Generated by Django 4.1.5 on 2023-01-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training', '0015_constructionstage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preconstructionstage',
            name='RulesOfShiftingofUtilities',
            field=models.CharField(default='High tension power line, water supply pipeline, sewer\n                                                                            line, gas pipeline etc. as per MCGM guide lines', max_length=255),
        ),
    ]
