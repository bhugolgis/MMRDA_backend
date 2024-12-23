from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import *



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



class PostSensorLocationDetailsViewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = sensors
        fields = '__all__'
        geo_field = 'location'


class AirSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=True )
    latitude=serializers.CharField(max_length=50,required=True)
    class Meta:
        model = Air
        fields = ('quarter','packages','month','longitude','latitude','place_location', 'dateOfMonitoring','PM10',
                  'PM2_5','SO2','NOx','CO','AQI','Remarks')
        # geo_field='location'
    def validate(self, data):
        quarter = data.get('quarter')
        if not quarter:
            raise serializers.ValidationError("Quarter cannot be empty!!")

        packages = data.get('packages')
        if not quarter:
            raise serializers.ValidationError("Package cannot be empty!!")
        
        longitude = data.get('longitude')
        if longitude:
            long_part = longitude.split('.')[-1]
            if len(long_part) > 6:
                raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        
        latitude = data.get('latitude')
        if latitude:
            lat_part = latitude.split('.')[-1]
            if len(lat_part) > 6:
                raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        
        return data

    def create(self,data):
        data.pop('latitude')
        data.pop('longitude')
        return Air.objects.create(**data)


class AirUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    quarter = serializers.CharField(required=False)
    packages = serializers.CharField(required=False)

    class Meta:
        model = Air
        fields = (
            'quarter', 'packages', 'month', 'longitude', 'latitude', 'place_location', 
            'dateOfMonitoring', 'PM10', 'PM2_5', 'SO2', 'NOx', 'CO', 'AQI', 'Remarks'
        )

    def validate(self, data):
        long = data.get('longitude', '').split('.')[-1]
        if long and len(long) > 6:
            raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        lat = data.get('latitude', '').split('.')[-1]
        if lat and len(lat) > 6:
            raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        return data


class AirViewSerializer(GeoFeatureModelSerializer):
    class Meta:
        model=Air
        fields='__all__'
        geo_field='location'

class WaterSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=True)
    latitude=serializers.CharField(max_length=50,required=True)
    class Meta:
        model = water
        fields = ('quarter','packages','month', 'dateOfMonitoringTwo','longitude','latitude',
                    'qualityOfWater' , 'sourceOfWater' ,'waterDisposal','pH', 'trueColor', 'turbidity', 'odour', 'totalDissolvedSolids', 'totalAlkalinityAsCaCO3', 'totalHardnessAsCaCO3', 'calcium', 'magnesium', 'chlorides', 'fluoride', 'sulphate', 'nitrate', 'iron', 'zinc', 'copper', 'aluminum', 'nickel', 'manganese', 'phenolicCompounds', 'sulphide', 'cadmium', 'cyanide', 'lead', 'mercury', 'totalArsenic', 'totalChromium', 'totalColiform', 'eColi', 'WQI', 'place_location')


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


# Update
class WaterUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    quarter = serializers.CharField(required=False)
    packages = serializers.CharField(required=False)

    class Meta:
        model = water
        fields = (
            'quarter', 'packages', 'month', 'dateOfMonitoringTwo', 'longitude', 'latitude',
            'qualityOfWater', 'sourceOfWater', 'waterDisposal', 'pH', 'trueColor', 'turbidity',
            'odour', 'totalDissolvedSolids', 'totalAlkalinityAsCaCO3', 'totalHardnessAsCaCO3',
            'calcium', 'magnesium', 'chlorides', 'fluoride', 'sulphate', 'nitrate', 'iron',
            'zinc', 'copper', 'aluminum', 'nickel', 'manganese', 'phenolicCompounds', 'sulphide',
            'cadmium', 'cyanide', 'lead', 'mercury', 'totalArsenic', 'totalChromium',
            'totalColiform', 'eColi', 'WQI'
        )

    def validate(self, data):
        long = data.get('longitude', '').split('.')[-1]
        if long and len(long) > 6:
            raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        lat = data.get('latitude', '').split('.')[-1]
        if lat and len(lat) > 6:
            raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        return data
    
    

class NoiseSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=False)
    latitude=serializers.CharField(max_length=50,required=False)
    class Meta:
        model = Noise
        fields = ('quarter','month','packages','longitude','latitude' ,'dateOfMonitoringThree','noiseLevel_day', 'noiseLevel_night' , 'monitoringPeriod_day', 'monitoringPeriod_night', 'typeOfArea','isWithinLimit_day', 'isWithinLimit_night', 'place_location')

    def validate(self,data):
        required_fields = ['quarter', 'month', 'packages', 'longitude', 'latitude', 'dateOfMonitoringThree']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required")
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


class NoiseUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    quarter = serializers.CharField(required=False)
    packages = serializers.CharField(required=False)

    class Meta:
        model = Noise
        fields = (
            'quarter', 'month', 'packages', 'longitude', 'latitude', 'dateOfMonitoringThree',
            'noiseLevel_day', 'noiseLevel_night', 'monitoringPeriod_day', 'monitoringPeriod_night',
            'typeOfArea', 'isWithinLimit_day', 'isWithinLimit_night'
        )

    def validate(self, data):
        long = data.get('longitude', '').split('.')[-1]
        if long and len(long) > 6:
            raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        lat = data.get('latitude', '').split('.')[-1]
        if lat and len(lat) > 6:
            raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        return data


class Noiseviewserializer(GeoFeatureModelSerializer):
    class Meta:
        model = Noise
        fields = '__all__'
        geo_field='location'



class TreeManagementSerailizer(serializers.ModelSerializer):
    longitude=serializers.CharField(max_length=50,required=True)
    latitude=serializers.CharField(max_length=50,required=True)
    documents  = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True , required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)


    class Meta:
        model = ExistingTreeManagment
        fields = ('quarter','month','dateOfMonitoring','packages','longitude','latitude' ,'treeID','commanName' ,'botanicalName',
                    'condition', 'actionTaken', 'photographs', 'documents','remarks',)

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


class TreeManagementUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = ExistingTreeManagment
        fields = ('quarter', 'month', 'dateOfMonitoring', 'packages', 'longitude', 'latitude', 'treeID', 'commanName',
                  'botanicalName', 'condition', 'actionTaken', 'photographs', 'documents', 'remarks')

    def validate(self, data):
        long = data.get('longitude', '').split('.')[-1]
        if long and len(long) > 6:
            raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        lat = data.get('latitude', '').split('.')[-1]
        if lat and len(lat) > 6:
            raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        return data


class NewTreeManagmentUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = NewTreeManagement
        fields = ('tree', 'quarter', 'month', 'dateOfMonitoring', 'packages', 'longitude', 'latitude',
                  'commanName', 'botanicalName', 'condition', 'photographs', 'documents', 'remarks')

    def validate(self, data):
        long = data.get('longitude', '').split('.')[-1]
        if long and len(long) > 6:
            raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        lat = data.get('latitude', '').split('.')[-1]
        if lat and len(lat) > 6:
            raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        return data


class TreeManagmentviewserializer(GeoFeatureModelSerializer):
    class Meta:
        model = ExistingTreeManagment
        fields = '__all__'
        geo_field = 'location'


class NewTreeManagmentSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50,required=True)
    latitude = serializers.CharField(max_length=50,required=True)
    documents  = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True , required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)
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











class WasteTreatmentsSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=True)
    latitude=serializers.CharField(max_length=50,required=True)
    waste_longitude = serializers.CharField(max_length=50,required=True)
    waste_latitude = serializers.CharField(max_length=50,required=True)
    documents  = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True , required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)
    GISPermitsTransportationDocuments = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)
    TransportationVechicalHasPermissionDocuments = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)
    waste_collecting_location = models.CharField(max_length=255, null=True, blank=True)
    waste_handlingLocation = models.PointField(null=True, blank=True)
    waste_disposing_location = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        model  = WasteTreatments
        fields = ('quarter','month','packages','longitude','latitude'  ,'dateOfMonitoring' ,'waste_collecting_location', 'wasteOilQnt', 'waste_handlingLocation','CCPCPaintSludgeQnt', 'filterQnt', 'airFiltersQnt', 'usedCartridgesQnt', 'plasticQnt', 'paperQnt', 'woodQnt', 'bottlesQnt', 'rubberQnt', 'bioDegradableQuantity', 'bioMedicalQuantity', 'metalScrapeQuantity', 'eWasteQuantity', 'constructionWasteQuantity', 'iswasteOilQnt', 'isCCPCPaintSludgeQnt', 'isfilterQnt', 'isairFiltersQnt', 'isusedCartridgesQnt', 'isplasticQnt', 'ispaperQnt', 'iswoodQnt', 'isbottlesQnt', 'isrubberQnt', 'isbioDegradableQuantity', 'isbioMedicalQuantity', 'ismetalScrapeQuantity', 'iseWasteQuantity', 'isconstructionWasteQuantity', 'isGISPermitsTransportation', 'GISPermitsTransportationDocuments', 'isTransportationVechicalHasPermission', 'TransportationVechicalHasPermissionDocuments',
        'waste_disposing_location', 'waste_longitude' ,'waste_latitude', 'photographs' , 'documents','remarks')#'wastetype' ,


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


