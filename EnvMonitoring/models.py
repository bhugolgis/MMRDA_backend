from django.db import models
from Auth.models import User
from django.db.models.signals import post_save
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
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

# Why is user a field, what is it used for ? testing/debugging which user created which data? or to track
class  Air(Baseclass):
    # sensor = models.ForeignKey(sensors , related_name="sensor_name" , on_delete=models.CASCADE , null = True , blank = True)
    user = models.ForeignKey(User, related_name='airs_user', on_delete=models.CASCADE, null=True, blank=True)
    PM10 = models.FloatField(blank=True, default=0, null=True)
    PM2_5 = models.FloatField(blank=True, default=0, null=True)
    SO2 = models.FloatField(blank=True, default=0, null=True)
    NOx = models.FloatField(blank=True, default=0, null=True)
    CO = models.FloatField(blank=True, default=0, null=True)
    AQI = models.FloatField(blank=True, default=0, null=True)
    Remarks = models.TextField(blank=True, max_length=255, null=True)
    place_location = models.CharField(max_length=255, null=True, blank=True)


    

# there are two types of water parameters, ground water and surface water, we have used ground water and calculated wqi for ground water
class water(Baseclass):
    dateOfMonitoring = None
    dateOfMonitoringTwo =  models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='waters', on_delete=models.CASCADE , null= True   , blank=True)
    qualityOfWater = models.CharField(max_length=255, null=True, blank=True)
    sourceOfWater = models.CharField(max_length=255, null=True, blank=True)
    waterDisposal = models.CharField(max_length=255, null=True, blank=True)
    pH = models.CharField(max_length=255, null=True, blank=True)
    trueColor = models.CharField(max_length=255, null=True, blank=True)
    turbidity = models.CharField(max_length=255, null=True, blank=True)
    odour = models.CharField(max_length=255, null=True, blank=True)
    totalDissolvedSolids = models.CharField(max_length=255, null=True, blank=True)
    totalAlkalinityAsCaCO3 = models.CharField(max_length=255, null=True, blank=True)
    totalHardnessAsCaCO3 = models.CharField(max_length=255, null=True, blank=True)
    calcium = models.CharField(max_length=255, null=True, blank=True)
    magnesium = models.CharField(max_length=255, null=True, blank=True)
    chlorides = models.CharField(max_length=255, null=True, blank=True)
    fluoride = models.CharField(max_length=255, null=True, blank=True)
    sulphate = models.CharField(max_length=255, null=True, blank=True)
    nitrate = models.CharField(max_length=255, null=True, blank=True)
    iron = models.CharField(max_length=255, null=True, blank=True)
    zinc = models.CharField(max_length=255, null=True, blank=True)
    copper = models.CharField(max_length=255, null=True, blank=True)
    aluminum = models.CharField(max_length=255, null=True, blank=True)
    nickel = models.CharField(max_length=255, null=True, blank=True)
    manganese = models.CharField(max_length=255, null=True, blank=True)
    phenolicCompounds = models.CharField(max_length=255, null=True, blank=True)
    sulphide = models.CharField(max_length=255, null=True, blank=True)
    cadmium = models.CharField(max_length=255, null=True, blank=True)
    cyanide = models.CharField(max_length=255, null=True, blank=True)
    lead = models.CharField(max_length=255, null=True, blank=True)
    mercury = models.CharField(max_length=255, null=True, blank=True)
    totalArsenic = models.CharField(max_length=255, null=True, blank=True)
    totalChromium = models.CharField(max_length=255, null=True, blank=True)
    totalColiform = models.CharField(max_length=255, null=True, blank=True) # not added in the forms
    eColi = models.CharField(max_length=255, null=True, blank=True) # not added in the forms
    WQI = models.FloatField(blank=True, default=0, null=True)
    place_location = models.CharField(max_length=255, null=True, blank=True)


class Noise(Baseclass):
    dateOfMonitoring = None
    dateOfMonitoringThree = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="noises", on_delete=models.CASCADE , blank=True )
    noiseLevel = models.IntegerField( null=True, blank=True)
    noiseLevel_day = models.FloatField( null=True, blank=True)
    noiseLevel_night = models.FloatField( null=True, blank=True)
    monitoringPeriod = models.CharField(max_length=255, null=True, blank=True)
    monitoringPeriod_day = models.CharField(max_length=255, null=True, blank=True)
    monitoringPeriod_night = models.CharField(max_length=255, null=True, blank=True)
    typeOfArea = models.CharField( max_length = 255, null=True, blank=True)
    isWithinLimit_day = models.CharField( max_length = 255, null=True, blank=True)
    isWithinLimit_night = models.CharField( max_length = 255, null=True, blank=True)
    place_location = models.CharField(max_length=255, null=True, blank=True)


# Also known as Identified Tree (in portal only existing tree existing)
class ExistingTreeManagment(Baseclass):
    user = models.ForeignKey( User ,  related_name="Tree_user" , on_delete= models.CASCADE , blank = True)
    treeID = models.CharField(max_length=255,null = True ,blank = True , unique=True)
    commanName = models.CharField(max_length=255, blank=True, null=True)
    botanicalName = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
    actionTaken = models.CharField(max_length=255 ,blank=True, null=True)
    noOfTreeCut = models.IntegerField(null=True, blank=True)
    documents =ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    photographs = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    remarks = models.TextField(blank=True, null=True )
    place_location = models.CharField(max_length=255, null=True, blank=True)



