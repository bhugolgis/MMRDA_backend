
from rest_framework import serializers
from .models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from itertools import zip_longest


# The below class is a serializer in Python that is used to serialize and deserialize data for the
# 'traning' model, including handling file fields for documents and photographs.
class TraningSerializer(serializers.ModelSerializer):
    longitude=serializers.CharField(max_length=10,required=True)
    latitude=serializers.CharField(max_length=10,required=True)

    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    
    class Meta:
        model = traning
        fields =( 'quarter' , 'packages' , 'dateOfMonitoring' ,'category' , 'traningTitle' , 'noOfAttends' ,'noOfTimesTrainingConducted' ,  'male' , 'female' ,
                 'longitude' , 'latitude' ,'inchargePerson' , 'traninigInitiatedBy' , 
                 'conductDate' , 'traningDate' ,  'photographs' , 'documents')

    def create(self,data):
        data.pop('longitude')
        data.pop('latitude')
        return traning.objects.create(**data)


# GET
class TrainingViewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = traning
        fields = '__all__'
        geo_field= 'location'

# Update (PATCH)
class TrainingUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=10, required=False)
    latitude = serializers.CharField(max_length=10, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = traning
        fields = ('quarter', 'packages', 'dateOfMonitoring', 'category', 'traningTitle', 'noOfAttends', 'noOfTimesTrainingConducted',
                  'male', 'female', 'longitude', 'latitude', 'inchargePerson', 'traninigInitiatedBy', 'conductDate',
                  'traningDate', 'photographs', 'documents')

    def validate(self, data):
        if 'longitude' in data:
            long = data['longitude'].split('.')[-1]
            if len(long) > 6:
                raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        if 'latitude' in data:
            lat = data['latitude'].split('.')[-1]
            if len(lat) > 6:
                raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        return data

# The `photographsSerializer` class is a serializer for the `photographs` model in Python, which
# includes fields for longitude and latitude and a create method that removes latitude and longitude
# from the data before creating a new `photographs` object.
class photographsSerializer(serializers.ModelSerializer):
    longitude=serializers.CharField(max_length=10,required=False)
    latitude=serializers.CharField(max_length=10,required=False)
    class Meta:
        model = photographs
        fields = ['photograph_title', 'photographs_uploaded_by' , 'longitude' , 'latitude',
                   'date' , 'site_photographs'  ]

    def create(self,data):
        data.pop('latitude')
        data.pop('longitude')
        return photographs.objects.create(**data)

class photographsViewSerializer(serializers.ModelSerializer):
    longitude=serializers.CharField(max_length=10,required=False)
    latitude=serializers.CharField(max_length=10,required=False)
    class Meta:
        model = photographs
        fields =['id','photograph_title', 'photographs_uploaded_by' , 'longitude' , 'latitude',
                   'date' , 'site_photographs'  ]


# The `occupationalHealthSafetySerialziers` class is a serializer class in Python that defines the
# fields and behavior for serializing and deserializing data related to occupational health and safety
# incidents.

# Find a way to create location data by getting lat long and make it  optional , handel that case, currently this situation is not occured.
class occupationalHealthSafetySerialziers(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length= 255 , required = True) # longitude
    latitude = serializers.CharField(max_length= 255, required = True) # latitude
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    photographs = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)

    class Meta:
        model = occupationalHealthSafety
        fields = ['dateOfMonitoring' ,'packages', 'quarter','longitude', 'latitude' ,
        'joiningMedicalCheckup' , 'ppeKit' ,'trainingToWorkers','houseKeeping' ,
        'powerSupplySystem' ,'assemblyArea' ,'ambulanceArrangement' ,'toiletFacility',
        'safeMomentPassage' ,'materialKeepingPractice','accidentalCheck','safetyGearStatus',
        'barricading','natureOfAccident' ,'typeOfIncident' , 'incidentReportingStatus', 'incidentDetails' ,
        'identifiedCauseOfIncident' ,'outcome' ,'compensationPaid' ,'manDaysLostCount', 'manDaysLostReason', 'photographs' , 'documents' , 'remarks']
    
    def create(self,data):
        data.pop('longitude')
        data.pop('latitude')
        return occupationalHealthSafety.objects.create(**data)
    

