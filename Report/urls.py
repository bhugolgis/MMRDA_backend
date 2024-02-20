from django.urls import path,include
from .views import *
# from .views import LabourcampReportExcelViewDetailList
from rest_framework import routers

urlpatterns = [
     
    path('labourcampreportpackageExcelDownloadView/', labourcampreportpackageExcelDownloadView.as_view(), name='labourcampreportpackageExcel'),
    # for social Monitoring
    path('labourcampreportpackage/<str:packages>/<str:labourCampName>',
         LabourcampReportPackageView.as_view(), name='Labourcamp Report View package'),



    path('labourcampreportquarter/<str:quarter>/<int:year>/<str:labourCampName>',
         LabourCampReportQuarterView.as_view(), name='Labourcamp Report View quarter'),
    path('labourQuarterExcelDownload/', labourQuarterExcelDownload.as_view(), name='labourQuarterExcelDownload'),


    path('constructioncampreportPackage/<str:packages>/<str:constructionSiteName>',
         ConstructionCampReportPackageView.as_view(), name='ConstructionSite Report'),
    path('ConstructionCampReportPackageExcelDownload/', ConstructionCampReportPackageExcelDownload.as_view(), name='labourQuarterExcelDownload'),
    
    
    
    path('constructioncampreportQuarter/<int:year>/<str:quarter>/<str:constructionSiteName>',
         ConstructionCampReportQuarterView.as_view(), name='ConstructionSite Report'),
    path('ConstructionCampReportQuaterExcelDownload/', ConstructionCampReportQuaterExcelDownload.as_view(), name='ConstructionCampReportQuaterExcelDownload'),



    
    
    
    
    path('papreportpackage/<str:packages>',
         PAPReportPackageView.as_view(), name='PAP Report package'),
    path('PAPReportPackageExcelDownload/', PAPReportPackageExcelDownload.as_view(), name='PAPReportPackageExcelDownload'),
    
    
    path('papreportquarter/<str:quarter>/<int:year>',
         PAPReportQuarterView.as_view(), name='PAP Report quarter'),
    path('PAPReportExcelQuaterExcelDownload/', PAPReportExcelQuaterExcelDownload.as_view(), name='PAPReportExcelQuaterExcelDownload'),



    path('Rehabilationreportpackage/<str:packages>',
         RehabilitationReportPackageView.as_view(), name=' Rehabilitation Report package'),
    path('RehabilitationReportPackageExcelDownload/', RehabilitationReportPackageExcelDownload.as_view(), name='RehabilitationReportPackageExcelDownload'),
    
    
    path('Rehabilationreportquarter/<str:quarter>/<int:year>',
         RehabilitationReportQuarterView.as_view(), name=' Rehabilitation Report quarter'),
    path('RehabilitationReportQuarterExcelDownload/', RehabilitationReportQuarterExcelDownload.as_view(), name='RehabilitationReportQuarterExcelDownload'),



    # Env Monitoring Routes

    path('airReportpackage/<str:packages>',
         AirReportPackageView.as_view(), name='AirReport Package View'),
    path('AirReportReportPackageExcelDownload/', AirReportReportPackageExcelDownload.as_view(), name='AirReportReportPackageExcelDownload'),
    
    
    path('airReportquarter/<str:month>/<int:year>',
          AirReportQuarterView.as_view(), name='AirReport Package View'),
    path('AirReportQuarterExcelDownload/', AirReportQuarterExcelDownload.as_view(), name='AirReportQuarterExcelDownload'),



    path('noisereportpackage/<str:packages>',
         NoiseReportpackageView.as_view(), name='Noisereport Package View'),
    path('NoiseReportReportPackageExcelDownload/', NoiseReportReportPackageExcelDownload.as_view(), name='NoiseReportReportPackageExcelDownload'),



    path('noisereportquarter/<str:month>/<int:year>',
         NoiseReportQuarterView.as_view(), name='Noisereport Package View'),

    path('NoiseReportQuarterExcelDownload/', NoiseReportQuarterExcelDownload.as_view(), name='NoiseReportQuarterExcelDownload'),




    path('waterReportpackage/<str:packages>',     
         waterReportPackageView.as_view(), name='Water Report Package View'),
    path('waterReportReportPackageExcelDownload/', waterReportReportPackageExcelDownload.as_view(), name='waterReportReportPackageExcelDownload'),

    path('waterReportquarter/<str:month>/<int:year>',
         waterReportQuarterView.as_view(), name='Water Report Package View'),
    path('WaterReportQuarterExcelDownload/', WaterReportQuarterExcelDownload.as_view(), name='WaterReportQuarterExcelDownload'),



    path('wastetreatmentpackage/<str:packages>',
         WasteTreatmentsPackageView.as_view(), name='Water Report Package View'),
    path('wasteTreatmentReportPackageExcelDownload/', wasteTreatmentReportPackageExcelDownload.as_view(), name='wasteTreatmentReportPackageExcelDownload'),



    path('wastetreatmentquarter/<str:quarter>/<int:year>',
         WasteTreatmentsQuarterView.as_view(), name='Water Report Quarter View'),
    path('wasteTreatmentQuarterExcelDownload/', wasteTreatmentQuarterExcelDownload.as_view(), name='wasteTreatmentQuarterExcelDownload'),



    path('materialmanagementpackage/<str:packages>',MaterialManagementReporetpackageView.as_view(), name='Material Management Package'),

    path('MaterialManegmanetReportPackageExcelDownload/', MaterialManegmanetReportPackageExcelDownload.as_view(), name='MaterialManegmanetReportPackageExcelDownload'),


    path('materialmanagementquarter/<str:quarter>/<int:year>',
         MaterialManagementReporetQuarterView.as_view(), name='Material Management Quarter'),
    path('materialManagementQuarterExcelDownload/', materialManagementQuarterExcelDownload.as_view(), name='materialManagementQuarterExcelDownload'),





     path('TreeMangementReportPackage/<str:packages>',
         TreeMangementReportPackage.as_view(), name='Tree Management Package'),
     path('TreeManagementReportQuarterView/', TreeManagementReportQuarterView.as_view(), name='TreeManagementReportQuarterView'),



     path('TreeManagementReportQuarterView/<str:quarter>/<int:year>',
         TreeManagementReportQuarterView.as_view(), name='Tree Management Quarter'),
     path('TreeManagementQuarterExcelDownload/', TreeManagementQuarterExcelDownload.as_view(), name='TreeManagementQuarterExcelDownload'),


     path('TrainnigReporQuarter/<str:quarter>/<int:year>' , TrainnigReportQuarterView.as_view() , name = ' TrainningManagementQuarterExcelDownload'),
     path('TrainningManagementQuarterExcelDownload/', TrainningManagementQuarterExcelDownload.as_view(), name='TrainningManagementQuarterExcelDownload'),
 

     path('TrainnigReporpackage/<str:packages>' , TrainnigReportPackageView.as_view() , name = ' PreConstructionStageCompliance'),
     path('TrainnigReportPackageExcelDownload/', TrainnigReportPackageExcelDownload.as_view(), name='TrainnigReportPackageExcelDownload'),



    
     path('OccupationalHealthQuarter/<str:quarter>/<int:year>' , OccupationalHealthQuarterView.as_view() , name = ' PreConstructionStageCompliance'),
     path('OccupationalHealthQuarterExcelDownload/', OccupationalHealthQuarterExcelDownload.as_view(), name='OccupationalHealthQuarterExcelDownload'),


     path('OccupationalHealthPackage/<str:packages>' , OccupationalHealthPackageView.as_view() , name = ' PreConstructionStageCompliance'),
     path('ExcelOccupationalHealthQuarterExcelDownload/', ExcelOccupationalHealthQuarterExcelDownload.as_view(), name='ExcelOccupationalHealthQuarterExcelDownload'),


     path('excel' , ExcelWorkbook.as_view() , name = 'sample excel'),
     
     
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
