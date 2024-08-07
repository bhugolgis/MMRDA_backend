from django.urls import path
from .views import *

urlpatterns = [
    # for social Monitoring
     path('SocialMonitoringPAPDashboardLanduseCategory', PAPCategoryDashboardView.as_view() , name='PAP Dashboard View'),
     path('CategoryWiseCompensationChart', CategoryWiseCompensationChart.as_view() , name='PAP Dashboard View'),
     path('IdentifiedPAPView', IdentifiedPAPDashboardView.as_view(), name='PAP Dashboard View'),
     
     path('SocialMonitoringDashboardCount/', SocialMonitoringCountDashboardView.as_view(), name='PAP Count'),

     path('LabourcampFaciliteis<str:labourCampName>/<str:quarter>',LabourCampFacilitiesDashboardView.as_view(), name='labour Dashboard View'),
     path('campFaciliteisOverAll',LabourCampFacilitiesOverallDashboardView.as_view(), name='labour Dashboard View'),
     path('ConstructionSiteFaciliteis<str:constructionSiteName>/<str:quarter>',ConstructionChartView.as_view(), name='labour Dashboard View'),
     path('SiteFaciliteisOverall',ConstructionSiteFacilitiesOverallDashboardView.as_view(), name='labour Dashboard View'),
     path('RehabilitatedPAP', RehabilitatedPAPDashboardView.as_view(),  name='Rehabilated Dashboard View'),
          
     path('CashCompensationTypeChar', CashCompensationTypeCharView.as_view(), name='Cash Compensation Dashboard View'),

     path('ExistingTreeCount', ExistingTreeCount.as_view() , name = 'Exiting tree count'),

     path('typeofwastecount', WasteTypeCount.as_view() , name = 'Wastecount'),
     path('wastehandelingtype', WasteHandelingChart.as_view() , name = 'Wastecount'),

     path('Sourceofmaterial',MaterialSourceTypeCountChart.as_view() , name = 'Material'),
     path('Materilcondition',MaterialConditionChart.as_view() , name = 'Material'),
     path('Incidenttype',IncidenttypeCountchart.as_view() , name = 'Incident Type char'),
     path('WaterCondition',WaterConditionChart.as_view() , name = 'Water condition char'),
     path('AirChartView/<str:month>/<int:year>',AirChartView.as_view() , name = 'AIr chart'),
     path('AirAQIChartDashboardView/<str:quarter>/<str:packages>',AirAQIChartDashboardView.as_view() , name = 'AIr chart'),
     path('WaterWQIChartDashboardView/<str:quarter>/<str:packages>',WaterWQIChartDashboardView.as_view() , name = 'WQI chart'),
     path('NoiseChartDashboardView/<str:quarter>/<str:packages>',NoiseChartDashboardView.as_view() , name = 'Noise chart'),
     path('ManDaysLost/<str:quarter>/<str:packages>',ManDaysLostCountchart.as_view() , name = 'Man Days Lost Count'),
     path('DashboardEnvMonitoringGISMap/<str:quarter>/<str:packages>',DashboardEnvMonitoringGISMap.as_view() , name = 'WQI chart'),
     path('DashboardEnvMonReportsSubmitted/<str:month>/<str:year>',DashboardEnvMonReportsSubmitted.as_view() , name = 'Env Mon Reports Submitted'),


    
]
