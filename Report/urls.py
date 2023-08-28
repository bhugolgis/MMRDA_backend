from django.urls import path
from .views import *

urlpatterns = [
    # for social Monitoring
    path('labourcampreportpackage/<str:packages>/<str:labourCampName>',
         LabourcampReportPackageView.as_view(), name='Labourcamp Report View package'),
    path('labourcampreportquarter/<str:quarter>/<int:year>/<str:labourCampName>',
         LabourCampReportQuarterView.as_view(), name='Labourcamp Report View quarter'),

    path('constructioncampreportPackage/<str:packages>/<str:constructionSiteName>',
         ConstructionCampReportPackageView.as_view(), name='ConstructionSite Report'),
    path('constructioncampreportQuarter/<int:year>/<str:quarter>/<str:constructionSiteName>',
         ConstructionCampReportQuarterView.as_view(), name='ConstructionSite Report'),

    path('papreportpackage/<str:packages>',
         PAPReportPackageView.as_view(), name='PAP Report package'),
    path('papreportquarter/<str:quarter>/<int:year>',
         PAPReportQuarterView.as_view(), name='PAP Report quarter'),

    path('Rehabilationreportpackage/<str:packages>',
         RehabilitationReportPackageView.as_view(), name=' Rehabilitation Report package'),
    path('Rehabilationreportquarter/<str:quarter>/<int:year>',
         RehabilitationReportQuarterView.as_view(), name=' Rehabilitation Report quarter'),

    # Env Monitoring Routes

    path('airReportpackage/<str:packages>',
         AirReportPackageView.as_view(), name='AirReport Package View'),
    path('airReportquarter/<str:month>/<int:year>',
          AirReportQuarterView.as_view(), name='AirReport Package View'),

    path('noisereportpackage/<str:packages>',
         NoiseReportpackageView.as_view(), name='Noisereport Package View'),
    path('noisereportquarter/<str:month>/<int:year>',
         NoiseReportQuarterView.as_view(), name='Noisereport Package View'),

    path('waterReportpackage/<str:packages>',     
         waterReportPackageView.as_view(), name='Water Report Package View'),
    path('waterReportquarter/<str:month>/<int:year>',
         waterReportQuarterView.as_view(), name='Water Report Package View'),

    path('wastetreatmentpackage/<str:packages>',
         WasteTreatmentsPackageView.as_view(), name='Water Report Package View'),
    path('wastetreatmentquarter/<str:quarter>/<int:year>',
         WasteTreatmentsQuarterView.as_view(), name='Water Report Quarter View'),

    path('materialmanagementpackage/<str:packages>',MaterialManagementReporetpackageView.as_view(), name='Material Management Package'),
    path('materialmanagementquarter/<str:quarter>/<int:year>',
         MaterialManagementReporetQuarterView.as_view(), name='Material Management Quarter'),

     path('TreeMangementReportPackage/<str:packages>',
         TreeMangementReportPackage.as_view(), name='Tree Management Package'),
     path('TreeManagementReportQuarterView/<str:quarter>/<int:year>',
         TreeManagementReportQuarterView.as_view(), name='Tree Management Quarter'),


     path('TrainnigReporQuarter/<str:quarter>/<int:year>' , TrainnigReportQuarterView.as_view() , name = ' PreConstructionStageCompliance'),
     path('TrainnigReporpackage/<str:packages>' , TrainnigReportPackageView.as_view() , name = ' PreConstructionStageCompliance'),
    
     path('OccupationalHealthQuarter/<str:quarter>/<int:year>' , OccupationalHealthQuarterView.as_view() , name = ' PreConstructionStageCompliance'),
     path('OccupationalHealthPackage/<str:packages>' , OccupationalHealthPackageView.as_view() , name = ' PreConstructionStageCompliance'),
     
     
     # path('MetroLine4Aligment' , MetroLine4View.as_view() , name = 'MetroLine4'),
     # path('package54Aligment' , Package54AlignmentView.as_view() , name = 'Package54AlignmentView'),
     # path('package12Aligment' , package12AlignmentView.as_view() , name = 'package12Aligment'),
     # path('package11Aligment' , package11AlignmentView.as_view() , name = 'package11Aligment'),
     # path('package10Aligment' , package10AlignmentView.as_view() , name = 'package10Aligment'),
     # path('package09Aligment' , package09AlignmentView.as_view() , name = 'package09Aligment'),
     # path('package08Aligment' , package08AlignmentView.as_view() , name = 'package08Aligment'),
     # path('MetroStation' , MetroStationView.as_view() , name = 'MetroStationView '),
     # path('ProjectAffectedTrees' , ProjectAffectedTreesView.as_view() , name = 'MetroStationView '),
    

]
