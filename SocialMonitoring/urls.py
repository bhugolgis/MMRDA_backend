from django.urls import path
from .views import *


# Use snake case for all new api created for endpoints and name attribute for better readability and standard practice
urlpatterns = [
    path ('Postlabourcampdetails' , PostlabourCampdetails.as_view() , name = "labourCampdetails "),
    path('labourCampdetailsView' , labourCampdetailsView.as_view() , name = "labourCampdetailsView"),
    path('labourCampdetailsViewSearch' , labourCampdetailsViewSearch.as_view() , name = "labourCampdetailsView"),
 
    path ('pap' , PapView.as_view() , name = "project affected Person "),
    path ('pap/<int:id>' , PapGetUpdateDeleteView.as_view() , name = "get-update-delete-pap "),
    path ('paplist' , PapListView.as_view() , name = "project affected Person List "),

    # Rehab spelling is inconsistent (rehabilitation)
    path('rehabitationpapid/<str:PAPID>' , RehabilatedPAPIDView.as_view() , name = "rehabitationPapID"),
    path('rehabilitation' , RehabilitationView.as_view() , name = "rehabitation"),
    path('rehabilitation/<int:id>', RehabilitationGetUpdateDeleteView.as_view(), name='get-update-delete-rehabilitation'),
        
    path ('constructionsite' , constructionSiteView.as_view() , name = "constructionSiteView"),
    path ('construction-site/<int:id>', ConstructionSiteGetUpdateDeleteView.as_view() , name = "get-update-delete-construction-site"),
    path ('constructionsiteList' , ConstructionSiteListView.as_view() , name = "ConstructionSiteListView"),

    path ('labourcamp' , LabourCampView.as_view() , name = "LabourCampDetailsView"),
    path('labour-camp/<int:id>', LabourCampUpdateGetDeleteView.as_view() , name =  "get-update-delete-labour-camp"),
]