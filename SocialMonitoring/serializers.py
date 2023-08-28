from rest_framework import serializers
from .models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.fields import CurrentUserDefault
from django.core.validators import MinLengthValidator, MaxLengthValidator



def validate_coordinate(value):
    if '.' in value:
        integer_part, decimal_part = value.split('.')
        if len(decimal_part) > 6:
            raise serializers.ValidationError("Coordinate must have at most 6 digits after the decimal point.")



#---------------Labour camp Serializer for GEO jason Format--------------------------------

class labourCampDetailSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=10, required=False )
    latitude = serializers.CharField(max_length=8, required=False )
    class Meta:
        model = labourcampDetails
        fields = ('LabourCampName' , 'LabourCampId' , 'longitude' , 'latitude')

    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data
    
    def create(self, data):
        data.pop('longitude')
        data.pop('latitude')
        return labourcampDetails.objects.create(**data) 

class labourCampDetailviewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = labourcampDetails
        fields = '__all__'
        geo_field = 'location'

class labourCampDetailGetviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = labourcampDetails
        fields = '__all__'





# --------------- PAP Serializer --------------------------------

class PapSerailzer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude = serializers.CharField(max_length=50, required=True)
    latitude = serializers.CharField(max_length=50, required=True)
    legalDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    presentPhotograph = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)

    class Meta:
        model = PAP
        fields = ('quarter', 'packages', 'longitude', 'latitude','dateOfMonitoring', 'user','dateOfIdentification','PAPID','nameOfPAP', 
                  'addressLine1','streetName','pincode','eligibility', 'categoryOfPap', 
                    'areaOfAsset','typeOfStructure','legalStatus','legalDocuments',
                   'actionTaken', 'notAgreedReason','presentPhotograph','remarks' )

    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

    def create(self, data):
        data.pop('longitude')
        data.pop('latitude')
        return PAP.objects.create(**data)
    
   

class PapUpdateSerialzier(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=10, required=False)
    latitude = serializers.CharField(max_length=10, required=False)
    class Meta:
        model = PAP
        fields = ('quarter', 'packages', 'longitude', 'latitude', 'dateOfIdentification',
                  'addressLine1','streetName','pincode','eligibility', 'categoryOfPap',
                  'areaOfAsset','typeOfStructure','legalStatus','legalDocuments',
                   'actionTaken', 'notAgreedReason','presentPhotograph','remarks')
    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

class papviewserialzer(GeoFeatureModelSerializer):
    class Meta:
        model = PAP
        fields = '__all__'
        geo_field = 'location'






# ------------------------ Rehabiliation Serializer ----------------------------------------
class RehabilitationSerializer(serializers.ModelSerializer):

    longitude = serializers.CharField(max_length=50, required=True  )
    latitude = serializers.CharField(max_length=50, required=True)

    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    livelihoodSupportPhotograph = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    trainingPhotograph = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    tenamentsPhotograph =serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    photographs =serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    class Meta:
        model = Rehabilitation
        fields = ('quarter','longitude', 'latitude','ID','dateOfRehabilitation' ,'PAPID', 'PAPName' ,'categoryOfPap','cashCompensation', 'compensationStatus',
                   'typeOfCompensation', 'otherCompensationType' ,'addressLine1','streetName','pincode',
                   'isShiftingAllowance','shiftingAllowanceAmount','isLivelihoodSupport', 'livelihoodSupportAmount','livelihoodSupportCondition',
                   'livelihoodSupportPhotograph','livelihoodSupportRemarks','isTraining','trainingCondition',
                   'trainingPhotograph' ,'trainingRemarks' , 'typeOfStructure'  ,'areaOfTenament' , 'tenamentsPhotograph',
                    'isRelocationAllowance' ,'RelocationAllowanceAmount' ,'isfinancialSupport',
                   'financialSupportAmount','isCommunityEngagement','isEngagementType', 'photographs' , 'documents','remarks')

    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

    def create(self, data):
        data.pop('longitude')
        data.pop('latitude')
        Rehabilitation_data = Rehabilitation.objects.create(**data)
  
        return Rehabilitation_data


class RehabilitationViewSerializer(GeoFeatureModelSerializer):
    class Meta:
            model = Rehabilitation
            fields = '__all__'
            geo_field = 'location'


class RehabilatedPAPIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAP
        fields = ('id', 'PAPID' , 'nameOfPAP' , 'categoryOfPap'  , "actionTaken")

