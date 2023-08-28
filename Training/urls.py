from django.urls import path
from .views import *

urlpatterns = [
    path('traning' , TraningView.as_view() , name = 'traning'),
    path('traningList' , TrainingListView.as_view() , name = 'traning list'),
    path('traningUpdate/<int:pk>' , TrainingupdateView.as_view() , name = 'traning update'),

    
    path('photographs' , PhotographsView.as_view() , name = 'photographs') ,
    path('photographsList' , photographsListView.as_view() , name = 'photographs list '),
    path('PhotographsViewupdate/<int:pk>' , updatephotographview.as_view() , name = 'photograph update'),

    path('occupational' , occupationalHealthSafety.as_view() , name = 'occupational Health & Safety') ,
    path('contactus' , ContactUsView.as_view() , name = 'occupational update'),
    path('contactussearch' , ContactusListView.as_view() , name = 'occupational update'),
    
    path('PreConstructionStageCompliance' , PreConstructionStageComplianceView.as_view() , name = ' PreConstructionStageCompliance'),
    path('ConstructionStageComplaince' , ConstructionStageComplainceView.as_view() , name = ' PreConstructionStageCompliance'),
   
    
    # path(' ContactUsimagesCompress' , ContactUsimagesCompress.as_view() , name = ' PreConstructionStageCompliance'),

]