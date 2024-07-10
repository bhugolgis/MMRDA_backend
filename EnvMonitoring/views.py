
from .serializer import *
from rest_framework.response import Response
from .models import *
from rest_framework import generics
# from .renderers import ErrorRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.contrib.gis.geos import Point,GEOSGeometry
from rest_framework.permissions import IsAuthenticated  , DjangoModelPermissions
from .paginations import LimitsetPagination
from Auth.permissions import IsConsultant , IsMMRDA
from .serializer import *
from .permissions import IsConsultant , IsContractor
from MMRDA.utils import error_simplifier
from Training.utils import save_multiple_files

from .utils import SubIndices

class PostSensorLocationDetails(generics.GenericAPIView):
    serializer_class = PostSensorLocationDetailsSerializer
    parser_classes = (MultiPartParser, )
    # queryset = labourcampDetails.objects.all()

    def post(self, request):

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
            error_message = str(key)+" ," + str(value[0])
            return Response({'status': 'error',
                            'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)



class GetSensorLocationDetails(generics.ListAPIView):
    queryset = sensors.objects.all()
    serializer_class = PostSensorLocationDetailsViewSerializer

class GenerateAQI(generics.GenericAPIView):
    serializer_class = GenerateAQISerializer
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            measures = serializer.validated_data.values()
            #     PM10 = sub_indices_calculator.get_PM10_subindex(serializer.validated_data['PM10'])
            print(serializer.validated_data.keys())
            print(request.data)
           
            sub_indices_calculator = SubIndices()
            # PM10 = sub_indices_calculator.get_PM10_subindex(serializer.validated_data['PM10'])
        
            # checking if parameter empty or not if empty return 0 else calculate subindex
            PM10 = sub_indices_calculator.get_PM10_subindex(serializer.validated_data['PM10']) if "PM10" in serializer.validated_data.keys() else 0
            PM2_5 = sub_indices_calculator.get_PM2_5_subindex(serializer.validated_data['PM2_5']) if "PM2_5" in serializer.validated_data.keys() else 0
            SO2 = sub_indices_calculator.get_SO2_subindex(serializer.validated_data['SO2']) if "SO2" in serializer.validated_data.keys() else 0
            NOx = sub_indices_calculator.get_NOx_subindex(serializer.validated_data['NOx']) if "NOx" in serializer.validated_data.keys() else 0
            CO = sub_indices_calculator.get_CO_subindex(serializer.validated_data['CO']) if "CO" in serializer.validated_data.keys() else 0
            

            # print(NOx)
            # AQI = max(measures)
            sub_indices = [PM10, PM2_5, NOx, SO2, CO]
            print(sub_indices)
            AQI = max(PM10, PM2_5, NOx, SO2, CO)

            quality = sub_indices_calculator.check_air_quality(AQI)

            return Response({
                "message":"AQI generated successfully",
                "status":"success",
                "data":AQI,
                "quality": quality
            })
        else:
            error = error_simplifier(serializer.errors)
            return Response({
                "message":error,
                "status":"error"
            },status=status.HTTP_400_BAD_REQUEST)


class AirView(generics.GenericAPIView):
    # renderer_classes = [ErrorRenderer]
    serializer_class = AirSerializer
    parser_classes = [MultiPartParser]
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
                    error_message = str(key)+" ," + str(value[0])
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
                    error_message = str(key)+" ," + str(value[0])
                    print(value[0])
                    return Response({'status' : 'failed',
                                    'message' : value[0]}, status = status.HTTP_400_BAD_REQUEST)
            else:
                 return  Response({'status' : 'failed',
                            'message' : "Only consultant and Contractor can fill this form"}, status=status.HTTP_401_UNAUTHORIZED)

class AirUpdateView(generics.UpdateAPIView):
    serializer_class = AirSerializer
    # renderer_classes = [ErrorRenderer]
    permission_classes = [IsAuthenticated , IsConsultant]
    parser_classes = [MultiPartParser]

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

class AirListView(generics.ListAPIView):

    serializer_class = AirViewSerializer
    parser_classes = [MultiPartParser]
    queryset = Air.objects.all()



class WaterView(generics.GenericAPIView):
    # renderer_classes = [ErrorRenderer]
    serializer_class = WaterSerializer
    parser_classes = [MultiPartParser]
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
                error_message = str(key)+" ," + str(value[0])
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
                error_message = str(key)+" ," + str(value[0])
                return Response({'status': 'failed',
                                'Message' : value[0]} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return  Response({'status': 'failed',
                            'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)


class waterupdateView(generics.UpdateAPIView):
    # renderer_classes = [ErrorRenderer]
    serializer_class = waterviewserializer
    permission_classes = [IsAuthenticated , IsConsultant]
    parser_classes = [MultiPartParser]

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

class waterListView(generics.ListAPIView):
    serializer_class = waterviewserializer
    parser_classes = [MultiPartParser]
    pagination_class = LimitsetPagination
    # renderer_classes = [ErrorRenderer]
    queryset = water.objects.all()




class NoiseView(generics.GenericAPIView):
    # renderer_classes = [ErrorRenderer]
    serializer_class = NoiseSerializer
    parser_classes = [MultiPartParser]
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
                error_message = str(key)+" ," + str(value[0])
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
                    error_message = str(key)+" ," + str(value[0])
                    return Response({'status': 'failed',
                                    'Message' : value[0]} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return  Response({'status': 'failed',
                            'Message' : "Only consultant and Contractor can fill this form"} , status= status.HTTP_401_UNAUTHORIZED)

class NoiseupdateView(generics.UpdateAPIView):
    serializer_class = NoiseSerializer
    parser_classes = [MultiPartParser]
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


class NoiseListView(generics.ListAPIView):
    pagination_class = LimitsetPagination
    serializer_class = Noiseviewserializer
    # renderer_classes = [ErrorRenderer]
    queryset = Noise.objects.all()



class ExistingTreeManagementView(generics.GenericAPIView):
    serializer_class = TreeManagementSerailizer
    # renderer_classes = [ErrorRenderer]
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated]


    def post(self , request):
        # try:
        if "contractor" in request.user.groups.values_list("name",flat=True):
            serializer = TreeManagementSerailizer(data = request.data )
            if serializer.is_valid():
                date = str(serializer.validated_data['dateOfMonitoring']).split('-')
                month  = serializer.validated_data['month']
                packages = serializer.validated_data['packages']
                data = ExistingTreeManagment.objects.filter( dateOfMonitoring__year = int(date[0]) , month = month ,  packages = packages ).exists()
                if data == True:
                    return Response({'message':'already data filled for this Month'} , status=status.HTTP_400_BAD_REQUEST)
                else:
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    Plocation=Point(long,lat,srid=4326)
                    
                    file_fields = {
                        'photographs' : 'ExistingTreeManagement/Photographs',
                        'documents' : 'ExistingTreeManagement/documents'
                        }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    tree_data =serializer.save(location=Plocation , user = request.user, **file_mapping)
                    data = TreeManagmentviewserializer(tree_data).data
                    return Response({'status': 'success' ,
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = str(key)+" ," + str(value[0])
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        elif "consultant" in request.user.groups.values_list("name",flat=True):
                serializer = TreeManagementSerailizer(data = request.data )
                if serializer.is_valid():
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    Plocation=Point(long,lat,srid=4326)
                    file_fields = {
                        'photographs' : 'ExistingTreeManagement/Photographs',
                        'documents' : 'ExistingTreeManagement/documents'
                        }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    tree_data =serializer.save(location=Plocation , user = request.user, **file_mapping)
                    data = TreeManagmentviewserializer(tree_data).data
                    return Response({'status': 'success' ,
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = str(key)+" ," + str(value[0])
                    return Response({'status': 'error',
                                    'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return  Response({'status': 'failed',
                            'Message' : "Only consultant and Contractor can fill this form"} , status= status.HTTP_401_UNAUTHORIZED)



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


class ExistingTereeManagementView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = TreeManagmentviewserializer
    pagination_class = LimitsetPagination
    # parser_classes = [MultiPartParser]
    queryset = ExistingTreeManagment.objects.all()


class GetExistingTreeIDView(generics.GenericAPIView):
    serializer_class = TreeManagementSerailizer
    parser_classes = [MultiPartParser]

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


class NewTereeManagementView(generics.GenericAPIView):
    serializer_class = NewTreeManagmentSerializer
    parser_classes = [MultiPartParser]
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
                        'photographs' : 'NewTreeManagement/Photographs',
                        'documents' : 'NewTreeManagement/Documents'
                        }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    new_tree_data =serializer.save(location=location , user = request.user, **file_mapping)
                    data = NewTreeManagmentviewserializer(new_tree_data).data
                    return Response({'status': 'success' ,
                                    'Message' : 'data saved successfully',
                                    'data' : data }, status = 200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = str(key)+" ," + str(value[0])
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)

        elif "consultant" in request.user.groups.values_list("name",flat=True):
                # return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)

                serializer = NewTreeManagmentSerializer(data = request.data )
                if serializer.is_valid():
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)
                    file_fields = {
                        'photographs' : 'NewTreeManagement/Photographs',
                        'documents' : 'NewTreeManagement/Documents'
                        }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    new_tree_data =serializer.save(location=location , user = request.user, **file_mapping)
                    data = NewTreeManagmentviewserializer(new_tree_data).data
                    return Response({'status': 'success' ,
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = str(key)+" ," + str(value[0])
                    return Response({'status': 'error',
                                   'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
        # except Exception:
            return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)




class WasteTreatmentsView(generics.GenericAPIView):
    serializer_class = WasteTreatmentsSerializer
    # renderer_classes = [ErrorRenderer]
    parser_classes = [MultiPartParser]
    permission_classes = [ IsAuthenticated , ]

    def post(self , request):
        # try:
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
                        'photographs' : 'Wastetreatment/Photographs',
                        'documents' : 'Wastetreatment/documents',
                        'GISPermitsTransportationDocuments' : 'Wastetreatment/GISPermitsTransportationDocuments',
                        'TransportationVechicalHasPermissionDocuments' : 'Wastetreatment/TransportationVechicalHasPermissionDocuments'
                        }

                        file_mapping = {}
                        for field, file_path in file_fields.items():
                            files = request.FILES.getlist(field)
                            file_mapping[field] = []
                            save_multiple_files(files, file_mapping, file_path , field)

                        waste_data =serializer.save(location=location , wasteHandlingLocation = waste_location , user = request.user, **file_mapping)
                        data = wastetreatmentsViewserializer(waste_data).data
                        return Response({'status': 'success' ,
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = str(key)+" ," + str(value[0])
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
                        'photographs' : 'Wastetreatment/Photographs',
                        'documents' : 'Wastetreatment/documents',
                        'GISPermitsTransportationDocuments' : 'Wastetreatment/GISPermitsTransportationDocuments',
                        'TransportationVechicalHasPermissionDocuments' : 'Wastetreatment/TransportationVechicalHasPermissionDocuments'
                    }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    waste_data =serializer.save(location=location , wasteHandlingLocation = waste_location , user = request.user, **file_mapping)

                    data = wastetreatmentsViewserializer(waste_data).data
                    return Response({'status': 'success' ,
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = str(key)+" ," + str(value[0])
                    return Response({'status': 'error',
                                    'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
            else:
                return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)


class wastemanagementUpdateView(generics.UpdateAPIView):
    serializer_class = wastetreatmentsViewserializer
    parser_classes = [MultiPartParser]
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

class MaterialSourcingView(generics.GenericAPIView):
    serializer_class = MaterialManagmentSerializer
    # renderer_classes = [ErrorRenderer]
    parser_classes = [MultiPartParser]
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
                        'photographs' : 'MaterialManagement/Photographs',
                        'documents' : 'MaterialManagement/Documents',
                        'approvals' : 'MaterialManagement/Approvals',
                        'materialStoragePhotograph' : 'MaterialManagement/StoragePhotograph',
                        }

                        file_mapping = {}
                        for field, file_path in file_fields.items():
                            files = request.FILES.getlist(field)
                            file_mapping[field] = []
                            save_multiple_files(files, file_mapping, file_path , field)

                        material_data =serializer.save(location=location , storageLocation = storageLocation , user = request.user, **file_mapping)
                        data = MaterialSourcingViewserializer(material_data).data
                        return Response({'status': 'success' ,
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = str(key)+" ," + str(value[0])
                    return Response({'status': 'error',
                                    'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
            elif "consultant" in request.user.groups.values_list("name",flat=True):
                serializer = self.get_serializer(data = request.data , context={'request': request})
                if serializer.is_valid():
                    lat=float(serializer.validated_data['latitude'])
                    long=float(serializer.validated_data['longitude'])
                    location=Point(long,lat,srid=4326)

                    storagelong = float(serializer.validated_data['storageLongitude'])
                    storagelat = float(serializer.validated_data['storageLatitude'])
                    storageLocation = Point(storagelong , storagelat , srid = 4326 )
                    file_fields = {
                        'photographs' : 'MaterialManagement/Photographs',
                        'documents' : 'MaterialManagement/Documents',
                        'approvals' : 'MaterialManagement/Approvals',
                        'materialStoragePhotograph' : 'MaterialManagement/StoragePhotograph',
                        }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    material_data =serializer.save(location=location , storageLocation = storageLocation , user = request.user, **file_mapping)

                    data = MaterialSourcingViewserializer(material_data).data
                    return Response({'status': 'success' ,
                                        'Message' : 'data saved successfully',
                                        'data' : data }, status = 200)
                else:
                    key, value =list(serializer.errors.items())[0]
                    error_message = str(key)+" ," + str(value[0])
                    return Response({'status': 'error',
                                    'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
            else:
                return  Response({'Message' : "Only consultant and Contractor can fill this form"}, status= status.HTTP_401_UNAUTHORIZED)


class materialmanagemantUpdate(generics.UpdateAPIView):
    serializer_class = MaterialManagmentSerializer
    # renderer_classes = [ErrorRenderer]
    parser_classes = [MultiPartParser]
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
            return Response({'message':'invalid package'}, status=status.HTTP_400_BAD_REQUEST)


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



# class GetAPI(generics.GenericAPIView):
#     serializer_class = GetAQISerializer
#     def get(self, request,packages, *args, **kwargs):
#         air_parameters = Air.objects.all()
#         if instance:
#             serializer = AirmanagementSerializer(instance, many=True)
#             return Response({'status': 200, 'data': serializer.data,
#                                       'message': 'successfully'})
#         else:
#             return Response({'status': 403, 'message': 'invalid package'})


class NoiseWhithinLimitAPI(generics.GenericAPIView):
    serializer_class = NoisemanagementSerializer
    parser_classes = [MultiPartParser]
    def post(self, request, *args, **kwargs):
        # typeOfArea = self.request.query_params.get("typeOfArea")
        # noiseLevel_day = float(self.request.query_params.get("noiseLevel_day"))
        # noiseLevel_night = float(self.request.query_params.get("noiseLevel_night"))
        # print(typeOfArea, noiseLevel_day, noiseLevel_night)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            typeOfArea = str(serializer.validated_data['typeOfArea'])
            noiseLevel_day = float(serializer.validated_data['noiseLevel_day'])
            noiseLevel_night = float(serializer.validated_data['noiseLevel_night'])
            print(typeOfArea, noiseLevel_day, noiseLevel_night)


            isWhithinLimit = {"day": "initial",
            "night": "initial"}
            # type of areas are below
            # typeOfAreaList = ["Industrial Area", "Commercial Area", "Residential Area", "Residential Area"]

            if typeOfArea == "Industrial Area":
                isWhithinLimit['day'] = "Out of Limit" if noiseLevel_day > 75 else "Whithin Limit"
                isWhithinLimit['night'] = "Out of Limit" if noiseLevel_night > 70 else "Whithin Limit"
            if typeOfArea == "Commercial Area":
                isWhithinLimit['day'] = "Out of Limit" if noiseLevel_day > 65 else "Whithin Limit"
                isWhithinLimit['night'] = "Out of Limit" if noiseLevel_night > 55 else "Whithin Limit"
            if typeOfArea == "Residential Area":
                isWhithinLimit['day'] = "Out of Limit" if noiseLevel_day > 55 else "Whithin Limit"
                isWhithinLimit['night'] = "Out of Limit" if noiseLevel_night > 45 else "Whithin Limit"
            if typeOfArea == "Sensitive Area":
                isWhithinLimit['day'] = "Out of Limit" if noiseLevel_day > 50 else "Whithin Limit"
                isWhithinLimit['night'] = "Out of Limit" if noiseLevel_night > 40 else "Whithin Limit"

            print(isWhithinLimit)

            return Response({'status': 200, 'data': isWhithinLimit,
                                        'message': 'successfully'})
        else:
            error = error_simplifier(serializer.errors)
            return Response({
                "message":error,
                "status":"error"
            },status=status.HTTP_400_BAD_REQUEST)


class GenerateWQI(generics.GenericAPIView):
    serializer_class = GenerateWQISerializer
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    
    # working but message is giving 1 field missing not all missing field at once, need to improve
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
          
            pH_WiQi = get_pH_WiQI((serializer.validated_data['pH']))
            totalHardnessAsCaCO3_WiQi = get_totalHardnessAsCaCO3_WiQI((serializer.validated_data['totalHardnessAsCaCO3']))
            calcium_WiQi = get_calcium_WiQI((serializer.validated_data['calcium']))
            totalAlkalinityAsCaCO3_WiQi = get_totalAlkalinityAsCaCO3_WiQI((serializer.validated_data['totalAlkalinityAsCaCO3']))
            chlorides_WiQi = get_chlorides_WiQI((serializer.validated_data['chlorides']))
            magnesium_WiQi = get_magnesium_WiQI((serializer.validated_data['magnesium']))
            totalDissolvedSolids_WiQi = get_totalDissolvedSolids_WiQI((serializer.validated_data['totalDissolvedSolids']))
            sulphate_WiQi = get_sulphate_WiQI((serializer.validated_data['sulphate']))
            nitrate_WiQi = get_nitrate_WiQI((serializer.validated_data['nitrate']))
            fluoride_WiQi = get_fluoride_WiQI((serializer.validated_data['fluoride']))
            iron_WiQi = get_iron_WiQI((serializer.validated_data['iron']))


            WQI = pH_WiQi + totalHardnessAsCaCO3_WiQi + calcium_WiQi + totalAlkalinityAsCaCO3_WiQi + chlorides_WiQi + magnesium_WiQi + totalDissolvedSolids_WiQi + sulphate_WiQi + nitrate_WiQi + fluoride_WiQi + iron_WiQi

            print(pH_WiQi)
            print(totalHardnessAsCaCO3_WiQi)
            print(calcium_WiQi)
            print(totalAlkalinityAsCaCO3_WiQi)
            print(chlorides_WiQi)
            print(magnesium_WiQi)
            print(totalDissolvedSolids_WiQi)
            print(sulphate_WiQi)
            print(nitrate_WiQi)
            print(fluoride_WiQi)
            print(iron_WiQi)
        

            return Response({
                "message":"WQI generated successfully",
                "status":"success",
                "data":WQI,
            })
        else:
            error = error_simplifier(serializer.errors)
            return Response({
                "message":error,
                "status":"error"
            },status=status.HTTP_400_BAD_REQUEST)
        


def get_pH_WiQI(x):
    qi = (float(x) / 7.5) * 100
    return 0.097560 * qi


def get_totalHardnessAsCaCO3_WiQI(x):
    qi = (float(x) / 200) * 100
    return 0.04878 * qi


def get_calcium_WiQI(x):
    qi = (float(x) / 75) * 100
    return 0.04878 * qi


def get_totalAlkalinityAsCaCO3_WiQI(x):
    qi = (float(x) / 200) * 100
    return 0.0731707317073171 * qi


def get_chlorides_WiQI(x):
    qi = (float(x) / 250) * 100
    return 0.07317 * qi


def get_magnesium_WiQI(x):
    qi = (float(x) / 30) * 100
    return 0.0487804878048781 * qi


def get_totalDissolvedSolids_WiQI(x):
    qi = (float(x) / 500) * 100
    return 0.09756 * qi


def get_sulphate_WiQI(x):
    qi = (float(x) / 200) * 100
    return 0.09756 * qi


def get_nitrate_WiQI(x):
    qi = (float(x) / 45) * 100
    return 0.12195 * qi


def get_fluoride_WiQI(x):
    qi = (float(x) / 1) * 100
    return 0.09756 * qi


def get_iron_WiQI(x):
    qi = (float(x) / 0.3) * 100
    return 0.09756 * qi