from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import *
from SocialMonitoring.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Count
from Training.models import *
from .models import *
from EnvMonitoring.models import ExistingTreeManagment
import math
from Report.serializers import LabourcampReportSerializer
# Create your views here.

class MetroLine4View(generics.GenericAPIView):
    serializer_class = MetroLine4AlignmentSerializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            MetroLine = MmrdaNew.objects.all()
            serializers = self.get_serializer(MetroLine , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)


class MetroLine4And4AView(generics.GenericAPIView):
    serializer_class = MetroLine4AlignmentSerializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            MetroLine = MmrdaAlignment4326.objects.all()
            serializers = self.get_serializer(MetroLine , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)

            
class Package54AlignmentView(generics.GenericAPIView):
    serializer_class = Package54AlignmentSerializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            package_ca_54 = MmrdaCa54Alignment4326.objects.all()
            serializers = Package54AlignmentSerializer(package_ca_54 , many = True).data
            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
        

class package12AlignmentView(generics.GenericAPIView):    
    # serializer_class = Package12AlignmentSerializer 
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
            
            package_ca_12 = MmrdaCa12Alignment4326.objects.all()
            serializers = Package12AlignmentSerializer(package_ca_12 , many = True).data
            # serializers = self.get_serializer(package_ca_12 , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializers},
                            status= 200)
        
class package11AlignmentView(generics.GenericAPIView):
    serializer_class = Package11AlignmentSerializer 
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
    
            package_ca_11 = MmrdaCa11Alignment4326.objects.all()
            serializer = Package11AlignmentSerializer(package_ca_11 , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer},
                             status= 200)
      
class package10AlignmentView(generics.GenericAPIView):
    serializer_class = Package10AlignmentSerializer
    #permission_classes = [IsAuthenticated]
    def get(self , request):

            package_ca_10 = MmrdaCa10Alignment4326.objects.all()
            serializer = Package10AlignmentSerializer(package_ca_10 , many = True).data
    
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer})
       
class package09AlignmentView(generics.GenericAPIView):
    serializer_class = Package09AlignmentSerializer  
    #permission_classes = [IsAuthenticated]
    def get(self , request):
      
            package_ca_09 = MmrdaCa09Alignment4326.objects.all()
            serializer = Package09AlignmentSerializer(package_ca_09 , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer},
                             status= 200)
      
class package08AlignmentView(generics.GenericAPIView):
    serializer_class = Package08AlignmentSerializer  
    #permission_classes = [IsAuthenticated]
    def get(self , request):
        
            package_ca_08 = MmrdaCa08Alignment4326.objects.all()
            serializer = Package08AlignmentSerializer(package_ca_08 , many = True)
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer.data},
                             status= 200)

class Start_end_points(generics.GenericAPIView):
    serializer_class = Start_end_points_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            Start_end_points = StartEndPoints.objects.all()
            serializers = self.get_serializer(Start_end_points , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)


class All_start_end_points(generics.GenericAPIView):
    serializer_class = All_start_end_point_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            All_StartEndPoint = AllStartEndPoints.objects.all()
            serializers = self.get_serializer(All_StartEndPoint , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)




class Package08_start_end_points(generics.GenericAPIView):
    serializer_class = Package08_start_end_point_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa08_StartEndPoint = PackageCa08StartEndPoint.objects.all()
            serializers = self.get_serializer(PackageCa08_StartEndPoint , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)

class Package09_start_end_points(generics.GenericAPIView):
    serializer_class = Package09_start_end_point_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa09_StartEndPoint = PackageCa09StartEndPoint.objects.all()
            serializers = self.get_serializer(PackageCa09_StartEndPoint , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)


