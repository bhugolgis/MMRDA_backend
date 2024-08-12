from django.urls import path
from .views import *

urlpatterns = [
    path('traning' , TraningView.as_view() , name = 'traning'),
    path('traning<int:id>' , TraningView.as_view() , name = 'get-traning'),
    path('traningList' , TrainingListView.as_view() , name = 'traning list'),
    path('traning/<int:id>' , TrainingUpdateView.as_view() , name = 'traningUpdate'),
    
    path('photographs' , PhotographsView.as_view() , name = 'photographs') ,
    path('photographsList' , photographsListView.as_view() , name = 'photographs list '),
    # path('PhotographsViewupdate/<int:pk>' , updatephotographview.as_view() , name = 'photograph update'),

    path('occupational' , occupationalHealthSafetyView.as_view() , name = 'occupational Health & Safety') ,
    path('occupational/<int:id>' , occupationalHealthSafetyView.as_view() , name = 'get-occupational-health-and-safety') ,
    path('occupational/<int:id>' , OccupationalHealthSafetyUpdateView.as_view() , name = 'ohs-update') ,
    path('contactus' , ContactUsView.as_view() , name = 'occupational update'),
    path('contactussearch' , ContactusListView.as_view() , name = 'occupational update'),
    
    path('PreConstructionStageCompliance' , PreConstructionStageComplianceView.as_view() , name = ' PreConstructionStageCompliance'),
    path('pre-construction-stage-compliance/<int:id>' , PreConstructionStageComplianceView.as_view() , name = 'get-pre-construction-stage-compliance'),
    path('PreConstructionStageCompliance/<int:id>' , PreConstructionStageComplianceUpdateView.as_view() , name = ' PreConstructionStageUpdateCompliance'),
    path('ConstructionStageComplaince' , ConstructionStageComplainceView.as_view() , name = ' ConstructionStageCompliance'),
    path('ConstructionStageComplaince/<int:id>' , ConstructionStageComplianceUpdateView.as_view() , name = ' ConstructionStageCompliance'),
   
    
    # path(' ContactUsimagesCompress' , ContactUsimagesCompress.as_view() , name = ' PreConstructionStageCompliance'),

]