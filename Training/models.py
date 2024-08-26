from django.db import models
from Auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon, LineString
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField


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


class Baseclass(models.Model):
    quarter = models.CharField(max_length=255, null=True, blank=True)
    packages = models.CharField(max_length=255,   null=True, blank=True)
    location = models.PointField(null=True, blank=True  , validators=[validate_location_precision])
    dateOfMonitoring = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


# The `traning` class is a subclass of `Baseclass` and represents a training session with various
# attributes such as user, category, training title, number of attendees, number of times training
# conducted, male and female participants, incharge person, training initiator, conduct date, training
# date, photographs, and documents.
# Training spelling is wrong
class traning(Baseclass):
    user = models.ForeignKey(User, related_name='training_User', on_delete=models.CASCADE)
    category = models.CharField(max_length=255, null=True, blank=True)
    traningTitle = models.CharField(max_length=255, null=True, blank=True)
    noOfAttends = models.IntegerField(null=True, blank=True)
    noOfTimesTrainingConducted = models.IntegerField(default= 0)
    male = models.CharField(max_length=255, null=True, blank=True)
    female = models.CharField(max_length=255, null=True, blank=True)
    inchargePerson = models.CharField(max_length=253, null=True, blank=True)
    traninigInitiatedBy = models.CharField(max_length=255, null=True, blank=True)
    conductDate = models.DateField(auto_now=True, null=True, blank=True)
    traningDate = models.DateField(auto_now=True, null=True, blank=True)
    photographs = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)
    documents = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)


# #----------------------------- PHOTOGRAPHS MODEL-----------------------------------------

