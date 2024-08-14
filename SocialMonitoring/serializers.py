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
    legalDocuments = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    presentPhotograph = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    cadastralMapDocuments = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True,  required=False)
    cadastralMapID = serializers.CharField(required=True)  # Ensure it's required

    class Meta:
        model = PAP
        fields = ('quarter', 'packages', 'longitude', 'latitude','dateOfMonitoring', 'user','dateOfIdentification','PAPID', 'cadastralMapID', 'cadastralMapDocuments', 'firstName', 'middleName', 'lastName',  
                  'addressLine1','streetName','pincode','eligibility', 'categoryOfPap', 
                    'areaOfAsset','typeOfStructure','legalStatus', 'legalDocuments', 'presentPhotograph',
                   'actionTaken', 'notAgreedReason','documents','remarks' )

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
    
    def validate_cadastralMapID(self, value):
        if not value:
            raise serializers.ValidationError("Cadastral Map ID is required.")
        if PAP.objects.filter(cadastralMapID=value).exists():
            raise serializers.ValidationError("This Cadastral Map ID already exists.")
        return value

    def create(self, data):
        """
        The function creates a new instance of the labourcampDetails model by removing the 'longitude'
        and 'latitude' keys from the data dictionary and passing the remaining data as keyword
        arguments.
        
        """
        data.pop('longitude')
        data.pop('latitude')
        return PAP.objects.create(**data)
    
   
class PapUpdateSerailzer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    legalDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    presentPhotograph = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    cadastralMapDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    cadastralMapID = serializers.CharField(required=False)  # Optional in PATCH

    class Meta:
        model = PAP
        fields = ('quarter', 'packages', 'longitude', 'latitude', 'dateOfMonitoring', 'user', 'dateOfIdentification', 'PAPID', 'cadastralMapID', 'cadastralMapDocuments', 'firstName', 'middleName', 'lastName',
                  'addressLine1', 'streetName', 'pincode', 'eligibility', 'categoryOfPap',
                  'areaOfAsset', 'typeOfStructure', 'legalStatus', 'legalDocuments', 'presentPhotograph',
                  'actionTaken', 'notAgreedReason', 'documents', 'remarks')

    def validate(self, data):
        """
        Validates the longitude and latitude values, ensuring
        that they have at most 6 digits after the decimal point.
        """
        longitude = data.get('longitude', '')
        latitude = data.get('latitude', '')
        
        if longitude and not self._is_valid_decimal(longitude):
            raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        if latitude and not self._is_valid_decimal(latitude):
            raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        
        return data

    def _is_valid_decimal(self, value):
        """
        Helper method to check if a value has at most 6 digits after the decimal point.
        """
        if '.' in value:
            return len(value.split('.')[-1]) <= 6
        return True



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

    documents  = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True , required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)
    class Meta:
        model = Rehabilitation
        fields = ('quarter','longitude', 'latitude','packages','dateOfRehabilitation' ,'PAPID',
                   'firstName', 'middleName', 'lastName', 'compensationStatus', 'agreedUpon', 'processStatus',
                   'cashCompensationAmount',
                   'typeOfCompensation', 'otherCompensationType' ,
                   'addressLine1','streetName','pincode',
                   'rehabLocation', 'allowance', 'area',
                   'isShiftingAllowance','shiftingAllowanceAmount',
                   'isLivelihoodSupport', 'livelihoodSupportAmount',
                   'isTraining','trainingRemarks', 'typeOfStructure',
                   'isRelocationAllowance' ,'RelocationAllowanceAmount' ,'isfinancialSupport',
                   'financialSupportAmount','isCommunityEngagement','isEngagementType',
                   'photographs' , 'documents','remarks')

    def validate(self, data):
        """
        The function validates the longitude and latitude values in a given data dictionary, ensuring
        that they have at most 6 digits after the decimal point.
        """
        long = data.get('longitude', '').split('.')[-1]
        if long and len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat = data.get('latitude', '').split('.')[-1]
        if lat and len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
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


# Rehab update (PATCH) check for PUT
class RehabilitationGetUpdateDeleteSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = Rehabilitation
        fields = ('id', 'quarter', 'longitude', 'latitude', 'packages', 'dateOfRehabilitation', 'PAPID',
                  'firstName', 'middleName', 'lastName', 'compensationStatus', 'agreedUpon', 'processStatus',
                  'cashCompensationAmount', 'typeOfCompensation', 'otherCompensationType',
                  'addressLine1', 'streetName', 'pincode', 'rehabLocation', 'allowance', 'area',
                  'isShiftingAllowance', 'shiftingAllowanceAmount', 'isLivelihoodSupport', 'livelihoodSupportAmount',
                  'isTraining', 'trainingRemarks', 'typeOfStructure', 'isRelocationAllowance', 'RelocationAllowanceAmount',
                  'isfinancialSupport', 'financialSupportAmount', 'isCommunityEngagement', 'isEngagementType',
                  'photographs', 'documents', 'remarks')

    def validate(self, data):
        """
        The function validates the longitude and latitude values in a given data dictionary, ensuring
        that they have at most 6 digits after the decimal point.
        """
        long = data.get('longitude', '').split('.')[-1]
        if long and len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat = data.get('latitude', '').split('.')[-1]
        if lat and len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data



