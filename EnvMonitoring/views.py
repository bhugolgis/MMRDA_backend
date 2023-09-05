
from .serializer import *
from rest_framework.response import Response
from .models import *
from rest_framework import generics
# from .renderers import ErrorRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.contrib.gis.geos import Point
from rest_framework.permissions import IsAuthenticated  
from .paginations import LimitsetPagination
from Auth.permissions import IsConsultant , IsMMRDA
from .serializer import *
from .permissions import IsConsultant , IsContractor
from Training.utils import save_multiple_files



# The below class is a view for posting sensor location details and saving them in the database.
class PostSensorLocationDetails(generics.GenericAPIView):
    serializer_class = PostSensorLocationDetailsSerializer
    parser_classes = (MultiPartParser, )
    # queryset = labourcampDetails.objects.all()

    def post(self, request):
        """
        This function saves sensor location details in the database and returns a success message with
        the saved data or an error message if the data is invalid.
        
        :param request: The request object contains information about the HTTP request made to the
        server, such as the request method (POST in this case), headers, and body
        :return: The code is returning a response object with a JSON payload. The payload includes the
        following keys:
        - 'status': indicating the status of the request ('success' or 'error')
        - 'Message': providing a message related to the status
        - 'data': containing the serialized data if the request was successful
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            lat = float(serializer.validated_data['latitude'])
            long = float(serializer.validated_data['longitude'])
            location = Point(long, lat, srid=4326)
            instance = serializer.save(location=location)
            data = PostSensorLocationDetailsViewSerializer(instance).data
            return Response({'status': 'success',
                            'Message': 'Data saved successfully',
                                'data': data}, status=status.HTTP_200_OK)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+value[0]
            return Response({'status': 'error',
                            'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
        

   
# The class GetSensorLocationDetails is a generic ListAPIView that retrieves all sensor objects and
# uses the PostSensorLocationDetailsViewSerializer for serialization.
class GetSensorLocationDetails(generics.ListAPIView):
    queryset = sensors.objects.all() 
    serializer_class = PostSensorLocationDetailsViewSerializer


# The `AirView` class is a view in a Django REST framework API that handles the creation of Air
# objects based on user roles and permissions , group.
class AirView(generics.GenericAPIView):
    # renderer_classes = [ErrorRenderer]
    serializer_class = AirSerializer
    #parser_classes = [MultiPartParser]
    queryset = Air.objects.all()
    permission_classes = [ IsAuthenticated & (IsConsultant | IsContractor)]

    def post(self , request):
        # try:
            if "contractor" in request.user.groups.values_list("name",flat=True):
                Serializer = self.get_serializer(data = request.data , context={'request': request})
                if Serializer.is_valid():
                    date = str(Serializer.validated_data['dateOfMonitoringTwo']).split('-')
                    month  = Serializer.validated_data['month']
                    packages = Serializer.validated_data['packages']
                    data = self.get_queryset().filter( dateOfMonitoring__year = int(date[0]) , month = month , packages = packages ,  user = request.user.id , ).exists()
                    if data == True:
                        return Response({'status': 'success',
                                        'message':'already data filled for this Month'} , status=status.HTTP_400_BAD_REQUEST)
                    else:
                        lat=float(Serializer.validated_data['latitude'])
                        long=float(Serializer.validated_data['longitude'])
                        location=Point(long,lat,srid=4326)
                        air=Serializer.save(location=location ,  user = request.user)
                        data=AirViewSerializer(air).data
                        return Response({'status': 'success',
                                        'message' : 'data saved successfully',
                                        'data': data}, status= status.HTTP_200_OK)
                else:
                    key, value =list(Serializer.errors.items())[0]
                    error_message = key+" ,"+value[0]
                    print(value[0])
                    return Response({'status' : 'error',
                                    'message' : value[0]} , status = status.HTTP_400_BAD_REQUEST)
                
            elif "consultant" in request.user.groups.values_list("name",flat=True):
                Serializer = self.get_serializer(data = request.data , context={'request': request})
                if Serializer.is_valid():
                    lat=float(Serializer.validated_data['latitude'])
                    long=float(Serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)
                    air=Serializer.save(location=location , user = request.user)
                    data=AirViewSerializer(air).data
                    return Response({'status': 'success',
                                        'message' : 'data saved successfully',
                                        'data': data}, status= status.HTTP_200_OK)
                else:
                    key, value =list(Serializer.errors.items())[0]
                    error_message = key+" ,"+value[0]
                    print(value[0])
                    return Response({'status' : 'failed',
                                    'message' : value[0]}, status = status.HTTP_400_BAD_REQUEST)
            else:
                 return  Response({'status' : 'failed',
                            'message' : "Only consultant and Contractor can fill this form"}, status=status.HTTP_401_UNAUTHORIZED)

# The `AirUpdateView` class is a view in a Python Django application that handles updating Air data
# for a specific user.
class AirUpdateView(generics.UpdateAPIView):
    serializer_class = AirSerializer
    # renderer_classes = [ErrorRenderer]
    permission_classes = [IsAuthenticated , IsConsultant]
    #parser_classes = [MultiPartParser]

    def update(self, request , id ,  **kwargs):
        try:
            instance = Air.objects.get(id=id,user=request.user.id)
        except Exception:
            return Response({'success' : 'success' , 
                            "message": "There is no Air data for user %s" % (request.user.username)})

        serializer = AirSerializer(instance , data=request.data , partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success' : 'success' ,
                            'message' : 'Data Updated Successfully'} , status= 200)
        else:
            return Response({'status' : 'failed' , 
                            "message": "Please Enter a valid data"} , status= 400)



# The class AirListView is a generic ListAPIView that serializes Air objects and retrieves all
# instances of Air from the database.
class AirListView(generics.ListAPIView):
 
    serializer_class = AirViewSerializer
    #parser_classes = [MultiPartParser]
    queryset = Air.objects.all()



# The `WaterView` class is a view in a Django REST framework API that handles the creation of water
# data entries, with different permissions for consultants and contractors.
class WaterView(generics.GenericAPIView):
    # renderer_classes = [ErrorRenderer]
    serializer_class = WaterSerializer
    #parser_classes = [MultiPartParser]
    permission_classes = [ IsAuthenticated & (IsConsultant | IsContractor)]
    queryset = water.objects.all()
    
    def post(self , request):
        # try:
        if "contractor" in request.user.groups.values_list("name",flat=True) :
            serializer = WaterSerializer(data = request.data , context={'request': request})
            if serializer.is_valid():
                date = str(serializer.validated_data['dateOfMonitoringTwo']).split('-')
                quarter = serializer.validated_data['quarter']
                packages = serializer.validated_data['packages']
                data = self.get_queryset().filter( dateOfMonitoringTwo__year = int(date[0]) , quarter = quarter ,  packages = packages ).exists()
                if data == True:
                    return Response({'status':'success' , 
                                    'Message': 'already data filled for this Quarter'} , status=status.HTTP_400_BAD_REQUEST)
                else:
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)
                    water_data =serializer.save(location=location , user = request.user)
                    data = waterviewserializer(water_data).data
                    return Response({'status': 'success' , 
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
        elif "consultant" in request.user.groups.values_list("name",flat=True):
            # return  Response({'status': 'failed',
            #                 'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)

            serializer = self.get_serializer(data = request.data , context={'request': request})
            if serializer.is_valid():
                lat=float(serializer.validated_data['latitude'])
                long=float(serializer.validated_data['longitude'])
                location=Point(long,lat,srid=4326)
                water_data =serializer.save(location=location , user = request.user)
                data = waterviewserializer(water_data).data
                return Response({'status': 'success' , 
                                    'Message' : 'data saved successfully',
                                    'datat' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'failed',
                                'Message' : value[0]} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return  Response({'status': 'failed',
                            'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)



# The `waterupdateView` class is a view in a Django REST framework API that allows authenticated
# consultants to update water data for a specific user.
class waterupdateView(generics.UpdateAPIView):
    # renderer_classes = [ErrorRenderer]
    serializer_class = waterviewserializer
    permission_classes = [IsAuthenticated , IsConsultant]
    #parser_classes = [MultiPartParser]

    def update(self, request , id , **kwargs):
        try:
            instance = water.objects.get(id=id,user=request.user.id)
        except Exception:
            return Response({'status' : 'success',
                            "Message": "There is no Water data for user %s" % (request.user.username)})
        serializer = AirSerializer(instance , data=request.data , partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': 'success' , 
                            'Message' : 'data saved successfully'}, status = 200)
        else:
            return Response({'status' : 'failed' , 
                            "Message": "Please Enter a valid data"} , status= 400)


# The waterListView class is a generic ListAPIView that retrieves a list of water objects and uses the
# waterviewserializer for serialization.
class waterListView(generics.ListAPIView):
    serializer_class = waterviewserializer
    #parser_classes = [MultiPartParser]
    pagination_class = LimitsetPagination
    # renderer_classes = [ErrorRenderer]
    queryset = water.objects.all()




# The NoiseView class is a view in a Django REST framework API that handles the creation of noise
# data, with different permissions for consultants and contractors.
class NoiseView(generics.GenericAPIView):
    # renderer_classes = [ErrorRenderer]
    serializer_class = NoiseSerializer
    #parser_classes = [MultiPartParser]
    permission_classes = [ IsAuthenticated & (IsConsultant | IsContractor)]
    
    def post(self , request):
        # try:
        if "contractor" in request.user.groups.values_list("name",flat=True):
            serializer = NoiseSerializer(data = request.data , context={'request': request})
            if serializer.is_valid():
                date = str(serializer.validated_data['dateOfMonitoringThree']).split('-')
                month  = serializer.validated_data['month']
                packages = serializer.validated_data['packages']
                data = Noise.objects.filter( dateOfMonitoringThree__year = int(date[0]) , month = month ,  packages = packages).exists()
                if data == True:
                    return Response({'status':'success' , 
                                    'Message': 'already data filled for this Month'} , status=status.HTTP_400_BAD_REQUEST)
                else:
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)
                    water_data =serializer.save(location=location , user = request.user)
                    data = Noiseviewserializer(water_data).data
                    return Response({'status': 'success' , 
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'failed',
                                'Message' : value[0]} , status = status.HTTP_400_BAD_REQUEST)
        elif "consultant" in request.user.groups.values_list("name",flat=True):
                # return  Response({'status': 'failed',
                #         'Message' : "Only consultant and Contractor can fill this form"} , status= status.HTTP_401_UNAUTHORIZED)
                
                serializer = NoiseSerializer(data = request.data , context={'request': request})
                if serializer.is_valid():
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)
                    water_data =serializer.save(location=location , user = request.user)
                    data = Noiseviewserializer(water_data).data
                    return Response({'status': 'success' , 
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = key+" ,"+value[0]
                    return Response({'status': 'failed',
                                    'Message' : value[0]} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return  Response({'status': 'failed',
                            'Message' : "Only consultant and Contractor can fill this form"} , status= status.HTTP_401_UNAUTHORIZED)

# The `NoiseupdateView` class is a view for updating a Noise object with a NoiseSerializer, with
# authentication and permission checks.
class NoiseupdateView(generics.UpdateAPIView):
    serializer_class = NoiseSerializer
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated , IsConsultant]

    def update(self, request , id , **kwargs):
        try:
            instance = Noise.objects.get(id=id,user=request.user.id)
        except Exception:
            return Response({"Message": "There is no Noise data for user %s" % (request.user.username)})
        serializer = NoiseSerializer(instance , data=request.data , partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": "Please Enter a valid data"})
        
# The NoiseListView class is a generic ListAPIView that retrieves a list of Noise objects and uses the
# Noiseviewserializer to serialize the data.
class NoiseListView(generics.ListAPIView):
    pagination_class = LimitsetPagination
    serializer_class = Noiseviewserializer
    # renderer_classes = [ErrorRenderer]
    queryset = Noise.objects.all()



# The `ExistingTreeManagementView` class is a view in a Python Django project that handles the
# creation of tree management data, with different permissions for contractors and consultants.
class ExistingTreeManagementView(generics.GenericAPIView):
    serializer_class = TreeManagementSerailizer
    # renderer_classes = [ErrorRenderer]
    # #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
  
    
    def post(self , request):
        # try:
        if "contractor" in request.user.groups.values_list("name",flat=True):
            serializer = self.get_serializer(data = request.data )
            if serializer.is_valid():
                date = str(serializer.validated_data['dateOfMonitoring']).split('-')
                month  = serializer.validated_data['month']
                packages = serializer.validated_data['packages']
                data = ExistingTreeManagment.objects.filter( dateOfMonitoring__year = int(date[0]) , month = month ,  packages = packages ).exists()
                if data == True:
                    return Response({'message':'already data filled for this Month'} , status=status.HTTP_400_BAD_REQUEST)
                else:

                    file_fields = {
                    'documents': 'Existingtree_photos',
                    'photographs': 'existingTree_documents' ,}
                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    Plocation=Point(long,lat,srid=4326)

                    water_data =serializer.save(location=Plocation , user = request.user , **file_mapping)
                    data = TreeManagmentviewserializer(water_data).data
                    return Response({'status': 'success' , 
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ," + value[0]
                return Response({'status': 'error',
                                'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
        elif "consultant" in request.user.groups.values_list("name",flat=True):
                serializer = self.get_serializer(data = request.data )
                if serializer.is_valid():

                    file_fields = {
                    'documents': 'Existingtree_photos',
                    'photographs': 'existingTree_documents' ,}

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    Plocation=Point(long,lat,srid=4326)
                   
                    water_data =serializer.save(location=Plocation , user = request.user , **file_mapping)
                    data = TreeManagmentviewserializer(water_data).data
                    return Response({'status': 'success' , 
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = key+" ," + value[0]
                    return Response({'status': 'error',
                                    'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return  Response({'status': 'failed',
                            'Message' : "Only consultant and Contractor can fill this form"} , status= status.HTTP_401_UNAUTHORIZED)



# The `ExistingTreeManagmentUpdateView` class is a view for updating an existing tree management
# object with the provided data.
class ExistingTreeManagmentUpdateView(generics.UpdateAPIView):
    serializer_class = TreeManagementSerailizer
    permission_classes = [IsAuthenticated, IsConsultant]
    
    def update(self, request , id , **kwargs):
        try:
            instance = ExistingTreeManagment.objects.get(id=id,user=request.user.id)
        except Exception:
            return Response({"msg": "There is no Tree data for user %s" % (request.user.username)})
        serializer = TreeManagementSerailizer(instance , data=request.data , partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": "Please Enter a valid data"})



# The class `ExistingTereeManagementView` is a view that lists existing tree management objects and
# uses a serializer and pagination.
class ExistingTereeManagementView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = TreeManagmentviewserializer
    pagination_class = LimitsetPagination
    # #parser_classes = [MultiPartParser]
    queryset = ExistingTreeManagment.objects.all()



# The GetExistingTreeIDView class retrieves information about an existing tree based on its ID.
class GetExistingTreeIDView(generics.GenericAPIView):
    serializer_class = TreeManagementSerailizer
    #parser_classes = [MultiPartParser]

    def get(self, request, treeID):
        try:
            treedata = ExistingTreeManagment.objects.get(treeID=treeID)
        except:
            return Response({'Message': 'No data Avaialable for this Tree-ID',
                            'status' : 'success'}, status=200)
        if treedata.actionTaken == "To be Retained":
            return Response({'Message': 'For the enterd ID , Tree is Retained',
                            'status' : 'success'}, status=200)
        serializers = TreeManagmentviewserializer(treedata).data
        return Response(serializers, status=200)
        

# The `NewTereeManagementView` class is a view in a Django REST framework API that handles the
# creation of new tree management data, with different permissions for contractors and consultants.
class NewTereeManagementView(generics.GenericAPIView):
    serializer_class = NewTreeManagmentSerializer
    # #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self , request):
        # try:
        if "contractor" in request.user.groups.values_list("name",flat=True) :
            serializer = NewTreeManagmentSerializer(data = request.data )
            if serializer.is_valid():
                date = str(serializer.validated_data['dateOfMonitoring']).split('-')
                month  = serializer.validated_data['month']
                packages = serializer.validated_data['packages']
                data = NewTreeManagement.objects.filter( dateOfMonitoring__year = int(date[0]) , month = month  ,  packages = packages ).exists()
                if data == True:
                    return Response({'message':'already data filled for this Month'} , status=status.HTTP_400_BAD_REQUEST)
                else:
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)

                    file_fields = {
                    'documents': 'newTree_photographs',
                    'photographs': 'newTree_documents' ,}

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)
                    
                    water_data =serializer.save(location=location , user = request.user , **file_mapping)
                    data = NewTreeManagmentviewserializer(water_data).data
                    return Response({'status': 'success' , 
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ," + value[0]
                return Response({'status': 'error',
                                'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
            
        elif "consultant" in request.user.groups.values_list("name",flat=True):
                # return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)

                serializer = NewTreeManagmentSerializer(data = request.data )
                if serializer.is_valid():
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)

                    file_fields = {
                    'documents': 'newTree_photographs',
                    'photographs': 'newTree_documents' ,}
                    
                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)


                    water_data =serializer.save(location=location , user = request.user , **file_mapping)
                    data = NewTreeManagmentviewserializer(water_data).data
                    return Response({'status': 'success' , 
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = key+" ," + value[0]
                    return Response({'status': 'error',
                                   'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
        else:
        # except Exception:
            return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)


# The WasteTreatmentsView class is a view in a Django REST framework API that handles the creation of
# waste treatment data, with different permissions for contractors and consultants.
class WasteTreatmentsView(generics.GenericAPIView):
    serializer_class = WasteTreatmentsSerializer
    # renderer_classes = [ErrorRenderer]
    # #parser_classes = [MultiPartParser]
    permission_classes = [ IsAuthenticated , ]
    
    def post(self , request):
   
        if "contractor" in request.user.groups.values_list("name",flat=True)  :
            serializer = WasteTreatmentsSerializer(data = request.data , context={'request': request})
            if serializer.is_valid():
                date = str(serializer.validated_data['dateOfMonitoring']).split('-')
                month  = serializer.validated_data['month']
                packages = serializer.validated_data['packages']
                data = WasteTreatments.objects.filter(dateOfMonitoring__year = int(date[0]) , month = month  ,  packages = packages).exists()
                if data == True:
                    return Response({'message':'already data filled for this Month'} , status=status.HTTP_400_BAD_REQUEST)
                
                else:
                    longitude = float(serializer.validated_data['waste_longitude'])
                    latitude = float(serializer.validated_data['waste_latitude'])
                    waste_location=Point(longitude,latitude,srid=4326)

                    
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)
                    
                    
                    file_fields = {
                    'documents': 'waste_documents',
                    'photographs': 'waste_photographs' ,}

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    waste_data =serializer.save(location=location , wasteHandlingLocation = waste_location , user = request.user , **file_mapping)
                    data = wastetreatmentsViewserializer(waste_data).data
                    return Response({'status': 'success' , 
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ," + value[0]
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        elif "consultant" in request.user.groups.values_list("name",flat=True):
            serializer = WasteTreatmentsSerializer(data = request.data , context={'request': request})
            if serializer.is_valid():
                longitude = float(serializer.validated_data['waste_longitude'])
                latitude = float(serializer.validated_data['waste_latitude'])
                waste_location=Point(longitude,latitude,srid=4326)
                
                lat=float(serializer.validated_data['latitude'])
                long=float(serializer.validated_data['longitude'])
                location=Point(long,lat,srid=4326)

                file_fields = {
                    'documents': 'waste_documents',
                    'photographs': 'waste_photographs' ,}

                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path , field)

                waste_data =serializer.save( location=location , wasteHandlingLocation = waste_location , user = request.user , **file_mapping)
                data = wastetreatmentsViewserializer(waste_data).data
                return Response({'status': 'success' , 
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ," + value[0]
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)


# The `wastemanagementUpdateView` class is an API view that allows authenticated consultants to update
# waste treatment data for a specific user.
class wastemanagementUpdateView(generics.UpdateAPIView):
    serializer_class = wastetreatmentsViewserializer
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsConsultant]
    
    def update(self, request , id , **kwargs):
        try:
            instance = WasteTreatments.objects.get(id=id,user=request.user.id)
        except Exception:
            return Response({"msg": "There is no Tree data for user %s" % (request.user.username)})
        serializer = WasteTreatmentsSerializer(instance , data=request.data , partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": "Please Enter a valid data"})



# The `MaterialSourcingView` class is a view in a Django REST framework API that handles the creation
# of material sourcing data, with different logic based on the user's role.
class MaterialSourcingView(generics.GenericAPIView):
    serializer_class = MaterialManagmentSerializer
    # renderer_classes = [ErrorRenderer]
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self , request):
        # try:
            if "contractor" in request.user.groups.values_list("name",flat=True) :
                serializer = self.get_serializer(data = request.data , context={'request': request})
                if serializer.is_valid():
                    date = str(serializer.validated_data['dateOfMonitoring']).split('-')
                    month  = serializer.validated_data['month']
                    packages = serializer.validated_data['packages']
                    data = MaterialManegmanet.objects.filter( dateOfMonitoring__year = int(date[0]) , month = month  ,  packages = packages  ).exists()
                    if data == True:
                        return Response({'message':'already data filled for this Month'} , status=status.HTTP_400_BAD_REQUEST)
                    else:
                        lat=float(serializer.validated_data['latitude'])
                        long=float(serializer.validated_data['longitude'])
                        location=Point(long,lat,srid=4326)

                        storagelong = float(serializer.validated_data['storageLongitude'])
                        storagelat = float(serializer.validated_data['storageLatitude'])
                        storageLocation = Point(storagelong , storagelat , srid = 4326 )

                        file_fields = {
                        'approvals' : 'MaterialManegment/materialsourcing_documents',
                        'materialStoragePhotograph': 'MaterialManegment/materailStorage_Photograph' ,
                        'documents': 'MaterialManegment/materialsourcing_photographs',
                        'photographs': 'MaterialManegment/materialsourcing_documents' ,}

                        file_mapping = {}
                        for field, file_path in file_fields.items():
                            files = request.FILES.getlist(field)
                            file_mapping[field] = []
                            save_multiple_files(files, file_mapping, file_path , field)

                        material_data =serializer.save(location=location , storageLocation = storageLocation , user = request.user , **file_mapping)
                        data = MaterialSourcingViewserializer(material_data).data
                        return Response({'status': 'success' , 
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = key+" ," + value[0]
                    return Response({'status': 'error',
                                    'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
            elif "consultant" in request.user.groups.values_list("name",flat=True):
            #   return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)
                serializer = self.get_serializer(data = request.data , context={'request': request})
                if serializer.is_valid():
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)

                    storagelong = float(serializer.validated_data['storageLongitude'])
                    storagelat = float(serializer.validated_data['storageLatitude'])
                    storageLocation = Point(storagelong , storagelat , srid = 4326 )

                    file_fields = {
                        'approvals' : 'MaterialManegment/materialsourcing_documents',
                        'materialStoragePhotograph': 'MaterialManegment/materailStorage_Photograph' ,
                        'documents': 'MaterialManegment/materialsourcing_photographs',
                        'photographs': 'MaterialManegment/materialsourcing_documents' ,}

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    material_data =serializer.save( location=location , storageLocation = storageLocation , user = request.user , **file_mapping)
                    data = MaterialSourcingViewserializer(material_data).data
                    return Response({'status': 'success' , 
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = key+" ," + value[0]
                    return Response({'status': 'error',
                                    'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
            else:
                return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)


# This is a class for updating material management data with authentication and error handling.
class materialmanagemantUpdate(generics.UpdateAPIView):
    serializer_class = MaterialManagmentSerializer
    # renderer_classes = [ErrorRenderer]
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def update(self, request , id , **kwargs):
        try:
            instance = MaterialManegmanet.objects.get(id=id,user=request.user.id)
        except Exception:
            return Response({"msg": "There is no Tree data for user %s" % (request.user.username)})
        serializer = MaterialManagmentSerializer(instance , data=request.data , partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"msg": "Please Enter a valid data"})


# The `TreemanagmentAPI` class is a generic API view that retrieves tree management instances based on
# a specified package name.
class TreemanagmentAPI(generics.GenericAPIView):
    serializer_class = TreemanagementSerializer
    def get(self, request,packages, *args, **kwargs):
            packages = packages
            instance = ExistingTreeManagment.objects.filter(packages__iexact=packages)
            if instance :
                serializer = TreemanagementSerializer(instance, many=True)
                return Response({'status': 200,'data': serializer.data,
                                   'message': 'successfully'})
            else:
                return Response({'status':403,'message':'invalid package'})



# The AirAPI class is a generic API view that retrieves Air objects based on a specified package and
# returns a response with the serialized data.
class AirAPI(generics.GenericAPIView):
    serializer_class = AirmanagementSerializer
    def get(self, request,packages, *args, **kwargs):
        instance = Air.objects.filter(packages__iexact=packages)
        if instance:
            serializer = AirmanagementSerializer(instance, many=True)
            return Response({'status': 200, 'data': serializer.data,
                                      'message': 'successfully'})
        else:
            return Response({'status': 403, 'message': 'invalid package'})


# The NoiseAPI class is a generic API view that retrieves noise data based on a specified package
# name.
class NoiseAPI(generics.GenericAPIView):
    serializer_class = NoisemanagementSerializer
    def get(self, request,packages, *args, **kwargs):
        packages = packages
        instance = Noise.objects.filter(packages__iexact=packages)
        if instance:
            serializer = NoisemanagementSerializer(instance, many=True)
            return Response({'status': 200, 'data': serializer.data,
                                      'message': 'successfully'})
        else:
            return Response({'status': 403, 'message': 'invalid package'})

# The WasteTreatmentsAPI class is a generic API view that retrieves waste treatments based on a
# specified package.
class WasteTreatmentsAPI(generics.GenericAPIView):
    serializer_class = WasteSerializer 
    def get(self, request,packages, *args, **kwargs):
        packages = packages
        instance = WasteTreatments.objects.filter(packages__iexact=packages).exists()
        if instance:
            serializer = WasteSerializer(instance, many=True)
            return Response({'status': 200, 'data': serializer.data,
                                      'message': 'successfully'})
        else:
            return Response({'status': 403, 'message': 'invalid package'})


# The MaterialSourcingAPI class is a generic API view that retrieves material instances based on a
# specified package and returns a response with the serialized data.
class MaterialSourcingAPI(generics.GenericAPIView):
    serializer_class = MaterialSerializer
    def get(self, request,packages, *args, **kwargs):
        packages = packages
        instance = MaterialManegmanet.objects.filter(packages__iexact=packages)
        if instance:
            serializer = MaterialSerializer(instance, many=True)
            return Response({'status': 200, 'data': serializer.data,
                                      'message': 'successfully'})
        else:
            return Response({'status':403,'message':'invalid package'})



# The WatermanagmentAPI class is a generic API view that retrieves water management data based on a
# specified package.
class WatermanagmentAPI(generics.GenericAPIView):
    serializer_class = WatermanamentSerializer
    def get(self, request,packages, *args, **kwargs):
        packages = packages
        instance = water.objects.filter(packages__iexact=packages)
        if instance:
            serializer = WatermanamentSerializer(instance, many=True)
            return Response({'status': 200, 'data': serializer.data,
                                      'message': 'successfully'})
        else:
            return Response({'status': 403, 'message': 'invalid package'})

