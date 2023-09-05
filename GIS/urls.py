from django.urls import path , re_path
from .views import *

urlpatterns = [
     
     path('MetroLine4Aligment' , MetroLine4View.as_view() , name = 'MetroLine4'),
     path('package54Aligment' , Package54AlignmentView.as_view() , name = 'Package54AlignmentView'),
     path('package12Aligment' , package12AlignmentView.as_view() , name = 'package12Aligment'),
     path('package11Aligment' , package11AlignmentView.as_view() , name = 'package11Aligment'),
     path('package10Aligment' , package10AlignmentView.as_view() , name = 'package10Aligment'),
     path('package09Aligment' , package09AlignmentView.as_view() , name = 'package09Aligment'),
     path('package08Aligment' , package08AlignmentView.as_view() , name = 'package08Aligment'),
     path('MetroStation' , MetroStationView.as_view() , name = 'MetroStationView '),
     path('projectAffectedPersons' , projectAffectedPersonsView.as_view() , name = 'projectAffectedPersons '),
     path('RehabilitatedPap' , RehabilitatedPapView.as_view() , name = 'RehabilitatedPap'),
     path('ProjectAffectedTrees' , ProjectAffectedTreesView.as_view() , name = 'MetroStationView '),
     re_path(r'PAP-Type-Of-Structure/(?P<categoryOfPap>.+)$' , PAPTypeOfStructureView.as_view() , name = 'MetroStationView '),
     re_path(r'Rehabilitation-compensation-status/(?P<compensationStatus>.+)$' , RehabilitationTypeOfStructureView.as_view() , name = 'MetroStationView '),
     path('MaterialManagementStorageGISQuarterView/<str:condition>',MaterialManagementStorageGISQuarterView.as_view(), name='Material Management Package'),
     path('MaterialManagementSourceGISQuarterView',MaterialManagementSourceGISQuarterView.as_view(), name='Material Management Package'),
     path('IncidentTypeGISQuarterView/<str:typeOfIncident>/<str:quarter>',IncidentTypeGISQuarterView.as_view(), name='Material Management Package'),
     path('occupationalHealthSafetyGISView/<int:year>/<str:quarter>/<str:package>',occupationalHealthSafetyGISView.as_view(), name='Material Management Package'),
              
]
