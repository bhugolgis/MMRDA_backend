from django.urls import path, re_path
from .views import *

urlpatterns = [
    # For Social Monitoring
     path('SocialMonitoringDashboardCount/', SocialMonitoringCountDashboardView.as_view(), name='PAP Count'),
     path('SocialMonitoringPAPDashboardLanduseCategory', PAPCategoryDashboardView.as_view() , name='PAP Dashboard View'),
     path('CategoryWiseCompensationChart', CategoryWiseCompensationChart.as_view() , name='PAP Dashboard View'),
     
     path('IdentifiedPAPView', IdentifiedPAPDashboardView.as_view(), name='PAP Dashboard View'),

    # For Env Monitoring

     path('AirAQIChartDashboardView/',AirAQIChartDashboardView.as_view() , name = 'get-aqi-chart'),
     path('WaterWQIChartDashboardView/',WaterWQIChartDashboardView.as_view() , name = 'get-wqi-chart'),
     path('NoiseChartDashboardView/',NoiseChartDashboardView.as_view() , name = 'get-noise-chart'),
     path('DashboardEnvMonitoringGISMap/',DashboardEnvMonitoringGISMap.as_view() , name = 'get-dashboard-env-gis-map'),
     
     path('AirChartView/<str:month>/<int:year>',AirChartView.as_view() , name = 'AIr chart'),
     path('WaterCondition',WaterConditionChart.as_view() , name = 'Water condition char'),
     path('DashboardEnvMonReportsSubmitted/<str:month>/<str:year>',DashboardEnvMonReportsSubmitted.as_view() , name = 'Env Mon Reports Submitted'),
     path('ExistingTreeCount', ExistingTreeCount.as_view() , name = 'Exiting tree count'),
     path('typeofwastecount', WasteTypeCount.as_view() , name = 'Wastecount'),
     path('wastehandelingtype', WasteHandelingChart.as_view() , name = 'Wastecount'),
     path('Sourceofmaterial',MaterialSourceTypeCountChart.as_view() , name = 'Material'),
     path('Materilcondition',MaterialConditionChart.as_view() , name = 'Material'),


     # For OHS
     path('ManDaysLost/',ManDaysLostCountchart.as_view() , name = 'man-days-lost-count'),
     
     path('LabourcampFaciliteis<str:labourCampName>/<str:quarter>',LabourCampFacilitiesDashboardView.as_view(), name='labour Dashboard View'),
     path('campFaciliteisOverAll',LabourCampFacilitiesOverallDashboardView.as_view(), name='labour Dashboard View'),
     path('ConstructionSiteFaciliteis<str:constructionSiteName>/<str:quarter>',ConstructionChartView.as_view(), name='labour Dashboard View'),
     path('SiteFaciliteisOverall',ConstructionSiteFacilitiesOverallDashboardView.as_view(), name='labour Dashboard View'),
     path('RehabilitatedPAP', RehabilitatedPAPDashboardView.as_view(),  name='Rehabilated Dashboard View'),
          
     path('CashCompensationTypeChar', CashCompensationTypeCharView.as_view(), name='Cash Compensation Dashboard View'),
     path('Incidenttype',IncidenttypeCountchart.as_view() , name = 'Incident Type char'),
     
    
]
