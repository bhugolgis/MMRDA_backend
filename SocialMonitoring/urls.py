from django.urls import path
from .views import *

# PAP stands for Project Affected Person
# Use snake case for all new api created for endpoints and name attribute for better readability and standard practice
urlpatterns = [
    path ('Postlabourcampdetails' , PostlabourCampdetails.as_view() , name = "labour-camp-details "),
    path('labourCampdetailsView' , labourCampdetailsView.as_view() , name = "labour-camp-details-view"),
    path('labourCampdetailsViewSearch' , labourCampdetailsViewSearch.as_view() , name = "labour-camp-details-view"),
 
    path ('pap' , PapView.as_view() , name = "create-pap"),
    path ('pap/<int:id>' , PapGetUpdateDeleteView.as_view() , name = "get-update-delete-pap "),
    path ('paplist' , PapListView.as_view() , name = "project affected Person List "),

    # Rehab spelling is inconsistent (rehabilitation)
    path('rehabitationpapid/<str:PAPID>' , RehabilatedPAPIDView.as_view() , name = "rehabitation-pap-id"),
    path('rehabilitation' , RehabilitationView.as_view() , name = "create-rehabitation"),
    path('rehabilitation/<int:id>', RehabilitationGetUpdateDeleteView.as_view(), name='get-update-delete-rehabilitation'),
        
    path ('constructionsite' , constructionSiteView.as_view() , name = "create-construction-site"),
    path ('construction-site/<int:id>', ConstructionSiteGetUpdateDeleteView.as_view() , name = "get-update-delete-construction-site"),
    path ('constructionsiteList' , ConstructionSiteListView.as_view() , name = "ConstructionSiteListView"),

    path ('labourcamp' , LabourCampView.as_view() , name = "create-labour-camp-details-view"),
    path('labour-camp/<int:id>', LabourCampUpdateGetDeleteView.as_view() , name =  "get-update-delete-labour-camp"),
]