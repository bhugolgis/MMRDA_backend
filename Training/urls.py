from django.urls import path
from .views import *

urlpatterns = [
    path('traning' , TraningView.as_view() , name = 'traning'),
    path('traning/<int:id>' , TrainingGetUpdateDeleteView.as_view() , name = 'get-update-delete-traning'),
    
    path('traningList' , TrainingListView.as_view() , name = 'traning-list'),
    
    path('photographs' , PhotographsView.as_view() , name = 'photographs') ,
    path('photographsList' , photographsListView.as_view() , name = 'photographs list '),
    # path('PhotographsViewupdate/<int:pk>' , updatephotographview.as_view() , name = 'photograph update'),

    path('occupational' , occupationalHealthSafetyView.as_view() , name = 'occupational Health & Safety') ,
    path('occupational/<int:id>' , OccupationalWellnessGetUpdateDeleteView.as_view() , name = 'get-update-delete-occupational-wellness') ,
    path('contactus' , ContactUsView.as_view() , name = 'occupational update'),
    path('contactussearch' , ContactusListView.as_view() , name = 'occupational update'),
    
    path('PreConstructionStageCompliance' , PreConstructionStageComplianceView.as_view() , name = ' PreConstructionStageCompliance'),
    path('pre-construction-stage-compliance/<int:id>' , PreConstructionStageComplianceGetUpdateDeleteView.as_view() , name = 'get-update-delete-pre-construction-stage'),
    path('ConstructionStageComplaince' , ConstructionStageComplainceView.as_view() , name = ' ConstructionStageCompliance'),
    path('ConstructionStageComplaince/<int:id>' , ConstructionStageComplianceGetUpdateDeleteView.as_view() , name = ' get-update-delete-construction-stage'),
   
    
    # path(' ContactUsimagesCompress' , ContactUsimagesCompress.as_view() , name = ' PreConstructionStageCompliance'),

]