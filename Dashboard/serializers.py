from rest_framework import serializers
from SocialMonitoring.models import *
from EnvMonitoring.models import *
from Training.models import *


class PAPDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAP
        fields = ('categoryOfPap' ,)

class RehabilationDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rehabilitation
        fields = '__all__'


class LabourcampDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabourCamp
        fields = ('id','labourCampName','toiletCondition' ,'drinkingWaterCondition' ,'demarkationOfPathwaysCondition',
                'signagesLabelingCondition','kitchenAreaCondition','fireExtinguishCondition','roomsOrDomsCondition',
                'segregationOfWasteCondition')


class ConstructionSiteDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionSiteDetails
        fields = ('id','constructionSiteName','toiletCondition' ,'drinkingWaterCondition' ,'demarkationOfPathwaysCondition',
                'signagesLabelingCondition',)


class ExistingTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExistingTreeManagment
        fields = ('quarter','month','dateOfMonitoring','packages','location','treeID','commanName' ,'botanicalName',
                    'condition', 'noOfTreeCut','actionTaken', 'photographs', 'documents','remarks')

class OccupationalHealthSafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = occupationalHealthSafety 
        fields = '__all__'

class waterserializer(serializers.ModelSerializer):
    class Meta:
        model = water   
        fields = '__all__'

class AirChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Air
        fields = ('month','PM10','standardPM10','SO2',
                   'standardSO2','O3','standardO3','NOx', 'standardNOx','AQI' )