from django.db import models
from django.contrib.gis.db import models

# Create your models h



class Projectaffectedperson(models.Model):
    gid = models.AutoField(primary_key=True)
    pap_id = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    category = models.CharField(max_length=254, blank=True, null=True)
    date = models.CharField(max_length=254, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projectAffectedPerson'

class RehabilitatedPap(models.Model):
    gid = models.AutoField(primary_key=True)
    pap_id = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    date_ident = models.CharField(max_length=254, blank=True, null=True)
    category = models.CharField(max_length=254, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rehabilitations'