# Update Waste Treatment
class WasteTreatmentsUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    waste_longitude = serializers.CharField(max_length=50, required=False)
    waste_latitude = serializers.CharField(max_length=50, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    GISPermitsTransportationDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    TransportationVechicalHasPermissionDocuments = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    waste_collecting_location= models.CharField(max_length=255, null=True, blank=True)
    waste_handlingLocation = models.PointField(null=True, blank=True)
    waste_disposing_location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        model  = WasteTreatments
        fields = ('quarter','month','packages','longitude','latitude'  ,'dateOfMonitoring' ,'waste_collecting_location', 'wasteOilQnt', 'waste_handlingLocation','CCPCPaintSludgeQnt', 'filterQnt', 'airFiltersQnt', 'usedCartridgesQnt', 'plasticQnt', 'paperQnt', 'woodQnt', 'bottlesQnt', 'rubberQnt', 'bioDegradableQuantity', 'bioMedicalQuantity', 'metalScrapeQuantity', 'eWasteQuantity', 'constructionWasteQuantity', 'iswasteOilQnt', 'isCCPCPaintSludgeQnt', 'isfilterQnt', 'isairFiltersQnt', 'isusedCartridgesQnt', 'isplasticQnt', 'ispaperQnt', 'iswoodQnt', 'isbottlesQnt', 'isrubberQnt', 'isbioDegradableQuantity', 'isbioMedicalQuantity', 'ismetalScrapeQuantity', 'iseWasteQuantity', 'isconstructionWasteQuantity', 'isGISPermitsTransportation', 'GISPermitsTransportationDocuments', 'isTransportationVechicalHasPermission', 'TransportationVechicalHasPermissionDocuments',
        'waste_disposing_location', 'waste_longitude' ,'waste_latitude', 'photographs' , 'documents','remarks')#'wastetype' ,

    # #class Meta:
    #     model = WasteTreatments
    #     fields = ('quarter', 'month', 'packages', 'longitude', 'latitude', 'dateOfMonitoring',         'waste_collecting_location','wasteOilQnt', 'CCPCPaintSludgeQnt', 'filterQnt', 'airFiltersQnt', 'usedCartridgesQnt', 
    #               'plasticQnt', 'paperQnt', 'woodQnt', 'bottlesQnt', 'rubberQnt', 'bioDegradableQuantity', 
    #               'bioMedicalQuantity', 'metalScrapeQuantity', 'eWasteQuantity', 'constructionWasteQuantity', 
    #               'iswasteOilQnt', 'isCCPCPaintSludgeQnt', 'isfilterQnt', 'isairFiltersQnt', 'isusedCartridgesQnt', 
    #               'isplasticQnt', 'ispaperQnt', 'iswoodQnt', 'isbottlesQnt', 'isrubberQnt', 'isbioDegradableQuantity', 
    #               'isbioMedicalQuantity', 'ismetalScrapeQuantity', 'iseWasteQuantity', 'isconstructionWasteQuantity', 
    #               'isGISPermitsTransportation', 'GISPermitsTransportationDocuments', 
    #               'isTransportationVechicalHasPermission', 'TransportationVechicalHasPermissionDocuments', 
    #                'waste_longitude', 'waste_latitude', 'photographs', 'documents', 'remarks','waste_handlingLocation','waste_disposing_location')#'wastetype',

    def validate(self, data):
        if 'longitude' in data:
            long = data['longitude'].split('.')[-1]
            if len(long) > 6:
                raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        if 'latitude' in data:
            lat = data['latitude'].split('.')[-1]
            if len(lat) > 6:
                raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        if 'waste_longitude' in data:
            waste_long = data['waste_longitude'].split('.')[-1]
            if len(waste_long) > 6:
                raise serializers.ValidationError("Waste longitude must have at most 6 digits after the decimal point.")
        if 'waste_latitude' in data:
            waste_lat = data['waste_latitude'].split('.')[-1]
            if len(waste_lat) > 6:
                raise serializers.ValidationError("Waste latitude must have at most 6 digits after the decimal point.")
        return data
    

class wastetreatmentsViewserializer(GeoFeatureModelSerializer):
    class Meta:
        model = WasteTreatments
        fields = '__all__'
        geo_field= 'location'


class MaterialManagmentSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    longitude=serializers.CharField(max_length=50,required=True)
    latitude=serializers.CharField(max_length=50,required=True)
    storageLongitude = serializers.CharField(max_length=50,required=True)
    storageLatitude = serializers.CharField(max_length=50,required=True)
    materialStoragePhotograph = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)
    approvals = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True , required=False)

    documents  = serializers.FileField(allow_empty_file=True, use_url=False,write_only=True , required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False,write_only=True ,  required=False)

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
    
    
class MaterialManagmentUpdateSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(max_length=50, required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    storageLongitude = serializers.CharField(max_length=50, required=False)
    storageLatitude = serializers.CharField(max_length=50, required=False)
    materialStoragePhotograph = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    approvals = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    documents = serializers.FileField(allow_empty_file=True, use_url=False, write_only=True, required=False)
    photographs = serializers.ImageField(allow_empty_file=True, use_url=False, write_only=True, required=False)

    class Meta:
        model = MaterialManegmanet
        fields = ('quarter', 'month', 'packages', 'longitude', 'latitude', 'dateOfMonitoring', 'typeOfMaterial',
                  'source', 'sourceOfQuarry', 'materialStorageType', 'storageLongitude', 'storageLatitude',
                  'materialStorageCondition', 'materialStoragePhotograph', 'approvals', 'documents', 'photographs',
                  'remarks')
        
    def validate(self, data):
        if 'longitude' in data:
            long = data['longitude'].split('.')[-1]
            if len(long) > 6:
                raise serializers.ValidationError("Longitude must have at most 6 digits after the decimal point.")
        if 'latitude' in data:
            lat = data['latitude'].split('.')[-1]
            if len(lat) > 6:
                raise serializers.ValidationError("Latitude must have at most 6 digits after the decimal point.")
        if 'storageLongitude' in data:
            storage_long = data['storageLongitude'].split('.')[-1]
            if len(storage_long) > 6:
                raise serializers.ValidationError("Storage longitude must have at most 6 digits after the decimal point.")
        if 'storageLatitude' in data:
            storage_lat = data['storageLatitude'].split('.')[-1]
            if len(storage_lat) > 6:
                raise serializers.ValidationError("Storage latitude must have at most 6 digits after the decimal point.")
        return data





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
        fields = ['monitoringPeriod','location','packages','quarter', 'noiseLevel_day', 'monitoringPeriod_day', 'monitoringPeriod_night', 'noiseLevel_night', 'typeOfArea', 'isWithinLimit_day', 'isWithinLimit_night']

    def validate(self, data):
        missing_fields = [field for field in self.Meta.fields if field not in data or data[field] is None]

        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return data
    

class NoiseWhihinLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noise
        fields = ['noiseLevel_day', 'noiseLevel_night', 'typeOfArea']

    def validate(self, data):
        missing_fields = [field for field in self.Meta.fields if field not in data or data[field] is None]

        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return data

class WasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTreatments
        fields = [#'wastetype',
                  'location','packages','quarter','photographs','waste_disposing_location','remarks']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialManegmanet
        fields = ['approvals','sourceOfQuarry','typeOfMaterial','location','packages','quarter']

class WatermanamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = water
        fields = ['qualityOfWater','sourceOfWater','location','packages','quarter']


class GenerateAQISerializer(serializers.ModelSerializer):
    class Meta:
        model = Air
        fields = ['PM10', 'PM2_5', 'SO2', 'NOx', 'CO']

    def validate(self, data):

        if len(data.keys())<3 or tuple(data.values()).count(0)>=3:
            raise serializers.ValidationError("Concentrations of minimum three pollutants are required")
        if (not data.get('PM10',None) and not data.get('PM2_5',None)) or (data.get('PM10') == 0 and data.get('PM2_5') == 0):
            raise serializers.ValidationError("Either PM10 or PM2.5 data are required for AQI Generation")

        return data
    


class GenerateWQISerializer(serializers.ModelSerializer):
    pH = serializers.FloatField(required=True)
    totalHardnessAsCaCO3 = serializers.FloatField(required=True)
    calcium = serializers.FloatField(required=True)
    totalAlkalinityAsCaCO3 = serializers.FloatField(required=True)
    chlorides = serializers.FloatField(required=True)
    magnesium = serializers.FloatField(required=True)
    totalDissolvedSolids = serializers.FloatField(required=True)
    sulphate = serializers.FloatField(required=True)
    nitrate = serializers.FloatField(required=True)
    fluoride = serializers.FloatField(required=True)
    iron = serializers.FloatField(required=True)

    def to_internal_value(self, data):
        required_fields = [
            'pH', 'totalHardnessAsCaCO3', 'calcium', 'totalAlkalinityAsCaCO3', 'chlorides',
            'magnesium', 'totalDissolvedSolids', 'sulphate', 'nitrate', 'fluoride', 'iron'
        ]
        errors = {}
        for field in required_fields:
            if field not in data or data[field] in [None, '']:
                errors[field] = f"This field is required."

        if errors:
            raise serializers.ValidationError(errors)

        return super().to_internal_value(data)
    
    class Meta:
        model = water
        fields = ['pH', 'totalHardnessAsCaCO3', 'calcium', 'totalAlkalinityAsCaCO3', 'chlorides', 'magnesium', 'totalDissolvedSolids', 'sulphate', 'nitrate', 'fluoride', 'iron']
# need to write some validation


