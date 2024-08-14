
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

    def get(self, request, id):
        try:
            air = Air.objects.get(id=id)
            data = AirViewSerializer(air).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except Air.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Air data not found'}, status=404)
            

class AirUpdateView(generics.UpdateAPIView):
    serializer_class = AirUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    queryset = Air.objects.all()

    def get_object(self):
        """
        Retrieve the Air object based on the ID and ensure it's owned by the current user.
        """
        try:
            return Air.objects.get(id=self.kwargs['id'])
        except Air.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the Air instance.
        """
        # Get the object to update
        air_instance = self.get_object()
        if not air_instance:
            return Response({"message": "Air data not found for user."}, status=status.HTTP_404_NOT_FOUND)

        # Use the serializer with the partial flag
        serializer = self.get_serializer(air_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                air_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated instance
        updated_air = serializer.save()
        data = AirViewSerializer(updated_air).data

        return Response({
            'status': 'success',
            'message': 'Data updated successfully',
            'data': data
        }, status=status.HTTP_200_OK)
        

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

    def get(self, request, id):
        try:
            water_instance = water.objects.get(id=id)
            data = waterviewserializer(water_instance).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except water.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Water data not found'}, status=404)
            

class WaterUpdateView(generics.UpdateAPIView):
    serializer_class = WaterUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    queryset = water.objects.all()

    def get_object(self):
        """
        Retrieve the Water object based on the ID and ensure it's owned by the current user.
        """
        try:
            return water.objects.get(id=self.kwargs['id'])
        except water.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the Water instance.
        """
        water_instance = self.get_object()
        print(water_instance)
        if not water_instance:
            return Response({"message": "Water data not found for user."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(water_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                water_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated instance
        updated_water = serializer.save()
        data = WaterUpdateSerializer(updated_water).data

        return Response({
            'status': 'success',
            'message': 'Data updated successfully',
            'data': data
        }, status=status.HTTP_200_OK)

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

    def get(self, request, id):
        try:
            noise = Noise.objects.get(id=id)
            data = Noiseviewserializer(noise).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except Noise.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Noise data not found'}, status=404)


class NoiseUpdateView(generics.UpdateAPIView):
    serializer_class = NoiseUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    queryset = Noise.objects.all()

    def get_object(self):
        """
        Retrieve the Noise object based on the ID.
        """
        try:
            return Noise.objects.get(id=self.kwargs['id'])
        except Noise.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the Noise instance.
        """
        # Get the object to update
        noise_instance = self.get_object()
        if not noise_instance:
            return Response({"message": "Noise data not found."}, status=status.HTTP_404_NOT_FOUND)

        # Use the serializer with the partial flag
        serializer = self.get_serializer(noise_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                noise_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated instance
        updated_noise = serializer.save()
        data = NoiseUpdateSerializer(updated_noise).data

        return Response({
            'status': 'success',
            'message': 'Data updated successfully',
            'data': data
        }, status=status.HTTP_200_OK)


class NoiseListView(generics.ListAPIView):
    pagination_class = LimitsetPagination
    serializer_class = Noiseviewserializer
    # renderer_classes = [ErrorRenderer]
    queryset = Noise.objects.all()


#check this API uncommented permission_classes
class ExistingTreeManagementView(generics.GenericAPIView):
    serializer_class = TreeManagementSerailizer
    # renderer_classes = [ErrorRenderer]
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]


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


# Get Update Delete Existing Tree

class ExistingTreeManagementGetUpdateDeleteView(generics.UpdateAPIView):
    serializer_class = TreeManagementUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    queryset = ExistingTreeManagment.objects.all()

    def get_object(self):
        """
        Retrieve the ExistingTreeManagment object based on the ID.
        """
        try:
            return ExistingTreeManagment.objects.get(id=self.kwargs['id'])
        except ExistingTreeManagment.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the ExistingTreeManagment instance.
        """
        # Get the object to update
        tree_instance = self.get_object()
        if not tree_instance:
            return Response({"message": "Tree data not found."}, status=status.HTTP_404_NOT_FOUND)

        # Use the serializer with the partial flag
        serializer = self.get_serializer(tree_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                tree_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle file fields
        file_fields = {
            'photographs': 'ExistingTreeManagement/Photographs',
            'documents': 'ExistingTreeManagement/documents'
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            file_mapping[field] = []
            save_multiple_files(files, file_mapping, file_path, field)

        # Save the updated instance
        updated_tree = serializer.save(**file_mapping)
        # serializer doesn't show all fields ideally it should show updated field
        data = TreeManagementUpdateSerializer(updated_tree).data

        return Response({
            'status': 'success',
            'message': 'Data updated successfully',
            'data': data
        }, status=status.HTTP_200_OK)

    def get(self, request, id):
        try:
            existing_tree = ExistingTreeManagment.objects.get(id=id)
            data = TreeManagmentviewserializer(existing_tree).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except ExistingTreeManagment.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Identified tree data not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the Rehab instance.
        """
        existing_tree_instance = self.get_object()
        if not existing_tree_instance:
            return Response({'status': 'error', 'Message': 'Identified tree data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        existing_tree_instance.delete()
        return Response({'status': 'success', 'Message': 'Identified tree deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


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


# New Tree Update
class NewTreeManagementGetUpdateDeleteView(generics.UpdateAPIView):
    serializer_class = NewTreeManagmentUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    queryset = NewTreeManagement.objects.all()

    def get_object(self):
        """
        Retrieve the NewTreeManagement object based on the ID.
        """
        try:
            return NewTreeManagement.objects.get(id=self.kwargs['id'])
        except NewTreeManagement.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the NewTreeManagement instance.
        """
        # Get the object to update
        tree_instance = self.get_object()
        if not tree_instance:
            return Response({"message": "Tree data not found."}, status=status.HTTP_404_NOT_FOUND)

        # Use the serializer with the partial flag
        serializer = self.get_serializer(tree_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                tree_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle file fields
        file_fields = {
            'photographs': 'NewTreeManagement/Photographs',
            'documents': 'NewTreeManagement/Documents'
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            file_mapping[field] = []
            save_multiple_files(files, file_mapping, file_path, field)

        # Save the updated instance
        updated_tree = serializer.save(**file_mapping)
        data = NewTreeManagmentUpdateSerializer(updated_tree).data

        return Response({
            'status': 'success',
            'message': 'Data updated successfully',
            'data': data
        }, status=status.HTTP_200_OK)

    def get(self, request, id):
        try:
            new_tree = NewTreeManagement.objects.get(id=id)
            data = NewTreeManagmentviewserializer(new_tree).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except NewTreeManagement.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'New tree data not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the Rehab instance.
        """
        new_tree_instance = self.get_object()
        if not new_tree_instance:
            return Response({'status': 'error', 'Message': 'New tree data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        new_tree_instance.delete()
        return Response({'status': 'success', 'Message': 'New tree deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

            
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


class WasteTreatmentsGetUpdateDeleteView(generics.UpdateAPIView):
    serializer_class = WasteTreatmentsUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    def get_object(self):
        try:
            return WasteTreatments.objects.get(id=self.kwargs['id'])
        except WasteTreatments.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle coordinates if provided
        if 'latitude' in request.data and 'longitude' in request.data:
            lat = float(request.data['latitude'])
            long = float(request.data['longitude'])
            instance.location = Point(long, lat, srid=4326)
        
        if 'waste_latitude' in request.data and 'waste_longitude' in request.data:
            waste_lat = float(request.data['waste_latitude'])
            waste_long = float(request.data['waste_longitude'])
            instance.wasteHandlingLocation = Point(waste_long, waste_lat, srid=4326)
        
        # Handle file fields
        file_fields = {
            'photographs': 'Wastetreatment/Photographs',
            'documents': 'Wastetreatment/documents',
            'GISPermitsTransportationDocuments': 'Wastetreatment/GISPermitsTransportationDocuments',
            'TransportationVechicalHasPermissionDocuments': 'Wastetreatment/TransportationVechicalHasPermissionDocuments'
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            file_mapping[field] = []
            save_multiple_files(files, file_mapping, file_path, field)

        updated_instance = serializer.save(**file_mapping)
        data = WasteTreatmentsUpdateSerializer(updated_instance).data

        return Response({'status': 'success', 'message': 'Data updated successfully', 'data': data}, status=status.HTTP_200_OK)


    def get(self, request, id):
        try:
            waste_treatment = WasteTreatments.objects.get(id=id)
            data = wastetreatmentsViewserializer(waste_treatment).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except WasteTreatments.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Waste treatment data not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the Rehab instance.
        """
        waste_instance = self.get_object()
        if not waste_instance:
            return Response({'status': 'error', 'Message': 'Waste management data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        waste_instance.delete()
        return Response({'status': 'success', 'Message': 'Waste management deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


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


class MaterialSourcingGetUpdateDeleteView(generics.UpdateAPIView):
    serializer_class = MaterialManagmentUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    def get_object(self):
        try:
            return MaterialManegmanet.objects.get(id=self.kwargs['id'])
        except MaterialManegmanet.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle coordinates if provided
        if 'latitude' in request.data and 'longitude' in request.data:
            lat = float(request.data['latitude'])
            long = float(request.data['longitude'])
            instance.location = Point(long, lat, srid=4326)
        
        if 'storageLatitude' in request.data and 'storageLongitude' in request.data:
            storagelat = float(request.data['storageLatitude'])
            storagelong = float(request.data['storageLongitude'])
            instance.storageLocation = Point(storagelong, storagelat, srid=4326)
        
        # Handle file fields
        file_fields = {
            'photographs': 'MaterialManagement/Photographs',
            'documents': 'MaterialManagement/Documents',
            'approvals': 'MaterialManagement/Approvals',
            'materialStoragePhotograph': 'MaterialManagement/StoragePhotograph',
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            file_mapping[field] = []
            save_multiple_files(files, file_mapping, file_path, field)

        updated_instance = serializer.save(**file_mapping)
        data = MaterialManagmentUpdateSerializer(updated_instance).data

        return Response({'status': 'success', 'message': 'Data updated successfully', 'data': data}, status=status.HTTP_200_OK)

    def get(self, request, id):
        try:
            material_management = MaterialManegmanet.objects.get(id=id)
            data = MaterialSourcingViewserializer(material_management).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except MaterialManegmanet.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Material management data not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the Rehab instance.
        """
        material_management_instance = self.get_object()
        if not material_management_instance:
            return Response({'status': 'error', 'Message': 'Material management data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        material_management_instance.delete()
        return Response({'status': 'success', 'Message': 'Material management deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    
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
    serializer_class = NoiseWhihinLimitSerializer
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