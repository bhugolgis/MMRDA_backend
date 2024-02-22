from django.db import models
from Auth.models import User
from django.db.models.signals import post_save
from django.contrib.gis.db import models
from django.utils import timezone
from MMRDA import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
# Create your models here.

# ----------------------------------SOCIAL MONITORING MODLES----------------------------------------
def validate_location_precision(value):
    """
    The function `validate_location_precision` checks if a given location value has at most 6 decimal
    places.
    
    :param value: The `value` parameter is expected to be a tuple containing two elements: the latitude
    and longitude coordinates of a location
    """
    # Ensure that the value has at most 6 decimal places
    if isinstance(value, tuple) and len(value) == 2:
        lat, lon = value
        if isinstance(lat, float) and isinstance(lon, float):
            if len(str(lat).split('.')[-1]) > 6 or len(str(lon).split('.')[-1]) > 6:
                raise ValidationError("The location must have at most 6 digits after the decimal point.")
            


# The above class is an abstract base class with fields for quarter, packages, location, and date of
# monitoring.
class Baseclass(models.Model):
    quarter = models.CharField(max_length=255, null=True, blank=True)
    packages = models.CharField(max_length=255,  null=True, blank=True)
    location = models.PointField(null=True, blank=True  , validators=[validate_location_precision])
    dateOfMonitoring = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


# The `labourcampDetails` class is a model in Django that represents details of a labour camp,
# including the user, camp name, camp ID, capacity, images, and location.
class labourcampDetails(models.Model):
    user = models.ForeignKey(User , related_name='labourcampDetails_user' , on_delete=models.SET_NULL , blank = True , null = True )
    LabourCampName = models.CharField(max_length=255, blank=True, null=True)
    LabourCampId = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.CharField(max_length=50 , blank = True , null = True )
    image = ArrayField(models.CharField( max_length=255, blank=True, null=True), blank = True , null = True )
    location = models.PointField(blank=True, null=True)

    def __str__(self):
        return self.LabourCampName


# The class PAP is a subclass of Baseclass and represents a Person Affected by a Project, with various
# attributes such as user, PAPID, nameOfPAP, addressLine1, streetName, pincode, dateOfIdentification,
# eligibility, categoryOfPap, typeOfStructure, areaOfAsset, legalStatus, legalDocuments, actionTaken,
# notAgreedReason, presentPhotograph, and remarks.
class PAP(Baseclass):
    user = models.ForeignKey(User, related_name='papUser', on_delete=models.CASCADE, null=True)
    PAPID = models.CharField( max_length=255,unique=True)
    cadastralMapID = models.CharField( max_length=255,unique=True, blank=True, null=True)
    cadastralMapDocuments = models.CharField(max_length=255, blank=True, null=True)
    nameOfPAP = models.CharField(max_length=255, blank=True, null=True)
    firstName = models.CharField(max_length=255, blank=True, null=True)
    middleName = models.CharField(max_length=255, blank=True, null=True)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    addressLine1 = models.TextField(max_length=255, blank=True, null=True)
    streetName = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.PositiveIntegerField(blank=True, null=True)
    dateOfIdentification = models.DateField(blank=True, null=True)
    eligibility = models.CharField(max_length=255, null=True, blank=True)
    categoryOfPap = models.CharField( max_length=255,  null=True, blank=True)
    # individualLandAsset = models.PositiveIntegerField(blank=True, null=True)
    typeOfStructure = models.CharField( max_length=255,  null=True, blank=True)
    areaOfAsset = models.BigIntegerField(blank=True, null=True)
    legalStatus = models.CharField( max_length=255,  null=True, blank=True)
    legalDocuments = models.CharField(max_length=255, blank=True, null=True)
    actionTaken = models.CharField(max_length=100, null=True, blank=True)
    notAgreedReason = models.TextField(max_length=255, blank=True, null=True)
    presentPhotograph = models.CharField( max_length=255, blank=True, null=True)
    remarks = models.TextField(max_length=255, blank=True, null=True)