# The class "photographs" is a model in Python that represents a collection of photographs with
# various attributes such as title, uploader, location, date, and the actual image file.
class photographs(models.Model):
    # site_name = models.CharField(max_length=255, null=True, blank=True)
    # incharge_person = models.CharField(max_length=244, null=True, blank=True)
    user = models.ForeignKey(
        User, related_name='photograph_User', on_delete=models.CASCADE, blank=True)
    photograph_title = models.CharField(max_length=255, null=True, blank=True)
    photographs_uploaded_by = models.CharField(
        max_length=100, null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    site_photographs = models.ImageField(
        upload_to='site_photographs/', null=True, blank=True)


# ---------------------Occupational Health & safety Model --------------------
# The `occupationalHealthSafety` class represents a model for tracking occupational health and safety
# information, including various conditions, remarks, and incident details.
class occupationalHealthSafety(Baseclass):
    choices = [('Complied' , 'Complied'),('Not-Complied' ,'Not-Complied')]
    user = models.ForeignKey(User, related_name='occupational_health_safety_User', on_delete=models.CASCADE, blank=True)
    # Occupational Facilities
    
    joiningMedicalCheckup = models.BooleanField(null=True, blank=True)
    ppeKit = models.BooleanField(blank=True)
    trainingToWorkers = models.BooleanField(blank=True)
    houseKeeping = models.BooleanField(blank=True)
    
    powerSupplySystem = models.BooleanField(blank=True)
    assemblyArea = models.BooleanField(blank=True)
    ambulanceArrangement = models.BooleanField(blank=True)
    toiletFacility = models.BooleanField(blank=True)
    
    safeMomentPassage = models.BooleanField(blank=True)
    materialKeepingPractice = models.CharField(max_length=255, blank=True, null=True)
    accidentalCheck = models.BooleanField(blank=True)
    safetyGearStatus = models.BooleanField(blank=True)
    
    barricading = models.BooleanField(blank=True)

    # Incident Details
    typeOfIncident = models.CharField(max_length=255,  blank=True, null=True)
    incidentReportingStatus = models.CharField(max_length=255,  blank=True, null=True)
    
    incidentDetails = models.TextField(max_length=255, blank=True, null=True)
    identifiedCauseOfIncident = models.CharField( max_length=255, blank=True, null=True)
    outcome = models.CharField(max_length=255, blank=True, null=True)
    compensationPaid = models.PositiveIntegerField(blank=True, null=True)
    natureOfAccident = models.CharField(max_length=255, blank=True, null=True)
    manDaysLostCount = models.PositiveBigIntegerField(blank=True, null=True)
    manDaysLostReason = models.TextField(max_length=255, blank=True, null=True)

    # Document and Remarks

    documents = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    photographs = ArrayField(models.CharField( max_length=255, blank=True, null=True), default=list, blank=True)
    remarks = models.TextField(max_length=255, blank=True, null=True)


# The Contactus class represents a contact form with fields for name, email, message, location,
# documents, and image, while the ContactusImage class represents images associated with a Contactus
# instance.
class Contactus(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, verbose_name='Email')
    messsage = models.TextField(max_length=255, blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    documents = models.CharField(max_length=255 , blank = True , null = True )
    image = models.CharField(max_length=255 , blank = True , null = True )

class ContactusImage(models.Model):
    contactus = models.ForeignKey(Contactus, on_delete=models.CASCADE, related_name='images' , blank = True    , null = True)
    images1 = models.ImageField(upload_to='contactus/images', max_length=255, blank=True, null=True)
    images2 = models.ImageField(upload_to='contactus/images' , max_length=255, blank=True, null = True )


# The `PreConstructionStage` class represents the pre-construction stage of a project and includes
# fields for various permissions and clearances required.
class PreConstructionStage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    ShiftingofUtilities = models.BooleanField(default=False)
    RulesOfShiftingofUtilities = models.CharField(max_length=255, default='''High tension power line, water supply pipeline, sewer line, gas pipeline etc. as per MCGM guide lines''')
    ResponsibilityOfShiftingofUtilities = models.CharField(max_length=255, blank=True)
    CurrentStatusOfShiftingofUtilities = models.CharField(max_length=255, blank=True, null=True)
    ShiftingofUtilitiesDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    PermissionForFellingOfTrees = models.BooleanField(default=False)
    RulesOfPermissionForFellingOfTrees = models.CharField(max_length=255, default= 'Forest Conservation Act 1980, Guideline as per the department of Environment, Govt. of Maharashtra. Maharashtra (Urban Area) Protection of trees Act 1975' , blank=True, null=True)
    ResponsibilityOfPermissionForFellingOfTrees = models.CharField(max_length=255, blank=True, null=True)
    CurrentStatusPermissionForFellingOfTrees = models.CharField(max_length=255, blank=True, null=True)
    PermissionForFellingOfTreesDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    CRZClearance = models.BooleanField(default=False)
    RulesOfCRZClearance = models.CharField(max_length=255, default='''As per CRZ Rules, MOEF&CC.''', blank=True, null=True)
    ResponsibilityOfCRZClearance = models.CharField(max_length=255, blank=True, null=True)
    CurrentStatusCRZClearance = models.CharField(max_length=255, blank=True, null=True)
    CRZClearanceDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    ForestClearance = models.BooleanField(default=False)
    RulesOfForestClearance = models.CharField(max_length=255, default='''Forest Conservation Act, 1980, amended 1988.''', blank=True, null=True)
    ResponsibilityOfForestClearance = models.CharField(max_length=255, blank=True, null=True)
    CurrentStatusOfForestClearance = models.CharField(max_length=255, blank=True, null=True)
    ForestClearanceDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)


# The above class represents a construction stage with various permissions, rules, responsibilities,
# and current statuses related to environmental regulations and waste management.
class ConstructionStage(models.Model):
    #guideline is rules
    user = models.ForeignKey(User,  on_delete=models.CASCADE,
                             related_name='user_ConstructionStage', null=True)  # User profile
    ConsenttToEstablishOoperate = models.BooleanField(default=False)
    RulesOfConsenttToEstablishOoperate = models.CharField(
        max_length=255, default='Air (Prevention and Control of Pollution) Act')
    ResponsibilityOfConsenttToEstablishOoperate = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusOfConsenttToEstablishOoperate = models.CharField(
        max_length=255, blank=True, null=True)
    ConsenttToEstablishOoperateDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    PermissionForSandMiningFromRiverbed = models.BooleanField(default=False)
    RulesOfSandMiningFromRiverbed = models.CharField(
        max_length=255, default='Environment (Protection) Act')
    ResponsibilityOfSandMiningFromRiverbed = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusOfSandMiningFromRiverbed = models.CharField(
        max_length=255, blank=True, null=True)
    PermissionForSandMiningFromRiverbedDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    PermissionForGroundWaterWithdrawal = models.BooleanField(default=False)
    RulesForGroundWaterWithdrawal = models.CharField(
        max_length=255, default='Environment (Protection) Act')
    ResponsibilityForGroundWaterWithdrawal = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusOfGroundWaterWithdrawal = models.CharField(
        max_length=255, blank=True, null=True)
    PermissionForGroundWaterWithdrawalDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    AuthorizationForCollectionDisposalManagement = models.BooleanField(
        default=False)
    RulesForCollectionDisposalManagement = models.CharField(
        max_length=255, default='Hazardous waste (Management andHandling) Rules')
    ResponsibilityForCollectionDisposalManagement = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusOfCollectionDisposalManagement = models.CharField(
        max_length=255, blank=True, null=True)
    AuthorizationForCollectionDisposalManagementDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    AuthorizationForSolidWaste = models.BooleanField(default=False)
    RulesForSolidWaste = models.CharField(
        max_length=255, default='Municipal Solid waste Rules')
    ResponsibilityOfSolidWaste = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusOfSolidWaste = models.CharField(
        max_length=255, blank=True, null=True)
    AuthorizationForSolidWasteDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    DisposalOfBituminousAndOtherWaste = models.BooleanField(default=False)
    RulesForDisposalOfBituminousAndOtherWaste = models.CharField(
        max_length=255, default='Hazardous waste (Management andHandling) Rules')
    ResponsibilityOfDisposalOfBituminousAndOtherWaste = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusOfDisposalOfBituminousAndOtherWaste = models.CharField(
        max_length=255, blank=True, null=True)
    DisposalOfBituminousAndOtherWasteDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    ConsentToDisposalOfsewagefromLabourCamps = models.BooleanField(
        default=False)
    RulesForDisposalOfsewagefromLabourCamps = models.CharField(
        max_length=255, default='Water (Prevention and Control of Pollution) Act')
    ResponsibilityOfDisposalOfsewagefromLabourCamps = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusOfDisposalOfsewagefromLabourCamps = models.CharField(
        max_length=255, blank=True, null=True)
    ConsentToDisposalOfsewagefromLabourCampsDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)

    PollutionUnderControlCertificate = models.BooleanField(default=False)
    RulesForPollutionUnderControl = models.CharField(
        max_length=255, default='Central Motor and Vehicles Act')
    ResponsibilityOfPollutionUnderControl = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusPollutionUnderControl = models.CharField(
        max_length=255, blank=True, null=True)
    PollutionUnderControlCertificateDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)


    RoofTopRainWaterHarvesting = models.BooleanField(default=False)
    RulesForRoofTopRainWaterHarvesting = models.CharField(
        max_length=255, default='Central Ground Water Authority (CGWA),Guidelines')
    ResponsibilityOfRoofTopRainWaterHarvesting = models.CharField(
        max_length=255, blank=True, null=True)
    CurrentStatusRoofTopRainWaterHarvesting = models.CharField(
        max_length=255, blank=True, null=True)
    RoofTopRainWaterHarvestingDocuments = ArrayField(models.CharField(max_length=255, blank=True, null=True), blank=True, null=True)