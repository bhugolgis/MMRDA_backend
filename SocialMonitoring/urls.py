from django.urls import path
from .views import *

urlpatterns = [

    
    # path ('test' , testAPiView.as_view() , name = "testAPiView "),
    path ('Postlabourcampdetails' , PostlabourCampdetails.as_view() , name = "labourCampdetails "),
    path('labourCampdetailsView' , labourCampdetailsView.as_view() , name = "labourCampdetailsView"),
    path('labourCampdetailsViewSearch' , labourCampdetailsViewSearch.as_view() , name = "labourCampdetailsView"),
 
    path ('pap' , PapView.as_view() , name = "project affected Person "),
    path ('pap/<int:id>' , papupdateView.as_view() , name = "project affected Person "),
    path ('paplist' , PapListView.as_view() , name = "project affected Person List "),

    path('rehabitation' , RehabilitationView.as_view() , name = "rehabitation"),
    path('rehabitationpapid/<str:PAPID>' , RehabilatedPAPIDView.as_view() , name = "rehabitation"),
    path ('rehabitation/<int:id>' , RehabilitationUpdateView.as_view() , name = "rehabitationUpdate"),
       
    

    path ('constructionsite' , constructionSiteView.as_view() , name = "constructionSiteView"),
    path ('constructionsite<int:id>', ConstructionSiteUpdateView.as_view() , name = "constructionSiteUpdateView"),
    path ('constructionsiteList' , ConstructionSiteListView.as_view() , name = "ConstructionSiteListView"),

    path ('labourcamp' , LabourCampDetailsView.as_view() , name = "LabourCampDetailsView"),
    path('labourcamp/<int:id>', labourCampUpdateView.as_view() , name =  "LabourCampDetailsView"),


]