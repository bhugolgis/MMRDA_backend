from rest_framework import generics
from .serialzers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.response import Response
from django.contrib.gis.geos import Point 
from .models import *
# from .models import traning, photographs
from .permission import IsConsultant, IsContractor
from rest_framework import filters
from rest_framework import status
from MMRDA.utils import error_simplifier
from .utils import save_multiple_files


# Create your views here.

# The below class is a view for handling the creation of training data with file uploads in a Django
# RThe post() method of the TraningView class first validates the data submitted by the user. 
# If the data is valid, the method then creates a new Point object from the latitude and longitude values submitted by the user.
#  It then saves the record to the database and returns a success message. Otherwise, the view returns an error message.

class TraningView(generics.GenericAPIView):
    serializer_class = TraningSerializer
    permission_classes = [IsAuthenticated]
    #parser_classes = [MultiPartParser]

    def post(self, request):
        """
        The above function is a POST request handler that saves data and files to the database.
        
        """
        
        serializer = TraningSerializer(data=request.data)
        if serializer.is_valid():
            lat = float(serializer.validated_data['latitude'])
            long = float(serializer.validated_data['longitude'])
            location = Point(long, lat, srid=4326)

            file_fields = {
                        'documents': 'traning_photographs',
                        'photographs': 'traning_photographs' ,}

            file_mapping = {}
            for field, file_path in file_fields.items():
                files = request.FILES.getlist(field)
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path , field)

            serializer.save(location = location , user = request.user , **file_mapping) 
            return Response({'status': 'success',
                                        'message' : 'data saved successfully',
                                        }, status= status.HTTP_200_OK)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : error_message} , status = status.HTTP_400_BAD_REQUEST)



# The below code is gives all of the object in a list from Traning table
class TrainingListView(generics.ListAPIView):
    serializer_class = TraningSerializer
    permission_classes = [IsAuthenticated, IsConsultant]
    queryset = traning.objects.all()



# The post() method of the PhotographsView class first validates the data submitted by the user.
# If the data is valid, the method then creates a new Point object from the latitude and longitude values submitted by the user.
#  It then saves the record to the database and returns the record. Otherwise, the view returns an error message.
class PhotographsView(generics.GenericAPIView):
    serializer_class = photographsSerializer
    # permission_classes = [IsAuthenticated, IsConsultant]
    #parser_classes = [MultiPartParser]

    def post(self, request):
        """
        The above function is a POST request handler that saves a photograph object with latitude and
        longitude coordinates and returns the serialized data.
        
        """
        serializer = photographsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            lat = float(serializer.validated_data['latitude'])
            long = float(serializer.validated_data['longitude'])
            location = Point(long, lat, srid=4326)
            phototgraph = serializer.save(location=location , user = request.user)
            
            data = photographsViewSerializer(phototgraph).data
            return Response(data, status=200)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : error_message} , status = status.HTTP_400_BAD_REQUEST)

# The below code is gives all of the object in a list from photograph table
class photographsListView(generics.GenericAPIView):
    serializer_class = photographsViewSerializer
    # permission_classes = [IsAuthenticated, IsConsultant]
    #parser_classes = [MultiPartParser]
    queryset = photographs.objects.all()

    def get(self , request):
        serializer = self.get_serializer(self.get_queryset() , many = True)
        return Response({'message':serializer.data})



