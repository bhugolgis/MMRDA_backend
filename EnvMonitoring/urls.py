
from django.urls import path
from .views import *

urlpatterns = [
# path('envmonitoring' , EnvMonitoringView.as_view() , name = 'envmonitoring'),

    path('PostSensorLocationDetails' , PostSensorLocationDetails.as_view() , name = 'PostSensorLocationDetails'),
    path('GetsensorLocationDetails' , GetSensorLocationDetails.as_view() , name = 'PostSensorLocationDetails'),
    path('generate-aqi' , GenerateAQI.as_view() , name = 'GenerateAQI'),
    path('generate-wqi' , GenerateWQI.as_view() , name = 'GenerateWQI'),
    path('air' , AirView.as_view() , name = 'Air Details'),
    path('air/<int:id>' , AirView.as_view() , name = 'get-air-details'),
    path('air/<int:id>' , AirUpdateView.as_view() , name = 'Air Details'),
    path('airList', AirListView.as_view() , name = 'ListAirView'),

    path('water' , WaterView.as_view() , name = 'water Details'),
    path('water/<int:id>' , WaterView.as_view() , name = 'get-water-details'),
    path('water/<int:id>' , WaterUpdateView.as_view() , name = 'water Details'),
    path('waterList' , waterListView.as_view() , name = 'water Details'),

    path('noise' , NoiseView.as_view() , name = "Noise Details"),
    path('noise/<int:id>' , NoiseView.as_view() , name = "get-noise-details"),
    path('noise/<int:id>' , NoiseUpdateView.as_view() , name = "Noise Details"),
    path('noiseList' ,NoiseListView.as_view() , name = "Noise"),
    path('noiseWhithinLimit' ,NoiseWhithinLimitAPI.as_view() , name = "noiseWhithinLimit"),

    # path('envview' , envMonitoringView.as_view() , name = 'EnvQualityMonitoring'),
    path('IdentifiedTree' , ExistingTreeManagementView.as_view() , name = "Tree Management"),
    path('existing-tree/<int:id>' , ExistingTreeManagementGetUpdateDeleteView.as_view() , name = "get-existing-tree"),
    path('existing-tree/<int:id>' , ExistingTreeManagementGetUpdateDeleteView.as_view() , name =" update-existing-tree"),
    path('existing-tree/<int:id>' , ExistingTreeManagementGetUpdateDeleteView.as_view() , name =" delete-existing-tree"),
    path('treeView' , ExistingTereeManagementView.as_view() , name = "Tree Management list"),
    path('GetExistingTreeIDView/<str:treeID>' , GetExistingTreeIDView.as_view() , name = "Tree Management list"),

    path('NewTree' , NewTereeManagementView.as_view() , name = "Tree Management"),
    path('new-tree/<int:id>' , NewTreeManagementGetUpdateDeleteView.as_view() , name = "get-new-tree"),
    path('new-tree/<int:id>' , NewTreeManagementGetUpdateDeleteView.as_view() , name = "update-new-tree"),
    path('new-tree/<int:id>' , NewTreeManagementGetUpdateDeleteView.as_view() , name = "delete-new-tree"),

    path('waste' , WasteTreatmentsView.as_view() , name = "Waste Management"),
    path('waste-management/<int:id>' , WasteTreatmentsGetUpdateDeleteView.as_view() , name = "get-waste-management"),
    path('waste-management/<int:id>' , WasteTreatmentsGetUpdateDeleteView.as_view() , name = "update-waste-management"),
    path('waste-management/<int:id>' , WasteTreatmentsGetUpdateDeleteView.as_view() , name = "delete-waste-management"),
    
    path('materialmanagement' , MaterialSourcingView.as_view() , name = "MaterialSourcingCreate"),
    path('material-management/<int:id>' , MaterialSourcingGetUpdateDeleteView.as_view() , name = "get-material-management"),
    path('materialManagement/<int:id>' , MaterialSourcingGetUpdateDeleteView.as_view() , name = "update-material-management"),
    path('materialManagement/<int:id>' , MaterialSourcingGetUpdateDeleteView.as_view() , name = "delete-material-management"),

    path('treemanagement/<str:packages>' , TreemanagmentAPI.as_view() , name = "TreemanagmentAPI"),
    path('Airmanagement/<str:packages>' , AirAPI.as_view() , name = "AirAPI"),
    path('Noisemanagement/<str:packages>' , NoiseAPI.as_view() , name = "NoiseAPI"),
    path('wastemanagement/<str:packages>' , WasteTreatmentsAPI.as_view() , name = "waste_management"),
    path('materialmanagement/<str:packages>' , MaterialSourcingAPI.as_view() , name = "MaterialSourcingAPI"),
    path('watermanagement/<str:packages>' , WatermanagmentAPI.as_view() , name = "WatermanagmentAPI"),
 ]