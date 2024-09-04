from django.urls import path,include
from .views import *
# from .views import LabourcampReportExcelViewDetailList
from rest_framework import routers

urlpatterns = [
     
    # Social Monitoring

    path('papreportpackage/<str:packages>',PAPReportPackageView.as_view(), name='PAP Report package'),
    path('PAPReportPackageExcelDownload/', PAPReportPackageExcelDownload.as_view(), name='PAPReportPackageExcelDownload'),       
    path('papreportquarter/<str:quarter>/<int:year>',PAPReportQuarterView.as_view(), name='PAP Report quarter'),
    path('PAPReportExcelQuaterExcelDownload/', PAPReportExcelQuaterExcelDownload.as_view(), name='PAPReportExcelQuaterExcelDownload'),

    path('Rehabilationreportpackage/<str:packages>',RehabilitationReportPackageView.as_view(), name=' Rehabilitation Report package'),
    path('RehabilitationReportPackageExcelDownload/', RehabilitationReportPackageExcelDownload.as_view(), name='RehabilitationReportPackageExcelDownload'),       
    path('Rehabilationreportquarter/<str:quarter>/<int:year>',RehabilitationReportQuarterView.as_view(), name=' Rehabilitation Report quarter'),
    path('RehabilitationReportQuarterExcelDownload/', RehabilitationReportQuarterExcelDownload.as_view(), name='RehabilitationReportQuarterExcelDownload'),
    
    # Env Monitoring

    path('airReportpackage/<str:packages>',AirReportPackageView.as_view(), name='AirReport Package View'),
    path('AirReportReportPackageExcelDownload/', AirReportReportPackageExcelDownload.as_view(), name='AirReportReportPackageExcelDownload'),        
    path('airReportquarter/<str:month>/<int:year>',AirReportQuarterView.as_view(), name='AirReport Package View'),
    path('AirReportQuarterExcelDownload/', AirReportQuarterExcelDownload.as_view(), name='AirReportQuarterExcelDownload'),
    
    path('waterReportpackage/<str:packages>',     waterReportPackageView.as_view(), name='Water Report Package View'),
    path('waterReportReportPackageExcelDownload/', waterReportReportPackageExcelDownload.as_view(), name='waterReportReportPackageExcelDownload'),
    path('waterReportquarter/<str:month>/<int:year>',waterReportQuarterView.as_view(), name='Water Report Package View'),
    path('WaterReportQuarterExcelDownload/', WaterReportQuarterExcelDownload.as_view(), name='WaterReportQuarterExcelDownload'),
    
    path('noisereportpackage/<str:packages>',NoiseReportpackageView.as_view(), name='Noisereport Package View'),
    path('NoiseReportReportPackageExcelDownload/', NoiseReportReportPackageExcelDownload.as_view(), name='NoiseReportReportPackageExcelDownload'),
    path('noisereportquarter/<str:month>/<int:year>',NoiseReportQuarterView.as_view(), name='Noisereport Package View'),
    path('NoiseReportQuarterExcelDownload/', NoiseReportQuarterExcelDownload.as_view(), name='NoiseReportQuarterExcelDownload'),

    path('TreeMangementReportPackage/<str:packages>',TreeMangementReportPackage.as_view(), name='get-existing-tree-report-package'),
    path('TreeManagementReportQuarterView/<str:quarter>/<int:year>',TreeManagementReportQuarterView.as_view(), name='get-existing-tree-report-quarter'),
    path('TreeManagementReportPackageExcelDownload/', treeManagementReportPackageExcelDownload.as_view(), name='get-existing-tree-report-package-excel-download'),
    path('TreeManagementQuarterExcelDownload/', TreeManagementQuarterExcelDownload.as_view(), name='get-existing-tree-report-quarter-excel-download'),

    path('new-tree-report-package/<str:packages>',NewTreeReportPackage.as_view(), name='get-new-tree-report-package'),
    path('new-tree-report-quarter/<str:quarter>/<int:year>',NewTreeReportQuarterView.as_view(), name='get-new-tree-report-package'),
    
    path('wastetreatmentpackage/<str:packages>',WasteTreatmentsPackageView.as_view(), name='Water Report Package View'),
    path('wastetreatmentquarter/<str:quarter>/<int:year>',WasteTreatmentsQuarterView.as_view(), name='Water Report Quarter View'),
    path('wasteTreatmentReportPackageExcelDownload/', wasteTreatmentReportPackageExcelDownload.as_view(), name='wasteTreatmentReportPackageExcelDownload'),
    path('wasteTreatmentQuarterExcelDownload/', wasteTreatmentQuarterExcelDownload.as_view(), name='wasteTreatmentQuarterExcelDownload'),

    path('materialmanagementpackage/<str:packages>',MaterialManagementReporetpackageView.as_view(), name='Material Management Package'),
    path('MaterialManegmanetReportPackageExcelDownload/', MaterialManegmanetReportPackageExcelDownload.as_view(), name='MaterialManegmanetReportPackageExcelDownload'),
    path('materialmanagementquarter/<str:quarter>/<int:year>',MaterialManagementReporetQuarterView.as_view(), name='Material Management Quarter'),
    path('materialManagementQuarterExcelDownload/', materialManagementQuarterExcelDownload.as_view(), name='materialManagementQuarterExcelDownload'),
    
    # OHS

    path('OccupationalHealthPackage/<str:packages>' , OccupationalHealthPackageView.as_view() , name = ' get-occupational-wellness-package'),
    path('OccupationalHealthQuarter/<str:quarter>/<int:year>' , OccupationalHealthQuarterView.as_view() , name = ' get-occupational-wellness-quarter'),
    path('OccupationalHealthPackageExcelDownload/', OccupationalWellnessPackageExcelDownload.as_view(), name='occupational-wellness-package-excel-download'),
    path('OccupationalHealthQuarterExcelDownload/', OccupationalWellnessQuarterExcelDownload.as_view(), name='occupational-wellness-quarter-excel-download'),

    path('labourcampreportpackageExcelDownloadView/', labourcampreportpackageExcelDownloadView.as_view(), name='labourcampreportpackageExcel'),
    path('labourcampreportpackage/<str:packages>/<str:labourCampName>',LabourcampReportPackageView.as_view(), name='Labourcamp Report View package'),
    path('labourcampreportquarter/<str:quarter>/<int:year>/<str:labourCampName>',LabourCampReportQuarterView.as_view(), name='Labourcamp Report View quarter'),
    path('labourQuarterExcelDownload/', labourQuarterExcelDownload.as_view(), name='labourQuarterExcelDownload'),

    path('constructioncampreportPackage/<str:packages>/<str:constructionSiteName>',ConstructionCampReportPackageView.as_view(), name='ConstructionSite Report'),
    path('ConstructionCampReportPackageExcelDownload/', ConstructionCampReportPackageExcelDownload.as_view(), name='labourQuarterExcelDownload'),        
    path('constructioncampreportQuarter/<int:year>/<str:quarter>/<str:constructionSiteName>',ConstructionCampReportQuarterView.as_view(), name='ConstructionSite Report'),
    path('ConstructionCampReportQuaterExcelDownload/', ConstructionCampReportQuaterExcelDownload.as_view(), name='ConstructionCampReportQuaterExcelDownload'),

    # Training

    path('TrainnigReporpackage/<str:packages>' , TrainnigReportPackageView.as_view() , name = ' get-training-report-package'),
    path('TrainnigReporQuarter/<str:quarter>/<int:year>' , TrainnigReportQuarterView.as_view() , name = ' get-training-report-quarter'),
    path('TrainnigReportPackageExcelDownload/', TrainnigReportPackageExcelDownload.as_view(), name='get-trainig-report-package-excel-download'),
    path('TrainningManagementQuarterExcelDownload/', TrainningManagementQuarterExcelDownload.as_view(), name='get-trainig-report-quarter-excel-download'),

    path('excel' , ExcelWorkbook.as_view() , name = 'sample excel'),
]
