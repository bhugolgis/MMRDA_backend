from django.db import models
from Auth.models import User
from django.db.models.signals import post_save
from django.contrib.gis.db import models
from django.utils import timezone
from MMRDA import settings
from django.core.exceptions import ValidationError
# Create your models here.

# ----------------------------------SOCIAL MONITORING MODLES----------------------------------------
def validate_location_precision(value):
    # Ensure that the value has at most 6 decimal places
    if isinstance(value, tuple) and len(value) == 2:
        lat, lon = value
        if isinstance(lat, float) and isinstance(lon, float):
            if len(str(lat).split('.')[-1]) > 6 or len(str(lon).split('.')[-1]) > 6:
                raise ValidationError("The location must have at most 6 digits after the decimal point.")

class Baseclass(models.Model):
    quarter = models.CharField(max_length=255, null=True, blank=True)
    packages = models.CharField(max_length=255,  null=True, blank=True)
    location = models.PointField(null=True, blank=True  , validators=[validate_location_precision])
    dateOfMonitoring = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class labourcampDetails(models.Model):
    LabourCampName = models.CharField(max_length=255, blank=True, null=True)
    LabourCampId = models.CharField(max_length=255, blank=True, null=True)
    location = models.PointField(blank=True, null=True)

    def __str__(self):
        return self.LabourCampName


class PAP(Baseclass):
    user = models.ForeignKey(User, related_name='papUser',
                             on_delete=models.CASCADE, null=True)
    PAPID = models.CharField( max_length=255,unique=True)
    nameOfPAP = models.CharField(max_length=255, blank=True, null=True)
    addressLine1 = models.TextField(max_length=255, blank=True, null=True)
    streetName = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.PositiveIntegerField(blank=True, null=True)
    dateOfIdentification = models.DateField(blank=True, null=True)
    eligibility = models.CharField(max_length=255, null=True, blank=True)
    categoryOfPap = models.CharField(
        max_length=255,  null=True, blank=True)
    # individualLandAsset = models.PositiveIntegerField(blank=True, null=True)
    typeOfStructure = models.CharField(
        max_length=255,  null=True, blank=True)
    areaOfAsset = models.BigIntegerField(blank=True, null=True)
    legalStatus = models.CharField(
        max_length=255,  null=True, blank=True)
    legalDocuments = models.CharField(max_length=255, blank=True, null=True)
    actionTaken = models.CharField(
        max_length=100, null=True, blank=True)
    notAgreedReason = models.TextField(max_length=255, blank=True, null=True)
    presentPhotograph = models.CharField(
        max_length=255, blank=True, null=True)
    remarks = models.TextField(max_length=255, blank=True, null=True)


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
class LabourCamp(Baseclass):
    user = models.ForeignKey(User, related_name='LaboursCamp_User',
                             on_delete=models.CASCADE, blank=True, null=True)
    labourCampId = models.CharField(max_length=255  , blank = True , null = True )
    labourCampName = models.CharField(max_length=255 , blank = True , null = True)

    isToilet = models.BooleanField(max_length=255, blank=True)
    toiletCondition = models.CharField(max_length=255, blank=True, null=True)
    toiletPhotograph = models.ImageField(
        upload_to='Labour Camp/toilet_photographs/', blank=True, null=True)
    toiletRemarks = models.TextField(max_length=255, null=True, blank=True)

    isDrinkingWater = models.BooleanField(blank=True)
    drinkingWaterCondition = models.CharField(
        max_length=255, blank=True, null=True)
    drinkingWaterPhotographs = models.ImageField(
        upload_to='Labour Camp/drinkingWater_photographs/', null=True, blank=True)
    drinkingWaterRemarks = models.TextField(
        max_length=255, null=True, blank=True)

    isDemarkationOfPathways = models.BooleanField(blank=True)
    demarkationOfPathwaysCondition = models.CharField(
        max_length=255, blank=True, null=True)
    demarkationOfPathwaysPhotographs = models.ImageField(
        upload_to='Labour Camp/demarkingPathways_photographs/',  blank=True, null=True)
    demarkationOfPathwaysRemark = models.TextField(
        max_length=255, blank=True, null=True)

    isSignagesLabeling = models.BooleanField(blank=True)
    signagesLabelingCondition = models.CharField(
        max_length=255,  blank=True, null=True)
    signagesLabelingPhotographs = models.ImageField(
        upload_to='Labour Camp/signagesLabeling_Photographs/',  blank=True, null=True)
    signagesLabelingRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isKitchenArea = models.BooleanField(blank=True, null=True)
    kitchenAreaCondition = models.CharField(
        max_length=255,  blank=True, null=True)
    kitchenAreaPhotographs = models.ImageField(
        upload_to='Labour Camp/KitchenArea _photographs/', blank=True, null=True)
    kitchenAreaRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isFireExtinguish = models.BooleanField(blank=True, null=True)
    fireExtinguishCondition = models.CharField(
        max_length=255, blank=True, null=True)
    fireExtinguishPhotographs = models.ImageField(
        upload_to='Labour Camp/fireExtinguish_photographs/',   blank=True, null=True)
    fireExtinguishRemarks = models.TextField(
        max_length=255, blank=True, null=True)

    isRoomsOrDoms = models.BooleanField(blank=True, null=True)
    roomsOrDomsCondition = models.CharField(
        max_length=255,  blank=True, null=True, )
    roomsOrDomsPhotographs = models.ImageField(
        upload_to='Labour Camp/rooms_photographs/', blank=True, null=True)
    roomsOrDomsRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isSegregationOfWaste = models.BooleanField(blank=True)
    segregationOfWasteCondition = models.CharField(
        max_length=255,  blank=True, null=True)
    segregationOfWastePhotographs = models.ImageField(
        upload_to='labour Camp/segrigationOfWaste_Photographs/', blank=True, null=True)
    segregationOfWasteRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isRegularHealthCheckup = models.BooleanField(blank=True)
    regularHealthCheckupCondition = models.CharField(
        max_length=255,   blank=True, null=True)
    regularHealthCheckupPhotographs = models.ImageField(
        upload_to='Labour Camp/RegularHealthCheckup_Photographs/', blank=True, null=True)
    regularHealthCheckupRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isAvailabilityOfDoctor = models.BooleanField(blank=True)
    availabilityOfDoctorCondition = models.CharField(
        max_length=255,  blank=True, null=True)
    availabilityOfDoctorPhotographs = models.ImageField(
        upload_to='Labour Camp/AvailabilityOfDoctor_photographs/',  blank=True, null=True)
    availabilityOfDoctorRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isFirstAidKit = models.BooleanField(blank=True)
    firstAidKitCondition = models.CharField(
        max_length=255,  blank=True, null=True)
    firstAidKitPhotographs = models.ImageField(
        upload_to='Labour Camp/FirstAidKit_photographs/', blank=True, null=True)
    firstAidKitRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    transportationFacility = models.BooleanField(blank=True, null=True)
    transportationFacilityCondition = models.CharField(
        max_length=255,  blank=True, null=True)

    modeOfTransportation = models.CharField(
        max_length=255, blank=True, null=True)
    distanceFromSite = models.PositiveIntegerField(blank=True, null=True)

    photographs = models.CharField(max_length=255, blank=True, null=True)
    documents = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(max_length=255, blank=True, null=True)