class Package10_start_end_points(generics.GenericAPIView):
    serializer_class = Package10_start_end_point_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa10_StartEndPoint = PackageCa10StartEndPoint.objects.all()
            serializers = self.get_serializer(PackageCa10_StartEndPoint , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
    

class Package11_start_end_points(generics.GenericAPIView):
    serializer_class = Package11_start_end_point_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa11_StartEndPoint = PackageCa11StartEndPoint.objects.all()
            serializers = self.get_serializer(PackageCa11_StartEndPoint , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)



class Package12_start_end_points(generics.GenericAPIView):
    serializer_class = Package12_start_end_point_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa12_StartEndPoint = PackageCa12StartEndPoint.objects.all()
            serializers = self.get_serializer(PackageCa12_StartEndPoint , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)


class Package54_start_end_points(generics.GenericAPIView):
    serializer_class = Package54_start_end_point_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa54_StartEndPoint = PackageCa54StartEndPoint.objects.all()
            serializers = self.get_serializer(PackageCa54_StartEndPoint , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
    
class PackageCa08_metroStations(generics.GenericAPIView):
    serializer_class = PackageCa08_metroStations_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa08_metroStations = PackageCa08MetroStations.objects.all()
            serializers = self.get_serializer(PackageCa08_metroStations , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
    


class PackageCa09_metroStations(generics.GenericAPIView):
    serializer_class = PackageCa09_metroStations_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa09_metroStations = PackageCa09MetroStations.objects.all()
            serializers = self.get_serializer(PackageCa09_metroStations , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)



class PackageCa10_metroStations(generics.GenericAPIView):
    serializer_class = PackageCa10_metroStations_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa10_metroStations = PackageCa10MetroStations.objects.all()
            serializers = self.get_serializer(PackageCa10_metroStations , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)


class PackageCa11_metroStations(generics.GenericAPIView):
    serializer_class = PackageCa11_metroStations_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa11_metroStations = PackageCa11MetroStations.objects.all()
            serializers = self.get_serializer(PackageCa11_metroStations , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
    
class PackageCa12_metroStations(generics.GenericAPIView):
    serializer_class = PackageCa12_metroStations_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa12_metroStations = PackageCa12MetroStations.objects.all()
            serializers = self.get_serializer(PackageCa12_metroStations , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
    

class PackageCa54_metroStations(generics.GenericAPIView):
    serializer_class = PackageCa54_metroStations_Serializer
    #permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
       
            PackageCa54_metroStations = PackageCa54MetroStations.objects.all()
            serializers = self.get_serializer(PackageCa54_metroStations, many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
    
    
class GISPortalExistingTreeManagmentView(generics.GenericAPIView):
    serializer_class = GISPortalExistingTreeManagmentSerailizer
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            existing_tree_management = ExistingTreeManagment.objects.all()
            if not existing_tree_management.exists():
                return Response({'status': 'error',
                                 'message': 'No data found'},
                                 status=404)
            
            serializer = self.get_serializer(existing_tree_management, many=True)
            return Response({'status': 'success',
                             'message': 'Data was successfully fetched',
                             'data': serializer.data},
                             status=200)
        except Exception as e:
            return Response({'status': 'error',
                             'message': f'An error occurred: {str(e)}'},
                             status=500)


class projectAffectedPersonsView(generics.GenericAPIView):
    serializer_class = projectAffectedPersonsSerializer  
    #permission_classes = [IsAuthenticated]
    def get(self , request):
        
            Affected_data = Projectaffectedperson.objects.all()
            serializer = self.get_serializer(Affected_data , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer},
                             status= 200)
        

class MetroStationView(generics.GenericAPIView):
    serializer_class = MetroStationSerializer   
    #permission_classes = [IsAuthenticated]
    def get(self , request):
        try:
            metroStation = Station.objects.all()
            serializer = MetroStationSerializer(metroStation , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer},
                             status= 200)
        except :
            return Response({'status' : 'failed',
                            'message' : 'Something went wrong !! Please try again'}, status = 400)
 
class ProjectAffectedTreesView(generics.GenericAPIView):
    serializer_class = ProjectAffectedTreesSerializer
    #permission_classes = [IsAuthenticated]
    def get(self , request):
        try:
            AffectedTrees = ProjectAffectedTrees.objects.all()
            serializer = ProjectAffectedTreesSerializer(AffectedTrees , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data' : serializer},status= 200)
        except :
            return Response({'status' : 'failed',
                            'message' : 'Something went wrong !! Please try again'}, status = 400)
        

class PAPTypeOfStructureView(ListAPIView):

    serializer_class = PAPGISSerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated]
    def get(self, request, categoryOfPap, *args, **kwargs):
       
        data = PAP.objects.filter(categoryOfPap=categoryOfPap).order_by('-id')
        if not data.exists():
            return Response({'Message': 'No data found',
                                'status' : 'Failed'},  status=status.HTTP_200_OK)
        papdata = self.get_serializer(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                        'status' : 'success' , 
                        "PAP": papdata},
                        status=status.HTTP_200_OK)
        

class RehabilitationTypeOfStructureView(ListAPIView):
    serializer_class = RehabilitationGISSerializer
    parser_classes = [MultiPartParser]
    #permission_classes = [IsAuthenticated]

    def get(self, request, compensationStatus , *args, **kwargs):

        data = Rehabilitation.objects.filter(compensationStatus=compensationStatus).order_by('-id')
        if not data.exists():
            return Response({'Message': 'No data found',
                                'status' : 'success'},  status=status.HTTP_200_OK)
        Rehabilitationdata = self.get_serializer( data, many=True).data

        return Response({'Message': 'data Fetched Successfully',
                        'status' : 'success' , 
                        "Rehabilated_PAP_Package": Rehabilitationdata},
                        status=status.HTTP_200_OK)
       
class MaterialManagementStorageGISQuarterView(ListAPIView):
    serializer_class = materialManagementStorageGISSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, condition,  *args, **kwargs):
        try:
            data = MaterialManegmanet.objects.filter(
                materialStorageCondition=condition).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Material_data = self.get_serializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "material Management data": Material_data},
                            status=200)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)
        

