from django.db import models
from Auth.models import User
from django.db.models.signals import post_save
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
# Create your models here.

def validate_location_precision(value):
  
    if isinstance(value, tuple) and len(value) == 2:
        lat, lon = value
        if isinstance(lat, float) and isinstance(lon, float):
            if len(str(lat).split('.')[-1]) > 6 or len(str(lon).split('.')[-1]) > 6:
                raise ValidationError("The location must have at most 6 digits after the decimal point.")

# Abstarct Baseclass for EnvMonitoring for common field
class Baseclass(models.Model):
    quarter = models.CharField(max_length=255,  null=True, blank=True)
    month = models.CharField(max_length=255, null=True, blank=True)
    packages = models.CharField(max_length=255, null=True, blank=True)
    location = models.PointField(null=True, blank=True  , validators=[validate_location_precision])
    dateOfMonitoring = models.DateField(null=True, blank=True )
    class Meta:
        abstract = True


class sensors(models.Model):
    Name = models.CharField(max_length=100 , blank = True , null = True )
    ID = models.CharField(max_length=100 , blank= True , null = True )
    location = models.PointField(blank = True , null = True )

    def __str__(self) -> str:
        return self.Name


class  Air(Baseclass):
    # sensor = models.ForeignKey(sensors , related_name="sensor_name" , on_delete=models.CASCADE , null = True , blank = True)
    user = models.ForeignKey( User, related_name='airs_user', on_delete=models.CASCADE , null= True   , blank=True)
    PM10 = models.CharField(max_length= 50 , blank= True , default= 0, null= True)
    standardPM10 = models.FloatField(blank= True , default=100.00 , null= True)
    SO2 = models.CharField(max_length= 50 , blank= True , default= 0, null= True)
    standardSO2 = models.FloatField(blank= True , default = 80.00 , null= True)
    O3 = models.CharField(max_length= 50 , blank= True , default= 0, null= True)
    standardO3 = models.FloatField(blank= True , default = 100.00 , null= True)
    NOx = models.CharField( max_length= 50 , blank= True , default= 0, null = True)
    standardNOx = models.FloatField(blank= True , default = 80.00 , null= True)
    CO = models.CharField(max_length=50, blank= True, null=True)
    AQI = models.CharField(max_length= 50 , blank= True , default= 0, null = True) 
    Remarks = models.TextField ( blank = True, max_length  = 255, null = True )

class water(Baseclass):
    dateOfMonitoring = None
    dateOfMonitoringTwo =  models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='waters', on_delete=models.CASCADE , null= True   , blank=True)
    qualityOfWater = models.CharField(max_length=255, null=True, blank=True)
    sourceOfWater = models.CharField(max_length=255, null=True, blank=True)
    waterDisposal = models.CharField(max_length=255, null=True, blank=True)


class Noise(Baseclass):
    dateOfMonitoring = None
    dateOfMonitoringThree = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="noises", on_delete=models.CASCADE , blank=True )
    noiseLevel = models.IntegerField( null=True, blank=True)
    noiseLevel_day = models.IntegerField( null=True, blank=True)
    noiseLevel_night = models.IntegerField( null=True, blank=True)
    monitoringPeriod = models.CharField(
        max_length=255, null=True, blank=True)
    monitoringPeriod_day = models.CharField(
        max_length=255, null=True, blank=True)
    monitoringPeriod_night = models.CharField(
        max_length=255, null=True, blank=True)
    typeOfArea = models.CharField( max_length = 255, null=True, blank=True)
    

   


class ExistingTreeManagment(Baseclass):
    user = models.ForeignKey( User ,  related_name="Tree_user" , on_delete= models.CASCADE , blank = True)
    treeID = models.CharField(max_length=255,null = True ,blank = True , unique=True)
    commanName = models.CharField(max_length=255, blank=True, null=True)
    botanicalName = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
    actionTaken = models.CharField(max_length=255 ,blank=True, null=True)
    noOfTreeCut = models.IntegerField(null=True, blank=True)
    photographs = models.ImageField(upload_to="Existingtree_photos/", null=True, blank=True)
    documents = models.FileField(upload_to='existingTree_documents/', null = True , blank=True)
    remarks = models.TextField(blank=True, null=True )
    

class NewTreeManagement(Baseclass):
    user = models.ForeignKey(User , related_name="newTree_users" , on_delete=models.CASCADE , blank = True )
    tree = models.OneToOneField( ExistingTreeManagment , related_name= 'ExistingTreeManagment' , on_delete=models.CASCADE , blank = True , null = True )
    location = models.PointField(null = True , blank=True)
    commanName = models.CharField(max_length=255, blank=True, null=True)
    botanicalName = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)   
    photographs = models.ImageField(upload_to="newTree_photographs/", null=True, blank=True)
    documents = models.FileField(upload_to="newTree_documents/", null  = True, blank=True  )
    remarks = models.TextField(max_length= 255 , null = True , blank = True)
   


class WasteTreatments(Baseclass):
    user = models.ForeignKey(
        User, related_name="waste_treatments", on_delete=models.CASCADE, blank=True)
    wastetype = models.CharField(
        max_length=255,  null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    wastehandling = models.CharField(
        max_length=255, blank=True, null=True)
    wasteHandlingLocation = models.PointField(null=True, blank=True)
    photographs = models.ImageField(upload_to='waste_photographs/' ,null=True, blank=True)
    documents = models.FileField(upload_to='waste_documents' , null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)


class MaterialManegmanet(Baseclass):
    user = models.ForeignKey(User, related_name="MaterialSourcing", on_delete=models.CASCADE, blank=True)
    typeOfMaterial = models.CharField(max_length=255,  null=True, blank=True)
    source = models.CharField(max_length=255,  null=True, blank=True)
    sourceOfQuarry = models.CharField(max_length=255,  null=True, blank=True)
    storageLocation = models.PointField(blank = True , null = True)

    materialStorageType = models.CharField(max_length=255 , blank = True , null = True)
    materialStorageCondition = models.CharField(max_length = 255 , blank = True , null = True)
    materialStoragePhotograph = models.ImageField(upload_to = 'MaterialManegment/materailStorage_Photograph' , blank = True , null = True)

    approvals = models.FileField(null=True, blank=True)
    
    photographs = models.ImageField(upload_to='MaterialManegment/materialsourcing_photographs/',null=True, blank=True)
    documents = models.FileField(upload_to='MaterialManegment/materialsourcing_documents', null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)



