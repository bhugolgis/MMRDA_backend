from rest_framework import serializers 
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import *



# The class `PostSensorLocationDetailsSerializer` is a serializer in Python that is used to serialize
# and deserialize sensor location details, and it includes a `create` method to create a new sensor
# object.
class PostSensorLocationDetailsSerializer(serializers.ModelSerializer):
    longitude=serializers.CharField(max_length=50,required=True )
    latitude=serializers.CharField(max_length=50,required=True)
    class Meta:
        model = sensors 
        fields = ('Name' , 'ID' , 'longitude' , 'latitude')

    
    def create(self,data):
        data.pop('latitude')
        data.pop('longitude')
        return sensors.objects.create(**data)
    

# The class `PostSensorLocationDetailsViewSerializer` is a serializer for the `sensors` model that
# includes all fields and a geo field for location.
class PostSensorLocationDetailsViewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = sensors
        fields = '__all__'
        geo_field = 'location'


# The `AirSerializer` class is a serializer in Python that is used to serialize and validate data for
# the `Air` model, and it includes custom validation for the `longitude` and `latitude` fields.
class AirSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=True )
    latitude=serializers.CharField(max_length=50,required=True)
    class Meta:
        model = Air
        fields = ('quarter','packages','month','longitude','latitude','dateOfMonitoring','PM10','SO2',
                   'O3','NOx','AQI' , 'Remarks')
        # geo_field='location'
    def validate(self,data):
        if data['quarter']=="" or data['quarter']==None:
            raise serializers.ValidationError("quarter cannot be empty!!")
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data
    
    def create(self,data):
        data.pop('latitude')
        data.pop('longitude')
        return Air.objects.create(**data)

    
        
class AirViewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model=Air
        fields='__all__'
        geo_field='location'



# The WaterSerializer class is a serializer for the Water model, with fields for longitude, latitude,
# and other water-related information.
class WaterSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=True)
    latitude=serializers.CharField(max_length=50,required=True)
    class Meta:
        model = water
        fields = ('quarter','packages','month', 'dateOfMonitoringTwo','longitude','latitude',
                    'qualityOfWater' , 'sourceOfWater' ,'waterDisposal')


    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        
        # if data['quarter']=="" or data['quarter']==None:
        #     raise serializers.ValidationError("quarter cannot be empty!!")
        # if data['packages'] == "" or data['packages'] == None:
        #     raise serializers.ValidationError('package cannot be empty!!')
        # if data['qualityOfWater'] == "" or data['qualityOfWater'] == None:
        #     raise serializers.ValidationError('quality_of_water cannot be empty!!')
        # if data['sourceOfWater'] == "" or data['sourceOfWater'] == None:
        #     raise serializers.ValidationError('source_of_water cannot be empty!!')
        return data
    

    def create(self,data):
        data.pop('latitude')
        data.pop('longitude')
        return water.objects.create(**data)

class waterviewserializer(GeoFeatureModelSerializer):
    class Meta:
        model = water
        fields = '__all__'
        geo_field='location'


# The `NoiseSerializer` class is a serializer for the `Noise` model in Django, which includes
# validation for longitude and latitude fields and a create method that excludes latitude and
# longitude when creating a new instance of the model.
class NoiseSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=False)
    latitude=serializers.CharField(max_length=50,required=False)
    class Meta:
        model = Noise
        fields = ('quarter','month','packages','longitude','latitude' ,'dateOfMonitoringThree','noiseLevel' , 'monitoringPeriod', )

    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

    def create(self,data):
        data.pop('latitude')
        data.pop('longitude')
        return Noise.objects.create(**data)

    

class Noiseviewserializer(GeoFeatureModelSerializer):
    class Meta:
        model = Noise
        fields = '__all__'
        geo_field='location'



# The TreeManagementSerializer class is a serializer for the ExistingTreeManagement model in a Django
# application, which includes fields for longitude, latitude, documents, photographs, and other
# attributes, and also includes validation and creation methods.
class TreeManagementSerailizer(serializers.ModelSerializer):
    longitude=serializers.CharField(max_length=50,required=True)
    latitude=serializers.CharField(max_length=50,required=True)
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    photographs = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)

    class Meta:
        model = ExistingTreeManagment
        fields = ('quarter','month','dateOfMonitoring','packages','longitude','latitude' ,'treeID','commanName' ,'botanicalName',
                    'condition', 'noOfTreeCut','actionTaken', 'photographs', 'documents','remarks',)

    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data


    def create(self,data):
        data.pop('latitude')
        data.pop('longitude')
        return ExistingTreeManagment.objects.create(**data)

class TreeManagmentviewserializer(GeoFeatureModelSerializer):
    class Meta:
        model = ExistingTreeManagment
        fields = '__all__'
        geo_field = 'location'


