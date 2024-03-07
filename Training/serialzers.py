
from rest_framework import serializers
from .models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from itertools import zip_longest


# The below class is a serializer in Python that is used to serialize and deserialize data for the
# 'traning' model, including handling file fields for documents and photographs.
class TraningSerializer(serializers.ModelSerializer):
    longitude=serializers.CharField(max_length=10,required=True)
    latitude=serializers.CharField(max_length=10,required=True)

    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    photographs = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    
    class Meta:
        model = traning
        fields =( 'quarter' , 'packages' , 'dateOfMonitoring' ,'category' , 'traningTitle' , 'noOfAttends' ,'noOfTimesTrainingConducted' ,  'male' , 'female' ,
                 'longitude' , 'latitude' ,'inchargePerson' , 'traninigInitiatedBy' , 
                 'conductDate' , 'traningDate' ,  'photographs' , 'documents')

    def create(self,data):  
        data.pop('longitude')
        data.pop('latitude')
        return traning.objects.create(**data)


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
class occupationalHealthSafetySerialziers(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length= 255 , required = False) # longitude
    incidentlongitude = serializers.CharField(max_length= 255 , required = False) # longitude
    latitude = serializers.CharField(max_length= 255, required = False) # latitude
    incidentlatitude = serializers.CharField(max_length= 255, required = False) # latitude
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    photographs = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)

    class Meta:
        model = occupationalHealthSafety
        fields = ['dateOfMonitoring' ,'packages', 'quarter','longitude', 'latitude' ,
        'joiningMedicalCheckup' , 'ppeKit' ,'trainingToWorkers','houseKeeping' ,
        'powerSupplySystem' ,'assemblyArea' ,'ambulanceArrangement' ,'toiletFacility',
        'safeMomentPassage' ,'materialKeepingPractice','accidentalCheck','safetyGearStatus',
        'barricading','natureOfAccident' ,'typeOfIncident' , 'incidentReportingStatus', 'incidentlatitude','incidentlongitude','incidentDetails' ,
        'identifiedCauseOfIncident' ,'outcome' ,'compensationPaid' ,'photographs' , 'documents' , 'remarks']

    
    def create(self,data):
        data.pop('longitude')
        data.pop('latitude')
        data.pop('incidentlongitude')
        data.pop('incidentlatitude')
        return occupationalHealthSafety.objects.create(**data)
    

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
class PreConstructionStageComplianceSerialzier(serializers.ModelSerializer):
    class Meta:
        model =  PreConstructionStage
        fields = ('ShiftingofUtilities' , 'ResponsibilityOfShiftingofUtilities','CurrentStatusOfShiftingofUtilities', 'ShiftingofUtilitiesDocuments',
                    'PermissionForFellingOfTrees', 'ResponsibilityOfPermissionForFellingOfTrees','CurrentStatusPermissionForFellingOfTrees', 'PermissionForFellingOfTreesDocuments',
                   'CRZClearance','ResponsibilityOfCRZClearance' ,  'CurrentStatusCRZClearance' , 'CRZClearanceDocuments',
                   'ForestClearance' , 'ResponsibilityOfForestClearance', 'CurrentStatusOfForestClearance', 'ForestClearanceDocuments')


# The class ConstructionStageComplainceSerializer is a serializer for the ConstructionStage model,
# excluding certain fields.
class ConstructionStageComplainceSerializer(serializers.ModelSerializer):
    ConsenttToEstablishOoperateDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    PermissionForSandMiningFromRiverbedDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    PermissionForGroundWaterWithdrawalDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    AuthorizationForCollectionDisposalManagementDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    AuthorizationForSolidWasteDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    DisposalOfBituminousAndOtherWasteDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    ConsentToDisposalOfsewagefromLabourCampsDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    PollutionUnderControlCertificateDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    RoofTopRainWaterHarvestingDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)

    class Meta:
        model = ConstructionStage 
        # fields = '__all__'
        exclude = ('RulesOfConsenttToEstablishOoperate', 'RulesOfSandMiningFromRiverbed',
        'RulesForGroundWaterWithdrawal' , 'RulesForCollectionDisposalManagement', 'RulesForSolidWaste',
       'RulesForDisposalOfBituminousAndOtherWaste', 'RulesForDisposalOfsewagefromLabourCamps' , 'RulesForPollutionUnderControl',
       'RulesForRoofTopRainWaterHarvesting','user')



class ContactusImagesSeilizer(serializers.ModelSerializer):
    class Meta:
        model = ContactusImage
        fields = '__all__'