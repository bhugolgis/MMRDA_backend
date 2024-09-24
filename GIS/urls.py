from django.urls import path , re_path
from .views import *

urlpatterns = [
   
     
     path('MetroStation' , MetroStationView.as_view() , name = 'MetroStationView '),
     path('gis-portal-existing-tree' , GISPortalExistingTreeManagmentView.as_view() , name = 'get-existing-tree'),
 #aligments
     path('MetroLine4Aligment' , MetroLine4View.as_view() , name = 'metro-line-4-and-4a'),
     path('MetroLine4And4AAligment' , MetroLine4And4AView.as_view() , name = 'MetroLine4'),
     path('package54Aligment' , Package54AlignmentView.as_view() , name = 'Package54AlignmentView'),
     path('package12Aligment' , package12AlignmentView.as_view() , name = 'package12Aligment'),
     path('package11Aligment' , package11AlignmentView.as_view() , name = 'package11Aligment'),
     path('package10Aligment' , package10AlignmentView.as_view() , name = 'package10Aligment'),
     path('package09Aligment' , package09AlignmentView.as_view() , name = 'package09Aligment'),
     path('package08Aligment' , package08AlignmentView.as_view() , name = 'package08Aligment'),

#start and end points
     path('Start_end_points',Start_end_points.as_view() , name= 'Start_end_points'  ),
     path('All_Start_End_Point', All_start_end_points.as_view() , name='All_Start_End_Point'),
     path('PackageCa08_Start_End_Point', Package08_start_end_points.as_view() , name='PackageCa08_Start_End_Point'),
     path('PackageCa09_Start_End_Point', Package09_start_end_points.as_view() , name='PackageCa09_Start_End_Point'),
     path('PackageCa10_Start_End_Point', Package10_start_end_points.as_view() , name='PackageCa10_Start_End_Point'),
     path('PackageCa11_Start_End_Point', Package11_start_end_points.as_view() , name='PackageCa11_Start_End_Point'),
     path('PackageCa12_Start_End_Point', Package12_start_end_points.as_view() , name='PackageCa12_Start_End_Point'),
     path('PackageCa54_Start_End_Point', Package54_start_end_points.as_view() , name='PackageCa54_Start_End_Point'),
 #package wise metro stations
     path('PackageCa08_metroStations',PackageCa08_metroStations.as_view(),name='PackageCa08_metroStations'),
     path('PackageCa09_metroStations',PackageCa09_metroStations.as_view(),name='PackageCa09_metroStations'),
     path('PackageCa10_metroStations',PackageCa10_metroStations.as_view(),name='PackageCa10_metroStations'),
     path('PackageCa11_metroStations',PackageCa11_metroStations.as_view(),name='PackageCa11_metroStations'),
     path('PackageCa12_metroStations',PackageCa12_metroStations.as_view(),name='PackageCa12_metroStations'),
     path('PackageCa54_metroStations',PackageCa54_metroStations.as_view(),name='PackageCa54_metroStations'),
     
     
     
     
     
     
     path('projectAffectedPersons' , projectAffectedPersonsView.as_view() , name = 'projectAffectedPersons '),
     path('ProjectAffectedTrees' , ProjectAffectedTreesView.as_view() , name = 'MetroStationView '),
     re_path(r'PAP-Type-Of-Structure/(?P<categoryOfPap>.+)$' , PAPTypeOfStructureView.as_view() , name = 'MetroStationView '),
     re_path(r'Rehabilitation-compensation-status/(?P<compensationStatus>.+)$' , RehabilitationTypeOfStructureView.as_view() , name = 'MetroStationView '),
     path('MaterialManagementStorageGISQuarterView/<str:condition>',MaterialManagementStorageGISQuarterView.as_view(), name='Material Management Package'),
     path('MaterialManagementSourceGISQuarterView',MaterialManagementSourceGISQuarterView.as_view(), name='Material Management Package'),
     path('IncidentTypeGISQuarterView/<str:typeOfIncident>/<str:quarter>',IncidentTypeGISQuarterView.as_view(), name='Material Management Package'),
     path('occupationalHealthSafetyGISView/<int:year>/<str:quarter>/<str:package>',occupationalHealthSafetyGISView.as_view(), name='Material Management Package'),
     path('labourcampreportpackage/<str:packages>/<str:labourCampName>',LabourcampReportPackageView.as_view(), name='Labourcamp Report View package'),
              
]
