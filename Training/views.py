from rest_framework import generics
from .serialzers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.response import Response
from django.contrib.gis.geos import Point 
from .models import traning, photographs
from .permission import IsConsultant
from rest_framework import filters
from rest_framework import status
from MMRDA.utils import error_simplifier
from .utils import save_multiple_files


# Create your views here.

class TraningView(generics.GenericAPIView):
    serializer_class = TraningSerializer
    permission_classes = [IsAuthenticated]
    #parser_classes = [MultiPartParser]

    def post(self, request):
        # try:
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
        # except:
        #     return Response({'Please Enetr a valid data'}, status=400)


class TrainingListView(generics.ListAPIView):
    serializer_class = TraningSerializer
    permission_classes = [IsAuthenticated, IsConsultant]
    queryset = traning.objects.all()


class TrainingupdateView(generics.UpdateAPIView):
    serializer_class = TraningSerializer
    #parser_classes = [MultiPartParser]
    queryset = traning.objects.all()

    def update(self, request, pk, *args, **kwargs):
        try:
            instance = traning.objects.get(id=pk)
            serializer = TraningSerializer(
                instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except:
            return Response({'Message': 'Matching Id DoesNotExist'})


class PhotographsView(generics.GenericAPIView):
    serializer_class = photographsSerializer
    # permission_classes = [IsAuthenticated, IsConsultant]
    #parser_classes = [MultiPartParser]

    def post(self, request):
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


class photographsListView(generics.GenericAPIView):
    serializer_class = photographsViewSerializer
    # permission_classes = [IsAuthenticated, IsConsultant]
    #parser_classes = [MultiPartParser]
    queryset = photographs.objects.all()

    def get(self , request):
        serializer = self.get_serializer(self.get_queryset() , many = True)
        return Response({'message':serializer.data})


class updatephotographview(generics.UpdateAPIView):
    serializer_class = photographsViewSerializer
    #parser_classes = [MultiPartParser]
    queryset = photographs.objects.all()

    def update(self, request, pk, *args, **kwargs):
        try:
            instance = photographs.objects.get(id=pk)
            serializer = photographsViewSerializer(
                instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
        except:
            return Response({"message": "Matching id does not exist"})


class occupationalHealthSafety (generics.GenericAPIView):
    serializer_class = occupationalHealthSafetySerialziers
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        serializer = self.get_serializer(data = request.data )
        if serializer.is_valid():
            lat = float(serializer.validated_data['latitude'])
            long = float(serializer.validated_data['longitude'])

            location = Point(long, lat, srid=4326)

            incidentlatitude = float(serializer.validated_data['incidentlatitude'])
            incidentlongitude = float(serializer.validated_data['incidentlongitude'])
            
            incidentLocation = Point(incidentlongitude, incidentlatitude, srid=4326)

            file_fields = {
                        'documents': 'OccupationalHealth&Safety',
                        'photographs': 'OccupationalHealth&Safety' ,}

            file_mapping = {}
            for field, file_path in file_fields.items():
                files = request.FILES.getlist(field)
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path , field)
                
            data = serializer.save(location=location , incidentLocation = incidentLocation, user = request.user , **file_mapping)
            data = occupationalHealthSafetyViewSerializer(data).data
            return Response({'status' : 'success',
                             'Message' : 'Data Saved Successfully'}, status=200)
        else:
            key, value =list(serializer.errors.items())[0]
            # error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : value[0]} , status = status.HTTP_400_BAD_REQUEST)

   
      

class ContactUsView(generics.GenericAPIView):
    serializer_class = ContactusSerializezr
    # parser_classes = (FormParser,) 
    def post(self, request):

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


class PreConstructionStageComplianceView(generics.GenericAPIView):
    serializer_class = PreConstructionStageComplianceSerialzier
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def post(self , request):
        data = request.data
        serializer= PreConstructionStageComplianceSerialzier (data = data)
        if serializer.is_valid():
            serializer.save(user = self.request.user)
            return Response({'status': 'success' ,
                            'Message': 'Data saved successfully'} , status= 200)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : error_message } , status = status.HTTP_400_BAD_REQUEST)
                    

class ConstructionStageComplainceView(generics.CreateAPIView):
    serializer_class = ConstructionStageComplainceSerializer
    permission_classes = [IsAuthenticated]
    #parser_classes = [MultiPartParser]

    def post(self , request):
        data = request.data
        serializer= ConstructionStageComplainceSerializer(data = data)
        if serializer.is_valid(raise_exception= True):
            serializer.save(user = self.request.user)
            return Response({'status': 'success' ,
                            'Message': 'Data saved successfully'} , status= 200)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : error_message} , status = status.HTTP_400_BAD_REQUEST)


class ContactUsimagesCompress(generics.CreateAPIView):
    serializer_class =  ContactusImagesSeilizer
    #parser_classes = [MultiPartParser]
    queryset = ContactusImage.objects.all()