class ConstructionSiteDetails(Baseclass):
    user = models.ForeignKey(User, related_name='constructionsite_user',
                             on_delete=models.CASCADE, blank=True, null=True)

    constructionSiteName = models.CharField(
        max_length=255,   blank=True, null=True)
    constructionSiteId = models.CharField(
        max_length=255,  blank=True, null=True)

    isDemarkationOfPathways = models.BooleanField(blank=True)
    demarkationOfPathwaysCondition = models.CharField(
        max_length=255, blank=True, null=True)
    demarkationOfPathwaysPhotographs = models.ImageField(
        upload_to='constructionSite/demarkingPathways_photographs/',  blank=True, null=True)
    demarkationOfPathwaysRemark = models.TextField(
        max_length=255, blank=True, null=True)

    isSignagesLabelingCheck = models.BooleanField(blank=True)
    signagesLabelingCondition = models.CharField(
        max_length=255, blank=True, null=True)
    signagesLabelingPhotographs = models.ImageField(
        upload_to='constructionSite/signagesLabeling_Photographs/',  blank=True, null=True)
    signagesLabelingRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isRegularHealthCheckup = models.BooleanField(blank=True)
    regularHealthCheckupCondition = models.CharField(
        max_length=255, blank=True, null=True)
    regularHealthCheckupPhotographs = models.ImageField(
        upload_to='constructionSite/RegularHealthCheckup_Photographs/', blank=True, null=True)
    regularHealthCheckupRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isAvailabilityOfDoctor = models.BooleanField(blank=True)
    availabilityOfDoctorCondition = models.CharField(
        max_length=255, blank=True, null=True)
    availabilityOfDoctorPhotographs = models.ImageField(
        upload_to='constructionSite/AvailabilityOfDoctor_photographs/',  blank=True, null=True)
    availabilityOfDoctorRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isFirstAidKit = models.BooleanField(blank=True)
    firstAidKitCondition = models.CharField(
        max_length=255, blank=True, null=True)
    firstAidKitPhotographs = models.ImageField(
        upload_to='constructionSite/FirstAidKit_photographs/', blank=True, null=True)
    firstAidKitRemarks = models.TextField(
        max_length=255,  blank=True, null=True)

    isDrinkingWaterCheck = models.BooleanField(blank=True)
    drinkingWaterCondition = models.CharField(
        max_length=255, blank=True,  null=True)
    drinkingWaterPhotographs = models.ImageField(
        upload_to='constructionSite/drinkingWater_photographs/', null=True, blank=True)
    drinkingWaterRemarks = models.TextField(
        max_length=255, null=True, blank=True)

    isToilet = models.BooleanField(max_length=255, blank=True, null=True)
    toiletCondition = models.CharField(max_length=255, blank=True, null=True)
    toiletPhotograph = models.ImageField(
        upload_to='constructionSite/toilet_photographs/', blank=True, null=True)
    toiletRemarks = models.TextField(max_length=255, null=True, blank=True)


    genralphotographs = models.CharField(max_length= 255, blank=True, null=True)
    documents = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(max_length=255, blank=True, null=True)