# The Rehabilitation class is a subclass of the Baseclass and contains various fields related to
# rehabilitation information such as user, location, ID, date of rehabilitation, PAP ID, category of
# PAP, PAP name, cash compensation, compensation status, type of compensation, address, shifting
# allowance, livelihood support, training, type of structure, area of tenement, relocation allowance,
# financial support, community engagement, documents, remarks, and various photographs.
class Rehabilitation(Baseclass):
    user = models.ForeignKey(User, related_name='rehabilitationUser', on_delete=models.CASCADE, blank=True)
    location = models.PointField(null=True, blank=True)
    ID = models.ForeignKey( PAP, related_name='rehabilitation', on_delete=models.CASCADE)
    dateOfRehabilitation = models.DateField(blank=True, null=True)
    PAPID = models.CharField(max_length=255, blank=True, null=True)
    categoryOfPap = models.CharField( max_length=255,  null=True, blank=True)
    PAPName = models.CharField(max_length=255, blank=True, null=True)

    cashCompensation = models.PositiveIntegerField(blank=True, null=True)
    compensationStatus = models.CharField( max_length=255, null=True, blank=True)

    typeOfCompensation = models.CharField( max_length=255, null=True, blank=True)
    otherCompensationType = models.CharField(max_length=255, null=True, blank=True)

    addressLine1 = models.TextField(max_length=255, blank=True, null=True)
    streetName = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.BigIntegerField(blank=True, null=True)

    isShiftingAllowance = models.BooleanField(blank=True , null = True)
    shiftingAllowanceAmount = models.PositiveIntegerField(blank=True, null=True)

    isLivelihoodSupport = models.BooleanField(blank=True , null = True)
    livelihoodSupportAmount = models.BigIntegerField(blank=True, null=True)
    livelihoodSupportCondition = models.CharField( max_length=255, blank=True, null=True)
    
    livelihoodSupportRemarks = models.TextField(max_length=255, blank=True, null=True)

    isTraining = models.BooleanField(blank=True , null = True)
    trainingCondition = models.CharField( max_length=255,  blank=True, null=True)
    
    trainingRemarks = models.TextField(max_length=255, blank=True, null=True)

    typeOfStructure = models.CharField(max_length=255, blank=True)
    areaOfTenament = models.BigIntegerField(blank=True, null=True)
    

    isRelocationAllowance = models.CharField( max_length=255, blank=True, null=True)
    RelocationAllowanceAmount = models.PositiveIntegerField(blank=True, null=True)

    isfinancialSupport = models.BooleanField(blank=True, null=True)
    financialSupportAmount = models.PositiveIntegerField(blank=True, null=True)

    isCommunityEngagement = models.BooleanField(blank=True, null=True)
    isEngagementType = models.CharField(max_length=255, blank=True, null=True)

    
    documents = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(max_length=255, blank=True, null=True)
    
    livelihoodSupportPhotograph = models.CharField(max_length=255, blank=True, null=True)
    trainingPhotograph = models.CharField(max_length=255, blank=True, null=True)
    tenamentsPhotograph = models.CharField(max_length=255, blank=True, null=True)
    photographs = models.CharField(max_length=255, blank=True, null=True)


    
        
    


# Labour  Camp Model ----------------------------------------------
# The above code defines two classes, LabourCamp and ConstructionSiteDetails, which are subclasses of
# the Baseclass.
class LabourCamp(Baseclass):
    user = models.ForeignKey(User, related_name='LaboursCamp_User',on_delete=models.CASCADE, blank=True, null=True)
    labourCampId = models.CharField(max_length=255  , blank = True , null = True )
    labourCampName = models.CharField(max_length=255 , blank = True , null = True)

    isToilet = models.BooleanField(max_length=255, blank=True)
    toiletCondition = models.CharField(max_length=255, blank=True, null=True)
    toiletPhotograph = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    toiletRemarks = models.TextField(max_length=255, null=True, blank=True)

    isDrinkingWater = models.BooleanField(blank=True)
    drinkingWaterCondition = models.CharField( max_length=255, blank=True, null=True)
    drinkingWaterPhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    drinkingWaterRemarks = models.TextField(max_length=255, null=True, blank=True)

    isDemarkationOfPathways = models.BooleanField(blank=True)
    demarkationOfPathwaysCondition = models.CharField(max_length=255, blank=True, null=True)
    demarkationOfPathwaysPhotographs =ArrayField(models.CharField( max_length=255, blank=True, null=True))
    demarkationOfPathwaysRemark = models.TextField(max_length=255, blank=True, null=True)

    isSignagesLabeling = models.BooleanField(blank=True)
    signagesLabelingCondition = models.CharField( max_length=255,  blank=True, null=True)
    signagesLabelingPhotographs =ArrayField(models.CharField( max_length=255, blank=True, null=True))
    signagesLabelingRemarks = models.TextField( max_length=255,  blank=True, null=True)

    isKitchenArea = models.BooleanField(blank=True, null=True)
    kitchenAreaCondition = models.CharField( max_length=255,  blank=True, null=True)
    kitchenAreaPhotographs =ArrayField(models.CharField( max_length=255, blank=True, null=True))
    kitchenAreaRemarks = models.TextField(max_length=255,  blank=True, null=True)

    isFireExtinguish = models.BooleanField(blank=True, null=True)
    fireExtinguishCondition = models.CharField( max_length=255, blank=True, null=True)
    fireExtinguishPhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    fireExtinguishRemarks = models.TextField( max_length=255, blank=True, null=True)

    isRoomsOrDoms = models.BooleanField(blank=True, null=True)
    roomsOrDomsCondition = models.CharField( max_length=255,  blank=True, null=True, )
    roomsOrDomsPhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    roomsOrDomsRemarks = models.TextField( max_length=255,  blank=True, null=True)

    isSegregationOfWaste = models.BooleanField(blank=True)
    segregationOfWasteCondition = models.CharField( max_length=255,  blank=True, null=True)
    segregationOfWastePhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    segregationOfWasteRemarks = models.TextField( max_length=255,  blank=True, null=True)

    isRegularHealthCheckup = models.BooleanField(blank=True)
    regularHealthCheckupCondition = models.CharField( max_length=255,   blank=True, null=True)
    regularHealthCheckupPhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    regularHealthCheckupRemarks = models.TextField(max_length=255,  blank=True, null=True)

    isAvailabilityOfDoctor = models.BooleanField(blank=True)
    availabilityOfDoctorCondition = models.CharField( max_length=255,  blank=True, null=True)
    availabilityOfDoctorPhotographs =ArrayField(models.CharField( max_length=255, blank=True, null=True))
    availabilityOfDoctorRemarks = models.TextField(max_length=255,  blank=True, null=True)

    isFirstAidKit = models.BooleanField(blank=True)
    firstAidKitCondition = models.CharField( max_length=255,  blank=True, null=True)
    firstAidKitPhotographs =    (models.CharField( max_length=255, blank=True, null=True))
    firstAidKitRemarks = models.TextField(max_length=255,  blank=True, null=True)

    transportationFacility = models.BooleanField(blank=True, null=True)
    transportationFacilityCondition = models.CharField(max_length=255,  blank=True, null=True)

    modeOfTransportation = models.CharField(max_length=255, blank=True, null=True)
    distanceFromSite = models.PositiveIntegerField(blank=True, null=True)

    photographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    documents =ArrayField(models.CharField( max_length=255, blank=True, null=True))
    remarks = models.TextField(max_length=255,  null=True)



