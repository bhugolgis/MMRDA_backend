from rest_framework.serializers import ModelSerializer
from SocialMonitoring.models import *
from EnvMonitoring.models import *
from rest_framework.validators import ValidationError
from Report.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from Training.models import *

# The above class is a serializer in Python that is used to serialize and validate data for a
# LabourCampReport model.
class LabourcampReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = LabourCamp
        fields =('id','quarter', 'packages','dateOfMonitoring', 'labourCampName', 'labourCampId',
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
        geo_field= ('location')



    def validate(self, data):
        if data['packages'] == '' or data['packages'] == None:
            raise ValidationError('packages can not be empty')
        if data['labourCampName'] == '' or data['labourCampName'] ==None:
            raise ValidationError('labourCampName can not be empty')
        return data


class LabourCampDeatilViewSerialzier(ModelSerializer):
    class Meta:
        model = LabourCamp
        fields = "__all__"

# The ConstructionCampReportSerializer class is a serializer for the ConstructionSiteDetails model
# with specific fields and a geo_field for location.
class ConstructionCampReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ConstructionSiteDetails
        fields = ('id','quarter', 'packages','dateOfMonitoring' ,'constructionSiteName' , 'constructionSiteId',
                    'isDemarkationOfPathways','demarkationOfPathwaysCondition','demarkationOfPathwaysPhotographs','demarkationOfPathwaysRemark' ,
                    'isSignagesLabelingCheck','signagesLabelingCondition' ,'signagesLabelingPhotographs','signagesLabelingRemarks',
                    'isRegularHealthCheckup','regularHealthCheckupCondition','regularHealthCheckupPhotographs','regularHealthCheckupRemarks',
                    'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition','availabilityOfDoctorPhotographs','availabilityOfDoctorRemarks',
                        'isFirstAidKit','firstAidKitCondition' ,'firstAidKitPhotographs','firstAidKitRemarks',
                    'isDrinkingWaterCheck','drinkingWaterCondition' ,'drinkingWaterPhotographs','drinkingWaterRemarks',
                        'isToilet', 'toiletCondition','toiletPhotograph','toiletRemarks',
                        'genralphotographs','documents','remarks')
        geo_field= ('location')



# The PAPReportSerializer class is a serializer for the PAP model that includes specific fields and a
# geo_field for location.
class PAPReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PAP
        fields = ('id','quarter', 'packages','dateOfMonitoring','dateOfIdentification','PAPID','nameOfPAP',
                  'addressLine1','streetName','pincode','eligibility', 'categoryOfPap',
                  'areaOfAsset','typeOfStructure','legalStatus','legalDocuments',
                   'actionTaken', 'notAgreedReason','remarks' )
        geo_field= ('location')

class RehabilitationReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Rehabilitation
        fields = "__all__"
        # fields =  ('id','ID','dateOfRehabilitation' ,'PAPID', 'PAPName' ,'cashCompensation', 'compensationStatus',
        #            'typeOfCompensation', 'otherCompensationType' ,'addressLine1','streetName','pincode',
        #            'isShiftingAllowance','shiftingAllowanceAmount','isLivelihoodSupport', 'livelihoodSupportAmount','livelihoodSupportCondition',
        #            'livelihoodSupportPhotograph','livelihoodSupportRemarks','isTraining','trainingCondition',
        #            'trainingPhotograph' ,'trainingRemarks' , 'typeOfTenaments'  ,'areaOfTenament' , 'tenamentsPhotograph',
        #             'isRelocationAllowance' ,'RelocationAllowanceAmount' ,'isfinancialSupport',
        #            'financialSupportAmount','isCommunityEngagement','isEngagementType', 'photographs' , 'documents','remarks')
        geo_field= ('location')



'''----------------------- Env Monitoring Report Serilaizer------------------------------'''
# The AirReportSerializer class is a serializer for the Air model that includes specific fields and a
# geo_field for location.

class AirReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Air
        fields =('id','quarter','packages','month','dateOfMonitoring','PM10','PM2_5',
                 'SO2','NOx','CO','AQI','Remarks')
        geo_field= ('location')

# The NoiseReportSerializer class is a serializer for the Noise model that includes specific fields
# and a geo_field for location.
class NoiseReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Noise
        fields = ('id','location' ,'quarter','month','packages','dateOfMonitoringThree' ,'noiseLevel' , 'monitoringPeriod', )
        geo_field= ('location')

# The waterReportSerializer class is a serializer for the water model that includes specific fields
# and a geo_field for location.
class waterReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = water
        fields =('id','quarter','packages','month', 'dateOfMonitoringTwo','qualityOfWater' , 'sourceOfWater' ,'waterDisposal')
        geo_field= ('location')


# The class `wasteTreatmentsSerializer` is a serializer for the `WasteTreatments` model that includes
# specific fields and a geo field.
class wasteTreatmentsSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = WasteTreatments
        fields = ('id','quarter','month','packages','dateOfMonitoring' , 'wastetype' ,'quantity',
                    'wastehandling' , 'wasteHandlingLocation', 'photographs' , 'documents','remarks')
        geo_field= ('location')


# The class `materialManagementSerializer` is a serializer class in Python that is used for
# serializing and deserializing data related to material management.
class materialManagementSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MaterialManegmanet
        fields = ('id','quarter','month','packages','dateOfMonitoring',
         'typeOfMaterial','source','sourceOfQuarry','materialStorageType','storageLocation',
         'materialStorageCondition','materialStoragePhotograph','approvals' ,'photographs',
          'documents','remarks')
        geo_field= ('location')


# The `treeManagementSerializer` class is a serializer for the `ExistingTreeManagment` model with
# specific fields and a geo field.
class treeManagementSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ExistingTreeManagment
        fields = ('id','quarter','month','dateOfMonitoring','packages','treeID','commanName' ,'botanicalName',
                    'condition', 'noOfTreeCut','actionTaken', 'photographs', 'documents','remarks')

        geo_field= ('location')




# The class MetroLine4AlignmentSerializer is a serializer for the MmrdaNew model with fields gid and
# name, and a geo_field geom.
class MetroLine4AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MmrdaNew
        fields = ('gid' ,'name' )
        geo_field= ('geom')


class Package54AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Package54Alignment
        fields = ('gid' ,'name' )
        geo_field= ('geom')

class Package12AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Package12Alignment
        fields = ('gid' ,'name')
        geo_field= ('geom')

class Package11AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Package11Alignment
        fields = ('gid' ,'name' )
        geo_field= ('geom')


class Package10AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Package10Alignment
        fields = ('gid' ,'name' )
        geo_field= ('geom')


class Package09AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Package09Alignment
        fields = ('gid' ,'name' ,)
        geo_field= ('geom')



class Package08AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Package08Alignment
        fields = ('gid' ,'name')
        geo_field= ('geom')


class MetroStationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Station
        fields = ('gid' , 'name')
        geo_field= ('geom')


class ProjectAffectedTreesSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ProjectAffectedTrees
        fields = ('gid','tree_no_field' , 'common_nam' , 'botanical' ,'proposed_a','condition','survey_dat')
        geo_field= ('geom')




class TrainnigReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model= traning
        fields = ('quarter' , 'packages' , 'dateOfMonitoring',
                  'category' , 'traningTitle' , 'noOfAttends' , 'noOfTimesTrainingConducted',
                  'male','female' , 'inchargePerson', 'traninigInitiatedBy' , 'conductDate' ,
                  'traningDate' , 'photographs' , 'documents')
        geo_field = ('location')


class OccupationalHealthQuarterSeialzier(GeoFeatureModelSerializer):
    class Meta:
        model = occupationalHealthSafety
        # fields = '__all__'
        exclude = ['user' ]
        geo_field = ('location')























# import io
# from PIL import Image
# from rest_framework import serializers
# from django.core.files.base import ContentFile
# import base64
# class CompressedImageField(serializers.ImageField):
#     def to_internal_value(self, data):
#         print("kjsdf ")
#         if isinstance(data, str) and data.startswith('data:image'):
#             # Base64 encoded image - decode
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

#         # Compress the image
#         image = Image.open(data)
#         io_stream = io.BytesIO()
#         image.save(io_stream, format='JPEG', quality=60)
#         return ContentFile(io_stream.getvalue(), name=data.name)

# from Training.models import ContactusImage
# class GisSerializer(serializers.ModelSerializer):
#     # image = CompressedImageField()

#     model = ContactusImage
#     fields = ('image',)