# Update (PATCH) Serializer
class OccupationalHealthSafetyUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=255, required=False)
    latitude = serializers.CharField(max_length=255, required=False)
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False), write_only=True, required=False)
    photographs = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False), write_only=True, required=False)

    class Meta:
        model = occupationalHealthSafety
        fields = ['dateOfMonitoring', 'packages', 'quarter', 'longitude', 'latitude',
                  'joiningMedicalCheckup', 'ppeKit', 'trainingToWorkers', 'houseKeeping',
                  'powerSupplySystem', 'assemblyArea', 'ambulanceArrangement', 'toiletFacility',
                  'safeMomentPassage', 'materialKeepingPractice', 'accidentalCheck', 'safetyGearStatus',
                  'barricading', 'natureOfAccident', 'typeOfIncident', 'incidentReportingStatus', 'incidentDetails',
                  'identifiedCauseOfIncident', 'outcome', 'compensationPaid', 'manDaysLostCount', 'manDaysLostReason',
                  'photographs', 'documents', 'remarks']

    def validate(self, data):
        """
        Validate the longitude and latitude values, ensuring they have at most 6 digits after the decimal point.
        """
        longitude = data.get('longitude')
        latitude = data.get('latitude')
        
        if longitude:
            long = longitude.split('.')[-1]
            if len(long) > 6:
                raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        
        if latitude:
            lat = latitude.split('.')[-1]
            if len(lat) > 6:
                raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        
        return data
    

class occupationalHealthSafetyViewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = occupationalHealthSafety
        fields = '__all__'
        geo_field = 'location'
 
class ContactusImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contactus
        fields = "__all__"

# The ContactusSerializezr class is a serializer in Python that is used to serialize and deserialize
# Contactus objects, including fields for longitude, latitude, documents, and images.
class ContactusSerializezr(serializers.ModelSerializer):
    # images =  ContactusImageSerializers(many=True, read_only=True)
    longitude = serializers.CharField(max_length= 255 , required = False) # longitude
    latitude = serializers.CharField(max_length= 255, required = False) # latitude
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    image = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    class Meta:
        model = Contactus
        fields = ('name','email','messsage' , 'longitude' , 'latitude' ,'documents'  , 'image')

    def create(self,data):
        data.pop('longitude')
        data.pop('latitude')

        # uploaded_images1 = data.pop("uploaded_images1")
        # uploaded_images2 = data.pop("uploaded_images2")
        contactus = Contactus.objects.create(**data)
        
        # for image1  , image2 in zip_longest(uploaded_images1 ,uploaded_images2):
        #      images = ContactusImage.objects.create(contactus=contactus, images1=image1 , images2=image2)
                                               
        return contactus
        
class ContactusViewSerialzier(GeoFeatureModelSerializer):
    class Meta:
        model = Contactus
        fields = '__all__'
        geo_field = 'location'

# The class PreConstructionStageComplianceSerialzier is a serializer for the PreConstructionStage
# model with specific fields.
class PreConstructionStageComplianceSerializer(serializers.ModelSerializer):
    ShiftingofUtilitiesDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    PermissionForFellingOfTreesDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    CRZClearanceDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    ForestClearanceDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = PreConstructionStage
        fields = (
            'ShiftingofUtilities', 'ResponsibilityOfShiftingofUtilities', 'CurrentStatusOfShiftingofUtilities', 'ShiftingofUtilitiesDocuments',
            'PermissionForFellingOfTrees', 'ResponsibilityOfPermissionForFellingOfTrees', 'CurrentStatusPermissionForFellingOfTrees', 'PermissionForFellingOfTreesDocuments',
            'CRZClearance', 'ResponsibilityOfCRZClearance', 'CurrentStatusCRZClearance', 'CRZClearanceDocuments',
            'ForestClearance', 'ResponsibilityOfForestClearance', 'CurrentStatusOfForestClearance', 'ForestClearanceDocuments'
        )

# The class ConstructionStageComplainceSerializer is a serializer for the ConstructionStage model,
# excluding certain fields.
class ConstructionStageComplianceSerializer(serializers.ModelSerializer):
    ConsenttToEstablishOoperateDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    PermissionForSandMiningFromRiverbedDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    PermissionForGroundWaterWithdrawalDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    AuthorizationForCollectionDisposalManagementDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    AuthorizationForSolidWasteDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    DisposalOfBituminousAndOtherWasteDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    ConsentToDisposalOfsewagefromLabourCampsDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    PollutionUnderControlCertificateDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    RoofTopRainWaterHarvestingDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = ConstructionStage
        exclude = ('RulesOfConsenttToEstablishOoperate', 'RulesOfSandMiningFromRiverbed',
                   'RulesForGroundWaterWithdrawal', 'RulesForCollectionDisposalManagement', 'RulesForSolidWaste',
                   'RulesForDisposalOfBituminousAndOtherWaste', 'RulesForDisposalOfsewagefromLabourCamps', 'RulesForPollutionUnderControl',
                   'RulesForRoofTopRainWaterHarvesting', 'user')



class ContactusImagesSeilizer(serializers.ModelSerializer):
    class Meta:
        model = ContactusImage
        fields = '__all__'