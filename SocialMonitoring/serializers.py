from rest_framework import serializers
from .models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.fields import CurrentUserDefault
from django.core.validators import MinLengthValidator, MaxLengthValidator



def validate_coordinate(value):
    """
    The function `validate_coordinate` checks if a coordinate value has at most 6 digits after the
    decimal point.
    
    :param value: The `value` parameter is a string representing a coordinate value
    """
    if '.' in value:
        integer_part, decimal_part = value.split('.')
        if len(decimal_part) > 6:
            raise serializers.ValidationError("Coordinate must have at most 6 digits after the decimal point.")



#---------------Labour camp Serializer for GEO jason Format--------------------------------

# The `labourCampDetailSerializer` class is a serializer for the `labourcampDetails` model in Python,
# which includes validation for longitude and latitude fields and a create method that excludes those
# fields.
class labourCampDetailSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=10, required=False )
    latitude = serializers.CharField(max_length=10, required=False )
    image = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)
    class Meta:
        model = labourcampDetails
        fields = ('LabourCampName' , 'LabourCampId' , 'longitude' , 'latitude' ,'capacity' , 'image')

    def validate(self,data):
        """
        The function validates the longitude and latitude values in a given data dictionary, ensuring
        that they have at most 6 digits after the decimal point.
        """
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data
    
    def create(self, data):
        """
        The function creates a new instance of the labourcampDetails model by removing the 'longitude'
        and 'latitude' keys from the data dictionary and passing the remaining data as keyword
        arguments.
        
        """
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
    cadastralMapDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    legalDocuments = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    presentPhotograph = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)

    class Meta:
        model = PAP
        fields = ('quarter', 'packages', 'longitude', 'latitude','dateOfMonitoring', 'user','dateOfIdentification','PAPID', 'cadastralMapID', 'cadastralMapDocuments', 'nameOfPAP','firstName', 'middleName', 'lastName',  
                  'addressLine1','streetName','pincode','eligibility', 'categoryOfPap', 
                    'areaOfAsset','typeOfStructure','legalStatus','legalDocuments',
                   'actionTaken', 'notAgreedReason','presentPhotograph','remarks' )

    def validate(self,data):

        """
        The function validates the longitude and latitude values in a given data dictionary, ensuring
        that they have at most 6 digits after the decimal point.
        """
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

    def create(self, data):
        """
        The function creates a new instance of the labourcampDetails model by removing the 'longitude'
        and 'latitude' keys from the data dictionary and passing the remaining data as keyword
        arguments.
        
        """
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
        """
        The function validates the longitude and latitude values in a given data dictionary, ensuring
        that they have at most 6 digits after the decimal point.
        """
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
# The RehabilitationSerializer class is a serializer for the Rehabilitation model in a Python Django
# application, with various fields for data serialization and file uploads.
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
        fields = ('quarter','longitude', 'latitude','ID','packages','dateOfRehabilitation' ,'PAPID', 'PAPName' ,'categoryOfPap','cashCompensation', 'compensationStatus',
                   'typeOfCompensation', 'otherCompensationType' ,'addressLine1','streetName','pincode',
                   'isShiftingAllowance','shiftingAllowanceAmount','isLivelihoodSupport', 'livelihoodSupportAmount','livelihoodSupportCondition',
                   'livelihoodSupportPhotograph','livelihoodSupportRemarks','isTraining','trainingCondition',
                   'trainingPhotograph' ,'trainingRemarks' , 'typeOfStructure'  ,'areaOfTenament' , 'tenamentsPhotograph',
                    'isRelocationAllowance' ,'RelocationAllowanceAmount' ,'isfinancialSupport',
                   'financialSupportAmount','isCommunityEngagement','isEngagementType', 'photographs' , 'documents','remarks')

    def validate(self,data):
        """
        The function validates the longitude and latitude values in a given data dictionary, ensuring
        that they have at most 6 digits after the decimal point.
        
        """
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

    def create(self, data):
        """
        The function creates a new instance of the Rehabilitation model using the provided data,
        excluding the 'longitude' and 'latitude' fields.
        
        """
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
        fields = ('id', 'PAPID' , 'nameOfPAP' , 'categoryOfPap'  , 'actionTaken', 'firstName', 'middleName', 'lastName', 'addressLine1', 'streetName', 'pincode', 'location')

# -------------------------------- Labour camp details Serialzier --------------------------------      
# The `LabourCampDetailSerializer` class is a serializer for the `LabourCamp` model in Python, which
# includes various fields and nested fields for serialization and deserialization.
class LabourCampDetailSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    dateOfMonitoring = serializers.DateField(required=True)
    packages = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    longitude = serializers.CharField(max_length=50, required=True)
    latitude = serializers.CharField(max_length=50, required=True)
    labourCampName = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    labourCampId = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    
    toiletPhotograph = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    drinkingWaterPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    demarkationOfPathwaysPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    signagesLabelingPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    kitchenAreaPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    fireExtinguishPhotographs=serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    roomsOrDomsPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    segregationOfWastePhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    regularHealthCheckupPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    availabilityOfDoctorPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    firstAidKitPhotographs=serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    photographs =serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)
    documents  = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True , required=False)

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
        """
        The function validates the longitude and latitude values in a given data dictionary, ensuring
        that they have at most 6 digits after the decimal point.

        """
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data
    
    def create(self,data):
        """
        The function creates a new instance of the LabourCamp model using the provided data, excluding
        the 'longitude' and 'latitude' fields.
        
        """
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
# The `constructionSiteSerializer` class is a serializer for the `ConstructionSiteDetails` model in
# Python, which includes various fields and validations for construction site data.
class constructionSiteSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quarter = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    dateOfMonitoring = serializers.DateField(required=True)
    packages = serializers.CharField(validators=[MinLengthValidator(3)] , required=True)
    longitude = serializers.CharField(max_length=10, required=True)
    latitude = serializers.CharField(max_length=10, required=True)
    constructionSiteId = serializers.CharField(max_length = 255 , required = True)
    constructionSiteName = serializers.CharField(max_length = 255 , required = True)

    demarkationOfPathwaysPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    signagesLabelingPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    regularHealthCheckupPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    availabilityOfDoctorPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    firstAidKitPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    drinkingWaterPhotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    toiletPhotograph = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    genralphotographs= serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True , required=False)
    documents  = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True , required=False)
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
        """
        The function validates the longitude and latitude values in a given data dictionary, ensuring
        that they have at most 6 digits after the decimal point.
        
        """
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

    def create(self,data):
        """
        The create function removes the 'longitude' and 'latitude' keys from the data dictionary and
        creates a new ConstructionSiteDetails object with the remaining data.
        
        """
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