# The above class is a serializer for the NewTreeManagement model in Python, which includes validation
# for longitude and latitude fields and a create method.
class NewTreeManagmentSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50,required=True)
    latitude = serializers.CharField(max_length=50,required=True)
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    photographs = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)

    class Meta:
        model = NewTreeManagement
        fields = ('tree','quarter','month','dateOfMonitoring','packages','longitude','latitude',
                   'commanName' ,'botanicalName', 'condition', 'photographs', 'documents','remarks' )
        
    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        return data

    def create(self,data):
        data.pop('latitude')
        data.pop('longitude')
        return NewTreeManagement.objects.create(**data)


class NewTreeManagmentviewserializer(GeoFeatureModelSerializer):
    class Meta:
        model = NewTreeManagement
        fields = '__all__'
        geo_field = 'location'




# The WasteTreatmentsSerializer class is a serializer in Python that is used to validate and serialize
# data for waste treatments, including fields for longitude, latitude, waste longitude, waste
# latitude, documents, photographs, and other relevant information.
class WasteTreatmentsSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=True)
    latitude=serializers.CharField(max_length=50,required=True)
    waste_longitude = serializers.CharField(max_length=50,required=True)
    waste_latitude = serializers.CharField(max_length=50,required=True)
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    photographs = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)

    class Meta:
        model  = WasteTreatments
        fields = ('quarter','month','packages','longitude','latitude'  ,'dateOfMonitoring' , 'wastetype' ,'quantity',
         'wastehandling' , 'waste_longitude' ,'waste_latitude', 'photographs' , 'documents','remarks')

    def validate(self,data):
        long = data['longitude'].split('.')[-1]
        if len(long) > 6:
            raise serializers.ValidationError("longitude must have at most 6 digits after the decimal point.")
        lat =  data['latitude'].split('.')[-1]
        if len(lat) > 6:
            raise serializers.ValidationError("latitude must have at most 6 digits after the decimal point.")
        
        waste_longitude = data["waste_longitude"].split('.')[-1]
        if len(waste_longitude) > 6:
            raise serializers.ValidationError("waste_longitude must have at most 6 digits after the decimal point.")
        
        waste_latitude = data["waste_latitude"].split('.')[-1]
        if len(waste_latitude) > 6:
            raise serializers.ValidationError("waste_latitude must have at most 6 digits after the decimal point.")

        return data

    def create(self,data):
        data.pop('longitude')
        data.pop('latitude')
        data.pop('waste_longitude')
        data.pop('waste_latitude')

        return WasteTreatments.objects.create(**data)


class wastetreatmentsViewserializer(GeoFeatureModelSerializer):
    class Meta: 
        model = WasteTreatments
        fields = '__all__'
        geo_field= 'location'


# The MaterialManagmentSerializer class is a serializer for the MaterialManegmanet model in Python,
# which includes various fields for storing and managing materials, such as longitude, latitude,
# documents, photographs, and approvals.
class MaterialManagmentSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=True)
    latitude=serializers.CharField(max_length=50,required=True)
    storageLongitude = serializers.CharField(max_length=50,required=True)
    storageLatitude = serializers.CharField(max_length=50,required=True)
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    photographs = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    approvals = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    materialStoragePhotograph = serializers.ListField(child=serializers.ImageField(allow_empty_file=True, use_url=False),write_only=True , required = False)
    class Meta:
        model = MaterialManegmanet
        fields = ('quarter','month','packages','longitude','dateOfMonitoring','latitude' ,
                'typeOfMaterial','source','sourceOfQuarry','materialStorageType','storageLongitude' ,'storageLatitude',
                'materialStorageCondition','materialStoragePhotograph','approvals' ,'photographs',
                'documents','remarks')



    def create(self,data):
        data.pop('longitude')
        data.pop('latitude')
        data.pop('storageLongitude')
        data.pop('storageLatitude')
        return MaterialManegmanet.objects.create(**data)

    

class MaterialSourcingViewserializer(GeoFeatureModelSerializer):
    class Meta:
        model = MaterialManegmanet
        fields = '__all__'
        geo_field = 'location'


class TreemanagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExistingTreeManagment
        fields = ['quarter','packages','location']

class AirmanagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Air
        fields = ['quarter','packages']


class NoisemanagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noise
        fields = ['noiseLevel','monitoringPeriod','location','packages','quarter']


class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTreatments
        fields = ['wastetype','quantity','wastehandling','location','packages','quarter','photographs','remarks']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialManegmanet
        fields = ['approvals','sourceOfQuarry','typeOfMaterial','location','packages','quarter']

class WatermanamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = water
        fields = ['qualityOfWater','sourceOfWater','location','packages','quarter']