class NewTreeManagement(Baseclass):
    user = models.ForeignKey(User , related_name="newTree_users" , on_delete=models.CASCADE , blank = True )
    tree = models.OneToOneField( ExistingTreeManagment , related_name= 'ExistingTreeManagment' , on_delete=models.CASCADE , blank = True , null = True )
    location = models.PointField(null = True , blank=True)
    commanName = models.CharField(max_length=255, blank=True, null=True)
    botanicalName = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
    documents =ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    photographs = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    remarks = models.TextField(max_length= 255 , null = True , blank = True)
    place_location = models.CharField(max_length=255, null=True, blank=True)


# Also known as Waste Management
class WasteTreatments(Baseclass):
    #wastetype = models.CharField(max_length=255,  null=True, blank=True)
    user = models.ForeignKey(User, related_name="waste_treatments", on_delete=models.CASCADE, blank=True)
    isGISPermitsTransportation = models.BooleanField(blank=True, null=True)
    GISPermitsTransportationDocuments = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    isTransportationVechicalHasPermission = models.BooleanField(blank=True, null=True)
    TransportationVechicalHasPermissionDocuments = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    waste_collecting_location = models.CharField(max_length=255, null=True, blank=True)
    

    # Hazardous Waste
    iswasteOilQnt = models.BooleanField(blank=True, null=True)
    wasteOilQnt = models.FloatField(null=True, blank=True) # liter
    isCCPCPaintSludgeQnt = models.BooleanField(blank=True, null=True)
    CCPCPaintSludgeQnt = models.FloatField(null=True, blank=True) # Kg
    isfilterQnt = models.BooleanField(blank=True, null=True)
    filterQnt = models.FloatField(null=True, blank=True) # litre
    isairFiltersQnt = models.BooleanField(blank=True, null=True)
    airFiltersQnt = models.FloatField(null=True, blank=True) # liter
    isusedCartridgesQnt = models.BooleanField(blank=True, null=True)
    usedCartridgesQnt = models.FloatField(null=True, blank=True) # litre

    # Recyclable Waste

    isplasticQnt = models.BooleanField(blank=True, null=True)
    plasticQnt = models.FloatField(null=True, blank=True) # Kg
    ispaperQnt = models.BooleanField(blank=True, null=True)
    paperQnt = models.FloatField(null=True, blank=True) # Kg
    iswoodQnt = models.BooleanField(blank=True, null=True)
    woodQnt = models.FloatField(null=True, blank=True) # Kg
    isbottlesQnt = models.BooleanField(blank=True, null=True)
    bottlesQnt = models.FloatField(null=True, blank=True) # Kg
    isrubberQnt = models.BooleanField(blank=True, null=True)
    rubberQnt = models.FloatField(null=True, blank=True) # Kg

    # Bio Degradable Waste
    isbioDegradableQuantity = models.BooleanField(blank=True, null=True)
    bioDegradableQuantity = models.FloatField(null=True, blank=True) # Food and Vegetable waste

    # Bio Medical Waste
    isbioMedicalQuantity = models.BooleanField(blank=True, null=True)
    bioMedicalQuantity = models.FloatField(null=True, blank=True) # Syringe, Needles, Cotton & Bandages

    # Metal Scrape
    ismetalScrapeQuantity = models.BooleanField(blank=True, null=True)
    metalScrapeQuantity = models.FloatField(null=True, blank=True) # Kg
    
    # Construction Waste
    isconstructionWasteQuantity = models.BooleanField(blank=True, null=True)
    constructionWasteQuantity = models.FloatField(null=True, blank=True) # Kg
    
    # E Waste
    iseWasteQuantity = models.BooleanField(blank=True, null=True)
    eWasteQuantity = models.FloatField(null=True, blank=True) # Kg
    waste_handlingLocation = models.PointField(null=True, blank=True)
   
    waste_disposing_location = models.CharField(max_length=255, null=True, blank=True)
    # Documents and Remarks
    documents =ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    photographs = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    
    


class MaterialManegmanet(Baseclass):
    
    user = models.ForeignKey(User, related_name="MaterialSourcing", on_delete=models.CASCADE, blank=True)
    material_source_location = models.CharField(max_length=255, null=True, blank=True)

    
    #Material Management Details
    typeOfMaterial = models.CharField(max_length=255,  null=True, blank=True)
    materialStorageType = models.CharField(max_length=255 , blank = True , null = True)
    materialStorageCondition = models.CharField(max_length = 255 , blank = True , null = True)
    source = models.CharField(max_length=255,  null=True, blank=True)
    sourceOfQuarry = models.CharField(max_length=255,  null=True, blank=True)
    materialStoragePhotograph = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    approvals = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    
    storageLocation = models.PointField(blank = True , null = True)
    material_storage_location = models.CharField(max_length=255, null=True, blank=True)
    
   

    #Documents and Remarks
    documents =ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    photographs = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)



