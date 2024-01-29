from django.urls import path
from .views import *

urlpatterns = [
    # for social Monitoring
     path('SocialMonitoringPAPDashboardLanduseCategory', PAPCategoryDashboardView.as_view() , name='PAP Dashboard View'),
     path('CategoryWiseCompensationChart', CategoryWiseCompensationChart.as_view() , name='PAP Dashboard View'),
     path('IdentifiedPAPView', IdentifiedPAPDashboardView.as_view(), name='PAP Dashboard View'),
     
     path('SocialMonitoringDashboardCount/<str:quarter>/<str:packages>', SocialMonitoringCountDashboardView.as_view(), name='PAP Count'),

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
    
]