class RehabilitationViewSerializer(GeoFeatureModelSerializer):
    class Meta:
            model = Rehabilitation
            fields = '__all__'
            geo_field = 'location'


class RehabilatedPAPIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAP
        fields = ('id', 'PAPID', 'categoryOfPap'  , 'actionTaken', 'firstName', 'middleName', 'lastName', 'addressLine1', 'streetName', 'pincode', 'location')

# -------------------------------- Labour camp Serialzier --------------------------------      
# The `LabourCampDetailSerializer` class is a serializer for the `LabourCamp` model in Python, which
# includes various fields and nested fields for serialization and deserialization.
class LabourCampSerializer(serializers.ModelSerializer):
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

        
# Labour Camp Update
class LabourCampUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    toiletPhotograph = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    drinkingWaterPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    demarkationOfPathwaysPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    signagesLabelingPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    kitchenAreaPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    fireExtinguishPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    roomsOrDomsPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    segregationOfWastePhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    regularHealthCheckupPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    availabilityOfDoctorPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    firstAidKitPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = LabourCamp
        fields = (
            'quarter', 'packages', 'dateOfMonitoring', 'longitude', 'latitude', 'labourCampName', 'labourCampId',
            'isToilet', 'toiletCondition', 'toiletPhotograph', 'toiletRemarks',
            'isDrinkingWater', 'drinkingWaterCondition', 'drinkingWaterPhotographs', 'drinkingWaterRemarks',
            'isDemarkationOfPathways', 'demarkationOfPathwaysCondition', 'demarkationOfPathwaysPhotographs', 'demarkationOfPathwaysRemark',
            'isSignagesLabeling', 'signagesLabelingCondition', 'signagesLabelingPhotographs', 'signagesLabelingRemarks',
            'isKitchenArea', 'kitchenAreaCondition', 'kitchenAreaPhotographs', 'kitchenAreaRemarks',
            'isFireExtinguish', 'fireExtinguishCondition', 'fireExtinguishPhotographs', 'fireExtinguishRemarks',
            'isRoomsOrDoms', 'roomsOrDomsCondition', 'roomsOrDomsPhotographs', 'roomsOrDomsRemarks',
            'isSegregationOfWaste', 'segregationOfWasteCondition', 'segregationOfWastePhotographs', 'segregationOfWasteRemarks',
            'isRegularHealthCheckup', 'regularHealthCheckupCondition', 'regularHealthCheckupPhotographs', 'regularHealthCheckupRemarks',
            'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition', 'availabilityOfDoctorPhotographs', 'availabilityOfDoctorRemarks',
            'isFirstAidKit', 'firstAidKitCondition', 'firstAidKitPhotographs', 'firstAidKitRemarks',
            'transportationFacility', 'transportationFacilityCondition', 'modeOfTransportation', 'distanceFromSite',
            'photographs', 'documents', 'remarks'
        )

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
    

# Update Construction Site (PATCH)
class ConstructionSiteUpdateSerializer(serializers.ModelSerializer):
    quarter = serializers.CharField(validators=[MinLengthValidator(3)], required=False)
    dateOfMonitoring = serializers.DateField(required=False)
    packages = serializers.CharField(validators=[MinLengthValidator(3)], required=False)
    longitude = serializers.CharField(max_length=10, required=False)
    latitude = serializers.CharField(max_length=10, required=False)
    constructionSiteId = serializers.CharField(max_length=255, required=False)
    constructionSiteName = serializers.CharField(max_length=255, required=False)

    demarkationOfPathwaysPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    signagesLabelingPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    regularHealthCheckupPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    availabilityOfDoctorPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    firstAidKitPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    drinkingWaterPhotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    toiletPhotograph = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    genralphotographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = ConstructionSiteDetails
        fields = ('quarter', 'packages', 'dateOfMonitoring', 'longitude', 'latitude', 'constructionSiteName', 'constructionSiteId',
                  'isDemarkationOfPathways', 'demarkationOfPathwaysCondition', 'demarkationOfPathwaysPhotographs', 'demarkationOfPathwaysRemark',
                  'isSignagesLabelingCheck', 'signagesLabelingCondition', 'signagesLabelingPhotographs', 'signagesLabelingRemarks',
                  'isRegularHealthCheckup', 'regularHealthCheckupCondition', 'regularHealthCheckupPhotographs', 'regularHealthCheckupRemarks',
                  'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition', 'availabilityOfDoctorPhotographs', 'availabilityOfDoctorRemarks',
                  'isFirstAidKit', 'firstAidKitCondition', 'firstAidKitPhotographs', 'firstAidKitRemarks',
                  'isDrinkingWaterCheck', 'drinkingWaterCondition', 'drinkingWaterPhotographs', 'drinkingWaterRemarks',
                  'isToilet', 'toiletCondition', 'toiletPhotograph', 'toiletRemarks',
                  'genralphotographs', 'documents', 'remarks')

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