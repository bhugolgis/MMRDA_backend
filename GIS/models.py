from django.db import models
from django.contrib.gis.db import models

# Create your models

# Need to remove this table/model
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


class StartEndPoints(models.Model):
    gid = models.AutoField(primary_key=True)
    fid = models.FloatField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'start_end_points'
        

class AllStartEndPoints(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    names = models.CharField(max_length=80, blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_start_end_points'


# Whole Metro Line 4 and 4a layer
class MmrdaAlignment4326(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mmrda_alignment_4326'



class PackageCa08MetroStations(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_08_metro_stations'


class PackageCa08StartEndPoint(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_08_start_end_point'


class MmrdaCa08Alignment4326(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mmrda_ca_08_alignment_4326'
        

class PackageCa09MetroStations(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_09_metro_stations'


class PackageCa09StartEndPoint(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_09_start_end_point'


class MmrdaCa09Alignment4326(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mmrda_ca_09_alignment_4326'


class PackageCa10MetroStations(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_10_metro_stations'


class PackageCa10StartEndPoint(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_10_start_end_point'


class MmrdaCa10Alignment4326(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mmrda_ca_10_alignment_4326'


class PackageCa11MetroStations(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_11_metro_stations'


class PackageCa11StartEndPoint(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_11_start_end_point'


class MmrdaCa11Alignment4326(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mmrda_ca_11_alignment_4326'


class PackageCa12MetroStations(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_12_metro_stations'


class PackageCa12StartEndPoint(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_12_start_end_point'


class MmrdaCa12Alignment4326(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mmrda_ca_12_alignment_4326'


class PackageCa54MetroStations(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_54_metro_stations'


class PackageCa54StartEndPoint(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.FloatField(blank=True, null=True)
    geom = models.MultiPointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_ca_54_start_end_point'


class MmrdaCa54Alignment4326(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mmrda_ca_54_alignment_4326'