# This code defines an API view that allows authenticated users to create new occupational health and safety records.
# The view first validates the data submitted by the user. If the data is valid, the view saves the record to the database and returns a success message.
#  Otherwise, the view returns an error message.
# Check for incident location
class occupationalHealthSafetyView(generics.GenericAPIView):
    serializer_class = occupationalHealthSafetySerialziers
    # parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        The above function is a POST request handler that saves data and files related to occupational
        health and safety incidents.
        
        """
        
        serializer = self.get_serializer(data = request.data )
        if serializer.is_valid():
            lat = float(serializer.validated_data['latitude'])
            long = float(serializer.validated_data['longitude'])
            location = Point(long, lat, srid=4326)
              
              
                    
            file_fields = {
                        'documents': 'OccupationalHealth&Safety',
                        'photographs': 'OccupationalHealth&Safety' ,}

            file_mapping = {}
            for field, file_path in file_fields.items():
                files = request.FILES.getlist(field)
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path , field)

            data = serializer.save(location=location, user = request.user , **file_mapping)
            data = occupationalHealthSafetyViewSerializer(data).data
            return Response({'status' : 'success',
                             'Message' : 'Data Saved Successfully'}, status=200)
        else:
            key, value =list(serializer.errors.items())[0]
            # error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : value[0],
                            'data': data} , status = status.HTTP_400_BAD_REQUEST)


# Update PATCH API
class OccupationalHealthSafetyUpdateView(generics.UpdateAPIView):
    serializer_class = OccupationalHealthSafetyUpdateSerializer
    permission_classes = [IsAuthenticated, IsConsultant | IsContractor]

    def get_object(self):
        """
        Retrieve the occupationalHealthSafety object based on the ID.
        """
        try:
            return occupationalHealthSafety.objects.get(id=self.kwargs['id'])
        except occupationalHealthSafety.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the occupationalHealthSafety instance.
        """
        ohs_instance = self.get_object()
        if not ohs_instance:
            return Response({"message": "Occupational Health and Safety data not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(ohs_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                ohs_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle file fields
        file_fields = {
            'documents': 'OccupationalHealth&Safety',
            'photographs': 'OccupationalHealth&Safety',
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            if files:
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path, field)

        updated_ohs = serializer.save(**file_mapping)
        data = self.get_serializer(updated_ohs).data

        return Response({
            'Message': 'Data updated successfully',
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)


class ContactUsView(generics.GenericAPIView):
    serializer_class = ContactusSerializezr
    # parser_classes = (FormParser,) 
    def post(self, request):
        """
        This function handles a POST request by validating the serializer data, processing file uploads,
        saving the data to the database, and returning a response.
        
        """

        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            lat = float(serializer.validated_data['latitude'])
            long = float(serializer.validated_data['longitude'])
            location = Point(long, lat, srid=4326)
 
            file_fields = {
                    'documents': 'contactus/images',
                    'image': 'contactus/images' ,}
            file_mapping = {}
            for field, file_path in file_fields.items():
               
                # print(file_path , 'file_apth')
                files = request.FILES.getlist(field)
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path , field)
          
          
            contactus = serializer.save(location=location , **file_mapping )
            data = ContactusViewSerialzier(contactus ).data
            return Response(data, status=200)
        else:
            # error = error_simplifier(serializer.errors)
            # print(error)
            # key, value =list(serializer.errors.items())[0]
            # print(key , value)
            # error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : serializer.errors} , status = status.HTTP_400_BAD_REQUEST)
        

class ContactusListView(generics.ListAPIView):
    queryset = Contactus.objects.all()
    serializer_class = ContactusViewSerialzier
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name' , '^email']

# The serializer_class attribute of the PreConstructionStageComplianceView class is set to the PreConstructionStageComplianceSerialzier class. This class is used to serialize and deserialize the data submitted by the user.
# The permission_classes attribute of the PreConstructionStageComplianceView class is set to the IsAuthenticated class. This class ensures that only authenticated users can use the view.
# The post() method of the PreConstructionStageComplianceView class first validates the data submitted by the user.
# If the data is valid, the method then saves the record to the database and returns a success message. Otherwise, the view returns an error message.
class PreConstructionStageComplianceView(generics.GenericAPIView):
    serializer_class = PreConstructionStageComplianceSerialzier
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def post(self , request):
        """
        The above function is a POST request handler that saves data using a serializer and returns a
        success message if the data is valid, or an error message if the data is invalid.
        
        """

        serializer= PreConstructionStageComplianceSerialzier (data = request.data , context={'request': request})
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({'status': 'success' ,
                            'Message': 'Data saved successfully'} , status= 200)
        
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = str(key)+" ,"+ str(value[0])
            return Response({'status': 'error',
                            'Message' : error_message } , status = status.HTTP_400_BAD_REQUEST)
    

# The serializer_class attribute of the ConstructionStageComplainceView class is set to the ConstructionStageComplainceSerializer class. This class is used to serialize and deserialize the data submitted by the user.
# The permission_classes attribute of the ConstructionStageComplainceView class is set to the IsAuthenticated class. This class ensures that only authenticated users can use the view.
# The post() method of the ConstructionStageComplainceView class first validates the data submitted by the user.
# If the data is valid, the method then saves the record to the database and returns a success message. Otherwise, the view returns an error message.
class ConstructionStageComplainceView(generics.CreateAPIView):
    serializer_class = ConstructionStageComplainceSerializer
    permission_classes = [IsAuthenticated]
    #parser_classes = [MultiPartParser]

    def post(self , request):
        """
        The function `post` receives a request, validates the data using a serializer, saves the data if
        valid, and returns a response with a success message or an error message if the data is invalid.
        
        """
        data = request.data
        serializer= ConstructionStageComplainceSerializer(data = data)
        if serializer.is_valid(raise_exception= True):

            file_fields = {
                        'ConsenttToEstablishOoperateDocuments': 'Training\Training_ConsenttToEstablishOoperateDocuments',
                        'PermissionForSandMiningFromRiverbedDocuments': 'Training\Training_PermissionForSandMiningFromRiverbedDocuments',
                        'PermissionForGroundWaterWithdrawalDocuments': 'Training\Training_PermissionForGroundWaterWithdrawalDocuments' ,
                        'AuthorizationForCollectionDisposalManagementDocuments': 'Training\Training_AuthorizationForCollectionDisposalManagementDocuments',
                        'AuthorizationForSolidWasteDocuments': 'Training\Training_AuthorizationForSolidWasteDocuments',
                        'DisposalOfBituminousAndOtherWasteDocuments': 'Training\Training_DisposalOfBituminousAndOtherWasteDocuments',
                        'ConsentToDisposalOfsewagefromLabourCampsDocuments': 'Training\Training_ConsentToDisposalOfsewagefromLabourCampsDocuments' ,
                        'PollutionUnderControlCertificateDocuments': 'Training\Training_PollutionUnderControlCertificateDocuments',
                        'RoofTopRainWaterHarvestingDocuments': 'Training\Training_RoofTopRainWaterHarvestingDocuments',
                        }
            
            file_mapping = {}
            for field, file_path in file_fields.items():
                files = request.FILES.getlist(field)
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path, field)

            serializer.save(user = self.request.user, **file_mapping)
            return Response({'status': 'success' ,
                            'Message': 'Data saved successfully'} , status= 200)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : error_message} , status = status.HTTP_400_BAD_REQUEST)

