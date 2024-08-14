from django.urls import path
from .views import *


# Use snake case for all new api created for endpoints and name attribute for better readability and standard practice
urlpatterns = [
    path ('Postlabourcampdetails' , PostlabourCampdetails.as_view() , name = "labourCampdetails "),
    path('labourCampdetailsView' , labourCampdetailsView.as_view() , name = "labourCampdetailsView"),
    path('labourCampdetailsViewSearch' , labourCampdetailsViewSearch.as_view() , name = "labourCampdetailsView"),
 
    path ('pap' , PapView.as_view() , name = "project affected Person "),
    path ('pap/<int:id>' , PapUpdateView.as_view() , name = "get-pap "),
    path ('pap/<int:id>' , PapUpdateView.as_view() , name = "update-pap"),
    path ('pap/<int:id>/rud' , PapRetrieveDestroyView.as_view() , name = "retrieve-destroy-pap"),
    path ('paplist' , PapListView.as_view() , name = "project affected Person List "),

    # Rehab spelling is inconsistent (rehabilitation)
    path('rehabitationpapid/<str:PAPID>' , RehabilatedPAPIDView.as_view() , name = "rehabitationPapID"),
    path('rehabilitation' , RehabilitationView.as_view() , name = "rehabitation"),
    path('rehabilitation/<int:id>', RehabilitationView.as_view(), name='get-rehabilitation'),
    path('rehabilitation/<int:id>', RehabilitationUpdateView.as_view(), name='update-rehabilitation'),
        
    path ('constructionsite' , constructionSiteView.as_view() , name = "constructionSiteView"),
    path ('construction-site/<int:id>', constructionSiteView.as_view() , name = "get-construction-site"),
    path ('construction-site/<int:id>', ConstructionSiteUpdateView.as_view() , name = "update-construction-site"),
    path ('constructionsiteList' , ConstructionSiteListView.as_view() , name = "ConstructionSiteListView"),

    path ('labourcamp' , LabourCampView.as_view() , name = "LabourCampDetailsView"),
    path('labour-camp/<int:id>', LabourCampUpdateView.as_view() , name =  "get-labour-camp"),
    path('labour-camp/<int:id>', LabourCampUpdateView.as_view() , name =  "update-labour-camp"),
]