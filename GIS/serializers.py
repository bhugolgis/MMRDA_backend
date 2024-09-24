from rest_framework.serializers import ModelSerializer
from SocialMonitoring.models import *
from EnvMonitoring.models import *
from rest_framework.validators import ValidationError
from Report.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from Training.models import *
from .models import *
from rest_framework.serializers import ModelSerializer


class MetroLine4And4AAlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MmrdaAlignment4326
        fields = ('gid' ,'name' )
        geo_field= ('geom')
        

class MetroLine4AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MmrdaNew
        fields = ('gid' ,'name' )
        geo_field= ('geom')


class Package54AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MmrdaCa54Alignment4326
        fields = ('gid' ,'name' )
        geo_field= ('geom')

class Package12AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MmrdaCa12Alignment4326
        fields = ('gid' ,'name')
        geo_field= ('geom')

class Package11AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MmrdaCa11Alignment4326
        fields = ('gid' ,'name' )
        geo_field= ('geom')


class Package10AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MmrdaCa10Alignment4326
        fields = ('gid' ,'name' )
        geo_field= ('geom')


class Package09AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MmrdaCa09Alignment4326
        fields = ('gid' ,'name' ,)
        geo_field= ('geom')



class Package08AlignmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model =  MmrdaCa08Alignment4326
        fields = ('gid' ,'name')
        geo_field= ('geom')



class Start_end_points_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  StartEndPoints
        fields = ('gid' ,'fid')#, 'name')
        geo_field= ('geom')


class All_start_end_point_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  AllStartEndPoints
        fields = ('gid' ,'id','names')
        geo_field= ('geom')

class Package08_start_end_point_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa08StartEndPoint
        fields = ('gid' ,'id')
        geo_field= ('geom')



class Package09_start_end_point_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa09StartEndPoint
        fields = ('gid' ,'id')
        geo_field= ('geom')




class Package10_start_end_point_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa10StartEndPoint
        fields = ('gid' ,'id')
        geo_field= ('geom')


class Package11_start_end_point_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa11StartEndPoint
        fields = ('gid' ,'id')
        geo_field= ('geom')


class Package12_start_end_point_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa12StartEndPoint
        fields = ('gid' ,'id')
        geo_field= ('geom')


class Package54_start_end_point_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa54StartEndPoint
        fields = ('gid' ,'id')
        geo_field= ('geom')




class PackageCa08_metroStations_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa08MetroStations
        fields = ('gid' ,'id' )#,'name')
        geo_field= ('geom')


class PackageCa09_metroStations_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa09MetroStations
        fields = ('gid' ,'id' )#,'name')
        geo_field= ('geom')
    
class PackageCa10_metroStations_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa10MetroStations
        fields = ('gid' ,'id' )#,'name')
        geo_field= ('geom')


class PackageCa11_metroStations_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa11MetroStations
        fields = ('gid' ,'id' )#,'name')
        geo_field= ('geom')


class PackageCa12_metroStations_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa12MetroStations
        fields = ('gid' ,'id' )#,'name')
        geo_field= ('geom')        


class PackageCa54_metroStations_Serializer(GeoFeatureModelSerializer):
    class Meta:
        model =  PackageCa54MetroStations
        fields = ('gid' ,'id' )#,'name')
        geo_field= ('geom')



class MetroStationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Station
        fields = ('gid' , 'name')
        geo_field= ('geom')


class GISPortalExistingTreeManagmentSerailizer(GeoFeatureModelSerializer):
    class Meta:
        model = ExistingTreeManagment
        fields = ('quarter', 'month', 'dateOfMonitoring', 'packages', 'treeID','commanName' ,'botanicalName',
                    'condition', 'actionTaken', 'remarks',)
        geo_field= ('location')


class ProjectAffectedTreesSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ProjectAffectedTrees
        fields = ('gid','tree_no_field' , 'common_nam' , 'botanical' ,'proposed_a','condition','survey_dat')
        geo_field= ('geom')


class projectAffectedPersonsSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Projectaffectedperson
        fields = ('gid' , 'pap_id','name' , 'category' , 'date')
        geo_field= ('geom')

        
class PAPGISSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PAP
        fields = ('id','quarter', 'packages','dateOfMonitoring','dateOfIdentification','PAPID', 
                  'addressLine1','streetName','pincode','eligibility', 'categoryOfPap', 
                  'areaOfAsset','legalStatus','legalDocuments',
                   'actionTaken', 'notAgreedReason','remarks' )
        geo_field= ('location')


class RehabilitationGISSerializer(GeoFeatureModelSerializer):
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



class materialManagementStorageGISSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MaterialManegmanet
        fields = ('id','quarter','month','packages','dateOfMonitoring',
         'typeOfMaterial','source','sourceOfQuarry','materialStorageType','storageLocation',
         'materialStorageCondition','materialStoragePhotograph','approvals' ,'photographs',
          'documents','remarks')
        geo_field= ('location')





class materialManagementSourceGISSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MaterialManegmanet
        fields = ('id','quarter','month','packages','dateOfMonitoring', 'location' , 
         'typeOfMaterial','source','sourceOfQuarry','materialStorageType','storageLocation',
         'materialStorageCondition','materialStoragePhotograph','approvals' ,'photographs',
          'documents','remarks')
        geo_field= ('storageLocation')


class IncidentTypeGISQuarterSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = occupationalHealthSafety
        fields = '__all__'
        geo_field = 'incidentLocation'



class occupationalHealthSafetyGISConditionSerializer(ModelSerializer):
    class Meta:
        model = occupationalHealthSafety
        fields = ('joiningMedicalCheckupCondition' , 'ppeKitCondition' ,'trainingToWorkersCondition' ,
                  'houseKeepingCondition' , 'powerSupplySystemCondition' , 'assemblyAreaCondition' ,
                  'ambulanceArrangementCondition' , 'toiletFacilityCondition' ,
                  'safeMomentPassageCondition' , 'materialKeepingPracticeCondition' , 'accidentalCheckCondition' ,
                 'safetyGearStatusCondition' , 'barricadingCondition' )
 

class occupationalHealthSafetyGISSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = occupationalHealthSafety
        fields = '__all__'
        geo_field = 'location'
       