class ConstructionSiteDetails(Baseclass):
    user = models.ForeignKey(User, related_name='constructionsite_user',
                             on_delete=models.CASCADE, blank=True, null=True)

    constructionSiteName = models.CharField( max_length=255,   blank=True, null=True)
    constructionSiteId = models.CharField(max_length=255,  blank=True, null=True)

    isDemarkationOfPathways = models.BooleanField(blank=True)
    demarkationOfPathwaysCondition = models.CharField(max_length=255, blank=True, null=True)
    demarkationOfPathwaysPhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    demarkationOfPathwaysRemark = models.TextField(max_length=255, blank=True, null=True)

    isSignagesLabelingCheck = models.BooleanField(blank=True)
    signagesLabelingCondition = models.CharField( max_length=255, blank=True, null=True)
    signagesLabelingPhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    signagesLabelingRemarks = models.TextField( max_length=255,  blank=True, null=True)

    isRegularHealthCheckup = models.BooleanField(blank=True)
    regularHealthCheckupCondition = models.CharField( max_length=255, blank=True, null=True)
    regularHealthCheckupPhotographs =ArrayField(models.CharField( max_length=255, blank=True, null=True))
    regularHealthCheckupRemarks = models.TextField( max_length=255,  blank=True, null=True)

    isAvailabilityOfDoctor = models.BooleanField(blank=True)
    availabilityOfDoctorCondition = models.CharField(max_length=255, blank=True, null=True)
    availabilityOfDoctorPhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    availabilityOfDoctorRemarks = models.TextField( max_length=255,  blank=True, null=True)

    isFirstAidKit = models.BooleanField(blank=True)
    firstAidKitCondition = models.CharField(max_length=255, blank=True, null=True)
    firstAidKitPhotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    firstAidKitRemarks = models.TextField(max_length=255,  blank=True, null=True)

    isDrinkingWaterCheck = models.BooleanField(blank=True)
    drinkingWaterCondition = models.CharField(  max_length=255, blank=True,  null=True)
    drinkingWaterPhotographs =ArrayField(models.CharField( max_length=255, blank=True, null=True))
    drinkingWaterRemarks = models.TextField( max_length=255, null=True, blank=True)

    isToilet = models.BooleanField(max_length=255, blank=True, null=True)
    toiletCondition = models.CharField(max_length=255, blank=True, null=True)
    toiletPhotograph =  ArrayField(models.CharField( max_length=255, blank=True, null=True))
    toiletRemarks = models.TextField(max_length=255, null=True, blank=True)


    genralphotographs = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    documents = ArrayField(models.CharField( max_length=255, blank=True, null=True))
    remarks = models.TextField(max_length=255, blank=True, null=True)