class MaterialManagementSourceGISQuarterView(ListAPIView):

    serializer_class = materialManagementSourceGISSerializer
    parser_classes = [MultiPartParser]

    def get(self, request,  *args, **kwargs):
        try:
            # data = MaterialManegmanet.objects.filter(
            #     materialStorageCondition=condition).order_by('-id')
            data = MaterialManegmanet.objects.all()
            if len(data) == 0 :
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Material_data = self.get_serializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "material Management data": Material_data},
                            status=200)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)
        

class IncidentTypeGISQuarterView(ListAPIView):
    serializer_class = IncidentTypeGISQuarterSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, typeOfIncident, quarter , *args, **kwargs):
        try:
            data = occupationalHealthSafety.objects.filter(
                typeOfIncident=typeOfIncident , quarter = quarter ).order_by('-id')
            # data = occupationalHealthSafety.objects.all()
            if len(data) == 0 :
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK )

            incident_data = self.get_serializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "data": incident_data},
                            status=200)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)
        

class occupationalHealthSafetyGISView(APIView):
    
    def get(self, request, quarter , year , package, *args , **kwargs):
        quarter_waise_data= occupationalHealthSafety.objects.filter(packages = package , quarter = quarter , dateOfMonitoring__year = year ).latest('id')
        
        serializer1 = occupationalHealthSafetyGISConditionSerializer(quarter_waise_data).data
        values = list(serializer1.values())
        dataset = []
        dataset.append(((values.count('Complied')) / 13) * 100 ) ,
        dataset.append(((values.count('Not-Complied')) / 13 ) * 100) 
      
        for i in dataset:
             for j in (range(1 , len(dataset))):
                if i > j :
                    condition = 'Complied'
                else:
                    condition = 'Not-complied'
                    
        serializer2 =occupationalHealthSafetyGISSerializer(quarter_waise_data).data
        return Response({'status': 'success',
                        'Message': 'Data Fetched successfully',
                        'condition' : condition , 
                        'data' : serializer2
                        })







# The `LabourcampReportPackageView` class is a view in a Django REST framework that retrieves previous
# and latest data for a given package and labour camp name.
class LabourcampReportPackageView(ListAPIView):
    serializer_class = LabourcampReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, labourCampName ,*args, **kwargs):
        """
        This function retrieves the previous and latest data for a given package and labour camp name.

        """
        try:
            previous = LabourCamp.objects.filter(packages=packages, labourCampName=labourCampName ).order_by('-id')[1:]
           
            latest = LabourCamp.objects.filter(packages=packages, labourCampName=labourCampName).latest('id')
            # latest_serializer = LabourcampReportSerializer(latest).data
           
            previousData = self.serializer_class(previous, many=True)
            latestData = self.serializer_class(latest)

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            'Previous': previousData.data,
                             'latest': latestData.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'Message': 'There is no data available for this Package or Quarter',
                            'status' : 'Failed'}, status=status.HTTP_400_BAD_REQUEST) 