# -------------------------------- Labour camp details Serialzier --------------------------------      
class LabourCampDetailSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    dateOfMonitoring = serializers.DateField(required=True)
    packages = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    longitude = serializers.CharField(max_length=50, required=True)
    latitude = serializers.CharField(max_length=50, required=True)
    labourCampName = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    labourCampId = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    
    photographs= serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True)
    documents  = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True)
    class Meta:
        model = LabourCamp
        fields = ('quarter', 'packages','dateOfMonitoring','longitude', 'latitude', 'labourCampName', 'labourCampId',
                  'isToilet', 'toiletCondition','toiletPhotograph','toiletRemarks',
                  'isDrinkingWater','drinkingWaterCondition' ,'drinkingWaterPhotographs','drinkingWaterRemarks',
                    'isDemarkationOfPathways','demarkationOfPathwaysCondition','demarkationOfPathwaysPhotographs','demarkationOfPathwaysRemark' ,
                    'isSignagesLabeling','signagesLabelingCondition' ,'signagesLabelingPhotographs','signagesLabelingRemarks',
                    'isKitchenArea','kitchenAreaCondition','kitchenAreaPhotographs','kitchenAreaRemarks',
                    'isFireExtinguish','fireExtinguishCondition','fireExtinguishPhotographs','fireExtinguishRemarks',
                     'isRoomsOrDoms' ,'roomsOrDomsCondition','roomsOrDomsPhotographs' ,'roomsOrDomsRemarks',
                     'isSegregationOfWaste','segregationOfWasteCondition','segregationOfWastePhotographs','segregationOfWasteRemarks',
                    'isRegularHealthCheckup','regularHealthCheckupCondition','regularHealthCheckupPhotographs','regularHealthCheckupRemarks',
                     'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition','availabilityOfDoctorPhotographs','availabilityOfDoctorRemarks',
                      'isFirstAidKit','firstAidKitCondition' ,'firstAidKitPhotographs','firstAidKitRemarks',
                    'transportationFacility' ,'transportationFacilityCondition', 'modeOfTransportation','distanceFromSite',
                    'photographs' ,'documents','remarks')


    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        

        return data
    
    def create(self,data):
        data.pop('longitude')
        data.pop('latitude')
        return LabourCamp.objects.create(**data)

        

class LabourCampUpdateSerialzier(serializers.ModelSerializer):
    class Meta:
        model = LabourCamp
        fields = ('labourCampId' , 'labourCampName','isToilet','toiletCondition','toiletPhotograph','toiletRemarks',
                 'isDrinkingWater','drinkingWaterCondition' , 'drinkingWaterPhotographs', 'drinkingWaterRemarks',
                 'isDemarkationOfPathways','demarkationOfPathwaysCondition','demarkationOfPathwaysPhotographs' ,'demarkationOfPathwaysRemark',
                 'isSignagesLabeling','signagesLabelingPhotographs' ,'signagesLabelingRemarks' ,
                 'isKitchenArea','kitchenAreaCondition','kitchenAreaPhotographs','kitchenAreaRemarks',
                'isFireExtinguish','fireExtinguishCondition','fireExtinguishPhotographs','fireExtinguishRemarks',
                     'isRoomsOrDoms' ,'roomsOrDomsCondition','roomsOrDomsPhotographs' ,'roomsOrDomsRemarks',
                     'isSegregationOfWaste','segregationOfWasteCondition','segregationOfWastePhotographs','segregationOfWasteRemarks',
                    'isRegularHealthCheckup','regularHealthCheckupCondition','regularHealthCheckupPhotographs','regularHealthCheckupRemarks',
                     'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition','availabilityOfDoctorPhotographs','availabilityOfDoctorRemarks',
                      'isFirstAidKit','firstAidKitCondition' ,'firstAidKitPhotographs','firstAidKitRemarks',
                    'transportationFacility' ,'transportationFacilityCondition', 'modeOfTransportation','distanceFromSite',
                    'photographs' ,'documents','remarks')


    


# ----------------------------- Construction site serializer -----------------------------------
class constructionSiteSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quarter = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    dateOfMonitoring = serializers.DateField(required=True)
    packages = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    longitude = serializers.CharField(max_length=10, required=True)
    latitude = serializers.CharField(max_length=10, required=True)
    constructionSiteId = serializers.CharField(max_length = 255 , required = True)
    constructionSiteName = serializers.CharField(max_length = 255 , required = True)
    genralphotographs= serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True)
    documents  = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True)
    class Meta:
        model = ConstructionSiteDetails
        fields = ('quarter', 'packages','dateOfMonitoring' ,'longitude', 'latitude', 'constructionSiteName' , 'constructionSiteId',
                 'isDemarkationOfPathways','demarkationOfPathwaysCondition','demarkationOfPathwaysPhotographs','demarkationOfPathwaysRemark' ,
                'isSignagesLabelingCheck','signagesLabelingCondition' ,'signagesLabelingPhotographs','signagesLabelingRemarks',
                'isRegularHealthCheckup','regularHealthCheckupCondition','regularHealthCheckupPhotographs','regularHealthCheckupRemarks',
                  'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition','availabilityOfDoctorPhotographs','availabilityOfDoctorRemarks',
                      'isFirstAidKit','firstAidKitCondition' ,'firstAidKitPhotographs','firstAidKitRemarks',
                   'isDrinkingWaterCheck','drinkingWaterCondition' ,'drinkingWaterPhotographs','drinkingWaterRemarks',
                    'isToilet', 'toiletCondition','toiletPhotograph','toiletRemarks',
                    'genralphotographs','documents','remarks')
    
    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

    def create(self,data):
        data.pop('longitude', None)
        data.pop('latitude', None)
        return ConstructionSiteDetails.objects.create(**data)
    



''' This serializer for view the data - Amol Bhore'''

class ConstructionSiteDetailsViewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ConstructionSiteDetails
        fields = '__all__'
        geo_field = 'location'
class LabourCampDetailViewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = LabourCamp
        fields = '__all__'
        geo_field = 'location'

# class testserialzier(serializers.ModelSerializer):
#     class Meta:
#         model = Test
#         fields = '__all__'

class PAPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAP
        fields = '__all__'



class ConstructionSiteDetailsserializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionSiteDetails
        fields = '__all__'



class LabourCampserializer(serializers.ModelSerializer):
    class Meta:
        model = LabourCamp
        fields = '__all__' 