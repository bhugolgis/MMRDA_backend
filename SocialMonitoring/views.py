from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser 
from rest_framework.response import Response
from .renderers import ErrorRenderer
from django.contrib.gis.geos import Point
from .models import *
from .permissions import * # need to optimize / import only that functions that are required
from .permissions import IsConsultantOrRNR # already imported in above statement, will remove the above statement if all the functions are not being used
from rest_framework import status
from rest_framework import filters
from Training.utils import save_multiple_files


# ---------------Labour camp Serializer for GEO jason Format--------------------------------

# The below class is a view for creating and saving labour camp details with latitude and
# longitude coordinates.
class PostlabourCampdetails(generics.GenericAPIView):
    serializer_class = labourCampDetailSerializer
    parser_classes = (MultiPartParser, )
    permission_classes = [IsAuthenticated]
    queryset = labourcampDetails.objects.all()

    def post(self, request):
        """
        The above function is a POST request handler that saves data to a labour camp detail serializer
        and returns a response with the saved data or an error message.
        """
        try:
            serializer = labourCampDetailSerializer(data=request.data)
            if serializer.is_valid():
                lat = float(serializer.validated_data['latitude'])
                long = float(serializer.validated_data['longitude'])
                location = Point(long, lat, srid=4326)

                file_fields = { 'image': 'Labour Camp/LabourCamp_image' }

                file_mapping = {}
                for field, file_path in file_fields.items():
                    print(request.FILES)
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path , field)

                pap = serializer.save(location=location ,user = request.user , **file_mapping )
                data = labourCampDetailviewSerializer(pap).data
                return Response({'status': 'success',
                                'Message': 'Data saved successfully',
                                 'data': data}, status=status.HTTP_200_OK)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                'Message' :value[0]} , status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': 'failed',
                            'Message': 'Something Went Wrong'}, status=400)





# The `labourCampdetailsView` class is a generic list API view that retrieves all instances of the
# `labourcampDetails` model and serializes them using the `labourCampDetailGetviewSerializer`.
class labourCampdetailsView(generics.ListAPIView):
    queryset = labourcampDetails.objects.all()
    serializer_class = labourCampDetailGetviewSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['LabourCampName' ,'LabourCampID']


# The `labourCampdetailsViewSearch` class is a generic list API view that allows searching for labour
# camp details by the name of the labour camp.
class labourCampdetailsViewSearch(generics.ListAPIView):
    queryset = labourcampDetails.objects.all()
    serializer_class = labourCampDetailGetviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['LabourCampName']




# ---------------------------- PAP View--------------------------------------------------

# The `PapView` class is a view in a Django REST framework API that handles the creation of a PAP
# (Project Affected persons) object, with different validation and permission checks based on the
# user's group.
class PapView(generics.GenericAPIView):
    renderer_classes = [ErrorRenderer]
    parser_classes = [MultiPartParser]
    serializer_class = PapSerailzer
    permission_classes = [IsAuthenticated]
   

    def post(self, request):
        """
        The function handles the POST request for saving data, including file uploads, based on the
        user's group membership.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by
        the client. It contains information such as the request method (GET, POST, etc.), headers, user
        authentication, and the data sent in the request body
        :return: The code returns a response object with a message and status code. The specific
        response depends on the conditions in the code.
        """
        if "RNR" in request.user.groups.values_list("name", flat=True):
            serializer = self.get_serializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                papid = serializer.validated_data["PAPID"]
                data = PAP.objects.filter(PAPID=papid).exists()
                if data == True:
                    return Response({'Message': 'already data filled for this PAP-ID',
                                    'status' : 'success',
                                    }, status=400)
                else:
                    lat = float(serializer.validated_data['latitude'])
                    long = float(serializer.validated_data['longitude'])
                    location = Point(long, lat, srid=4326)

    
                    file_fields = {
                        'cadastralMapDocuments': 'PAP/PAP_cadastralMapDocuments',
                        'legalDocuments': 'PAP/PAP_legalDocuments',
                        'presentPhotograph': 'PAP/presentphotograph' , 
                        'documents': 'PAP/documents' , }
                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)
                    pap = serializer.save(location=location, user=request.user , **file_mapping)

                    data = papviewserialzer(pap).data
                    print(request.data)
                    return Response ({'Message': 'data saved successfully',
                                    'status' : 'success' , 
                                    'data': data
                                    }, status=200)
            else:    
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                print(error_message)
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
            
        elif "consultant" in request.user.groups.values_list("name" , flat = True):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                lat = float(serializer.validated_data['latitude'])
                long = float(serializer.validated_data['longitude'])
                location = Point(long, lat, srid=4326)

                file_fields = {
                    'cadastralMapDocuments': 'PAP/PAP_cadastralMapDocuments',
                    'legalDocuments': 'PAP/PAP_legalDocuments',
                    'presentPhotograph': 'PAP/presentphotograph' , 
                    'documents': 'PAP/documents' , }

                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path , field)

                pap = serializer.save(location=location , user = request.user , **file_mapping)
                data = papviewserialzer(pap).data 
                print(request.data)
                return Response ({'Message': 'data saved successfully',
                                    'status' : 'success',
                                    'data': data}, status=200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = str(key)+" ,"+str(value[0])
                print(error_message)
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)

    # def get(self, request, id):
    #     try:
    #         pap = PAP.objects.get(id=id)
    #         data = papviewserialzer(pap).data
    #         data['properties']['id'] = id
    #         return Response({'status': 'success',
    #                          'data': data}, status=200)
    #     except PAP.DoesNotExist:
    #         return Response({'status': 'error',
    #                          'Message': 'PAP not found'}, status=404)
        
# PATCH
class PapGetUpdateDeleteView(generics.UpdateAPIView):
    serializer_class = PapUpdateSerailzer
    permission_classes = [IsAuthenticated, IsConsultantOrRNR]
    # parser_classes = [MultiPartParser]

    def get_object(self):
        """
        Retrieve the PAP object based on the ID and ensure it's owned by the current user.
        """
        try:
            return PAP.objects.get(id=self.kwargs['id'])
        except PAP.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the PAP instance.
        """
        # Get the object to update
        pap_instance = self.get_object()
        if not pap_instance:
            return Response({"message": "PAP data not found for user."}, status=status.HTTP_404_NOT_FOUND)
        
        # Use the serializer with the partial flag
        serializer = self.get_serializer(pap_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
         # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                pap_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle file fields
        file_fields = {
            'cadastralMapDocuments': 'PAP/PAP_cadastralMapDocuments',
            'legalDocuments': 'PAP/PAP_legalDocuments',
            'presentPhotograph': 'PAP/presentphotograph',
            'documents': 'PAP/documents',
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            if files:
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path, field)

        # Save the updated instance
        updated_pap = serializer.save(**file_mapping)
        data = self.get_serializer(updated_pap).data

        return Response({
            'Message': 'Data updated successfully',
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)

    def get(self, request, id):
        try:
            pap = PAP.objects.get(id=id)
            data = papviewserialzer(pap).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except PAP.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'PAP not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the LabourCamp instance.
        """
        pap_instance = self.get_object()
        if not pap_instance:
            return Response({'status': 'error', 'Message': 'PAP data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        pap_instance.delete()
        return Response({'status': 'success', 'Message': 'PAP deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class PapListView(generics.ListAPIView):
    serializer_class = papviewserialzer
    permission_classes = [IsAuthenticated]
    queryset = PAP.objects.all()

# This below class is view which handels takes the PAP-ID and gives the PAP singel obejct
class RehabilatedPAPIDView(generics.GenericAPIView):
    serializer_class = RehabilatedPAPIDSerializer
    #parser_classes = [MultiPartParser]

    def get(self, request, PAPID):
        """
        The function retrieves data for a given PAPID and checks if the person is agreed for
        rehabilitation, returning an appropriate response.
        
        :param request: The request object contains information about the HTTP request made by the
        client, such as the headers, body, and method
        :param PAPID: PAPID is the unique identifier for a PAP (Person Affected by Project). It is used
        to retrieve data for a specific PAP from the database
        :return: a response object. If the PAPID is not found in the database, it returns a success
        message with a status code of 200. If the person with the given PAPID is not agreed for
        rehabilitation, it returns an error message with a status code of 400. Otherwise, it returns the
        serialized data for the PAPID with a status code of 200.
        """
        """
        The function retrieves data for a given PAPID and checks if the person is agreed for
        rehabilitation, returning an appropriate response.
    
        """
        try:
            papdata = PAP.objects.get(PAPID=PAPID)
        except:
            return Response({'Message': 'No data Avaialable for this PAPID',
                            'status' : 'success'}, status=200)
        
        serializers = RehabilatedPAPIDSerializer(papdata).data
        for i in serializers.values():
            if i == "Not agreed":
                return Response ({"status": "error" , 
                              "message" : "Person with this PAP-ID is not agreed for rehabilitaion"} , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializers, status=200)
        

# ------------------------------ Rehabilitation View ------------------------------


# The `RehabilitationView` class is a view in a Django REST framework API that handles the creation of
# rehabilitation data, with different validation and permission checks based on the user's group.

class RehabilitationView(generics.GenericAPIView):
    serializer_class = RehabilitationSerializer
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        The above function is a view function in Django that handles the POST request for saving data
        related to rehabilitation, with different logic based on the user's group.
        
        :param request: The `request` parameter is an object that represents the HTTP request made by
        the client. It contains information such as the request method (GET, POST, etc.), headers, user
        authentication, and the data sent in the request body
        :return: The code is returning a response object with a message and status. The specific message
        and status depend on the conditions in the code.
        """
     
        
        if "RNR" in request.user.groups.values_list("name", flat=True):
            serializer = RehabilitationSerializer(data=request.data )
            if serializer.is_valid():
                papid = serializer.validated_data['PAPID']
                data = Rehabilitation.objects.filter(PAPID=papid).exists()
                if data == True:
                    return Response({'Message': 'already data filled for this PAP' ,
                                    'status' : 'success'})
                else:
                    lat = float(serializer.validated_data['latitude'])
                    long = float(serializer.validated_data['longitude'])
                    location = Point(long, lat, srid=4326)

                    file_fields = {
                        'photographs' : 'rehabitation/Rehabitationphotographs',
                        'documents' : 'rehabitation/documents'
                        }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    rehabilitation = serializer.save(location=location, user=request.user , **file_mapping)
                    data = RehabilitationViewSerializer(rehabilitation).data
                    return Response({'Message': 'data saved successfully',
                                    'status' : 'success',
                                    'data':data})
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)

        elif "consultant" in request.user.groups.values_list("name" , flat = True):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                lat = float(serializer.validated_data['latitude'])
                long = float(serializer.validated_data['longitude'])
                location = Point(long, lat, srid=4326)
                file_fields = {
                        'photographs' : 'rehabitation/Rehabitationphotographs',
                        'documents' : 'rehabitation/documents',
                        }

                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path , field)
                    
                rehabilitation = serializer.save(location=location , user = request.user , **file_mapping)
                data = RehabilitationViewSerializer(rehabilitation).data
                return Response({'Message': 'data saved successfully',
                                    'status' : 'success',
                                    'data':data})
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = str(key)+" ,"+str(value[0])
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)



# Rehab Edit
# Not showing all fields updated, check the return response
class RehabilitationGetUpdateDeleteView(generics.UpdateAPIView):
    serializer_class = RehabilitationGetUpdateDeleteSerializer
    permission_classes = [IsAuthenticated, IsConsultantOrRNR]

    def get_object(self):
        """
        Retrieve the Rehabilitation object based on the ID and ensure it's owned by the current user.
        """
        try:
            return Rehabilitation.objects.get(id=self.kwargs['id'])
        except Rehabilitation.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the Rehabilitation instance.
        """
        rehabilitation_instance = self.get_object()
        if not rehabilitation_instance:
            return Response({"message": "Rehabilitation data not found for user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(rehabilitation_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                rehabilitation_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle file fields
        file_fields = {
            'photographs': 'rehabitation/Rehabilitationphotographs',
            'documents': 'rehabitation/documents',
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            if files:
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path, field)

        updated_rehabilitation = serializer.save(**file_mapping)
        data = self.get_serializer(updated_rehabilitation).data

        return Response({
            'Message': 'Data updated successfully',
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)


    def get(self, request, id):
        try:
            rehab = Rehabilitation.objects.get(id=id)
            data = RehabilitationViewSerializer(rehab).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except Rehabilitation.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Rehab data not found'}, status=404)


    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the Rehab instance.
        """
        rehab_instance = self.get_object()
        if not rehab_instance:
            return Response({'status': 'error', 'Message': 'Rehab data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        rehab_instance.delete()
        return Response({'status': 'success', 'Message': 'Rehab deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# ----------------------------- Labour Camp View --------------------------------

# The `LabourCampDetailsView` class is a view in a Django REST framework API that allows authenticated
# users who are either consultants or contractors to submit data for a labour camp, with different
# validation and response logic based on the user's role.

class LabourCampView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    parser_classes = [MultiPartParser]
    serializer_class = LabourCampSerializer

    def post(self, request):
        """
        The above function is a view function in a Django REST framework API that handles the POST
        request for saving data related to a labour camp, with different logic based on the user's group
        (contractor or consultant).
    
        """
    
        if "contractor" in request.user.groups.values_list("name", flat=True):
            serializer = self.get_serializer(data=request.data )
            if serializer.is_valid():
                date = str(serializer.validated_data['dateOfMonitoringTwo']).split('-')
                quarter = serializer.validated_data['quarter']
                packages = serializer.validated_data["packages"]
                data = LabourCamp.objects.filter(quarter=quarter, dateOfMonitoring__year=int(date[0]) , packages = packages).exists()
                if data == True:
                    return Response({'Message': 'already data filled for this Quarter'}, status=400)
                else:
                    lat = float(serializer.validated_data['latitude'])
                    long = float(serializer.validated_data['longitude'])
                    location = Point(long, lat, srid=4326)

                    # The above code is defining a dictionary called `file_fields` which maps field
                    # names to file paths. It then initializes an empty dictionary called
                    # `file_mapping`.
                    file_fields = {
                        'toiletPhotograph' : 'Labour Camp/toilet_photographs' ,
                        'drinkingWaterPhotographs' : 'Labour Camp/drinkingWater_photographs',
                        'demarkationOfPathwaysPhotographs': 'Labour Camp/demarkingPathways_photographs' ,
                        'signagesLabelingPhotographs': 'Labour Camp/signagesLabeling_Photographs',
                        'kitchenAreaPhotographs': 'Labour Camp/KitchenArea _photographs' ,
                        'fireExtinguishPhotographs': 'Labour Camp/fireExtinguish_photographs' ,
                        'roomsOrDomsPhotographs': 'Labour Camp/rooms_photographs',
                        'segregationOfWastePhotographs': 'labour Camp/segrigationOfWaste_Photographs',
                        'regularHealthCheckupPhotographs': 'Labour Camp/RegularHealthCheckup_Photographs',
                        'availabilityOfDoctorPhotographs': 'Labour Camp/AvailabilityOfDoctor_photographs' ,
                        'firstAidKitPhotographs': 'Labour Camp/FirstAidKit_photographs' ,
                        'documents': 'labourcamp_documents',
                        'photographs': 'Labour Camp/GenralPhotographs' , }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    LabourCampDetails = serializer.save(location=location , user = request.user , **file_mapping)
                    data = LabourCampDetailViewSerializer(LabourCampDetails).data

                    return Response({'Message': 'data saved successfully',
                                    'status' : 'success',
                                    'data': data}, status=200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
            
        elif "consultant" in request.user.groups.values_list("name" , flat = True):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                lat = float(serializer.validated_data['latitude'])
                long = float(serializer.validated_data['longitude'])
                location = Point(long, lat, srid=4326)

                file_fields = {
                        'toiletPhotograph' : 'Labour Camp/toilet_photographs' ,
                        'drinkingWaterPhotographs' : 'Labour Camp/drinkingWater_photographs',
                        'demarkationOfPathwaysPhotographs': 'Labour Camp/demarkingPathways_photographs' ,
                        'signagesLabelingPhotographs': 'Labour Camp/signagesLabeling_Photographs',
                        'kitchenAreaPhotographs': 'Labour Camp/KitchenArea _photographs' ,
                        'fireExtinguishPhotographs': 'Labour Camp/fireExtinguish_photographs' ,
                        'roomsOrDomsPhotographs': 'Labour Camp/rooms_photographs',
                        'segregationOfWastePhotographs': 'labour Camp/segrigationOfWaste_Photographs',
                        'regularHealthCheckupPhotographs': 'Labour Camp/RegularHealthCheckup_Photographs',
                        'availabilityOfDoctorPhotographs': 'Labour Camp/AvailabilityOfDoctor_photographs' ,
                        'firstAidKitPhotographs': 'Labour Camp/FirstAidKit_photographs' ,
                        'documents': 'labourcamp_documents',
                        'photographs': 'Labour Camp/GenralPhotographs' , }


                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path , field)

                LabourCampDetails = serializer.save(location=location , user = request.user , **file_mapping)
                data = LabourCampDetailViewSerializer(LabourCampDetails).data
                return Response({'Message': 'data saved successfully',
                                    'status' : 'success',
                                    'data': data}, status=200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                'Message' :error_message
                                } , status = status.HTTP_400_BAD_REQUEST)
        else:
        # except Exception:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)

    

# PATCH API 
class LabourCampUpdateGetDeleteView(generics.UpdateAPIView):
    serializer_class = LabourCampUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    def get_object(self):
        """
        Retrieve the LabourCamp object based on the ID.
        """
        try:
            return LabourCamp.objects.get(id=self.kwargs['id'])
        except LabourCamp.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the LabourCamp instance.
        """
        labour_camp_instance = self.get_object()
        if not labour_camp_instance:
            return Response({"message": "LabourCamp data not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(labour_camp_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                labour_camp_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle file fields
        file_fields = {
            'toiletPhotograph': 'Labour Camp/toilet_photographs',
            'drinkingWaterPhotographs': 'Labour Camp/drinkingWater_photographs',
            'demarkationOfPathwaysPhotographs': 'Labour Camp/demarkingPathways_photographs',
            'signagesLabelingPhotographs': 'Labour Camp/signagesLabeling_Photographs',
            'kitchenAreaPhotographs': 'Labour Camp/KitchenArea_photographs',
            'fireExtinguishPhotographs': 'Labour Camp/fireExtinguish_photographs',
            'roomsOrDomsPhotographs': 'Labour Camp/rooms_photographs',
            'segregationOfWastePhotographs': 'Labour Camp/segrigationOfWaste_Photographs',
            'regularHealthCheckupPhotographs': 'Labour Camp/RegularHealthCheckup_Photographs',
            'availabilityOfDoctorPhotographs': 'Labour Camp/AvailabilityOfDoctor_photographs',
            'firstAidKitPhotographs': 'Labour Camp/FirstAidKit_photographs',
            'photographs': 'Labour Camp/GenralPhotographs',
            'documents': 'labourcamp_documents',
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            if files:
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path, field)

        updated_labour_camp = serializer.save(**file_mapping)
        data = self.get_serializer(updated_labour_camp).data

        return Response({
            'Message': 'Data updated successfully',
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)


    def get(self, request, id):
        try:
            labour_camp = LabourCamp.objects.get(id=id)
            data = LabourCampDetailViewSerializer(labour_camp).data
            return Response({'status': 'success',
                             'data': data}, status=200)
        except LabourCamp.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Labour camp data not found'}, status=404)


    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the LabourCamp instance.
        """
        labour_camp_instance = self.get_object()
        if not labour_camp_instance:
            return Response({'status': 'error', 'Message': 'Labour camp data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        labour_camp_instance.delete()
        return Response({'status': 'success', 'Message': 'Labour camp deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# ------------------------------------ Construction site View -----------------------------------------------------


# The `constructionSiteView` class is a view in a Django REST framework API that handles the creation
# of construction site data, with different validation and permission checks based on the user's role.

class constructionSiteView(generics.GenericAPIView):
    renderer_classes = [ErrorRenderer]
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    serializer_class = constructionSiteSerializer

    def post(self, request):
        """
        The above function is a view function in Django that handles the POST request for saving
        construction site data, with different logic based on the user's group (contractor or
        consultant).
        
        """
        if "contractor" in request.user.groups.values_list("name", flat=True):
            serialzier = constructionSiteSerializer( data=request.data, context={'request': request})
            if serialzier.is_valid():
                constructionSiteId = serialzier.validated_data['constructionSiteId']
                constructionSiteName = serialzier.validated_data['constructionSiteName']
                data = ConstructionSiteDetails.objects.filter(constructionSiteId = constructionSiteId, constructionSiteName=constructionSiteName).exists()
                if data == True:
                    return Response({'message': 'already data filled for this Construction Site',
                                    'status': 'success'}, status=400)
                else:
                    lat = float(serialzier.validated_data['latitude'])
                    long = float(serialzier.validated_data['longitude'])
                    location = Point(long, lat, srid=4326)

                    file_fields = {
                        'demarkationOfPathwaysPhotographs' : 'constructionSite/demarkingPathways_photographs' ,
                        'signagesLabelingPhotographs' : 'constructionSite/signagesLabeling_Photographs' ,
                        'regularHealthCheckupPhotographs' : 'constructionSite/RegularHealthCheckup_Photographs' ,
                        'availabilityOfDoctorPhotographs' : 'constructionSite/AvailabilityOfDoctor_photographs' ,
                        'firstAidKitPhotographs' :  'constructionSite/FirstAidKit_photographs' ,
                        'drinkingWaterPhotographs' : 'constructionSite/drinkingWater_photographs' ,
                        'toiletPhotograph' : 'constructionSite/toilet_photographs' ,
                        'documents': 'constructionSite/documents', 
                        'genralphotographs': 'constructionSite/genral_photograph' , }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)

                    construction = serialzier.save(location=location , user = request.user , **file_mapping)
                    data = ConstructionSiteDetailsViewSerializer(construction).data
                    return  Response({'Message': 'data saved successfully',
                                'status' : 'success',
                                'data': data}, status=200)
            else:
                key, value =list(serialzier.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
            
        elif "consultant" in request.user.groups.values_list("name", flat=True):
            serialzier = constructionSiteSerializer( data=request.data, context={'request': request})
            if serialzier.is_valid(raise_exception=True):
                lat = float(serialzier.validated_data['latitude'])
                long = float(serialzier.validated_data['longitude'])
                location = Point(long, lat, srid=4326)

                file_fields = {
                        'demarkationOfPathwaysPhotographs' : 'constructionSite/demarkingPathways_photographs' ,
                        'signagesLabelingPhotographs' : 'constructionSite/signagesLabeling_Photographs' ,
                        'regularHealthCheckupPhotographs' : 'constructionSite/RegularHealthCheckup_Photographs' ,
                        'availabilityOfDoctorPhotographs' : 'constructionSite/AvailabilityOfDoctor_photographs' ,
                        'firstAidKitPhotographs' :  'constructionSite/FirstAidKit_photographs' ,
                        'drinkingWaterPhotographs' : 'constructionSite/drinkingWater_photographs' ,
                        'toiletPhotograph' : 'constructionSite/toilet_photographs' ,
                        'documents': 'constructionSite/documents', 
                        'genralphotographs': 'constructionSite/genral_photograph' , }

                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path , field)

                construction = serialzier.save(location=location , user = request.user , **file_mapping )
                data = ConstructionSiteDetailsViewSerializer(construction).data
                return  Response({'Message': 'data saved successfully',
                                    'status' : 'success',
                                    'data': data}, status=200)
            else:
                key, value =list(serialzier.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                    'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)


# The ConstructionSiteUpdateView class is a view in a Python Django application that handles updating construction site data.
class ConstructionSiteGetUpdateDeleteView(generics.UpdateAPIView):
    serializer_class = ConstructionSiteUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    def get_object(self):
        """
        Retrieve the ConstructionSiteDetails object based on the ID.
        """
        try:
            return ConstructionSiteDetails.objects.get(id=self.kwargs['id'])
        except ConstructionSiteDetails.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the ConstructionSiteDetails instance.
        """
        construction_site_instance = self.get_object()
        if not construction_site_instance:
            return Response({"message": "Construction Site data not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(construction_site_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle latitude and longitude to update location
        lat = request.data.get('latitude')
        long = request.data.get('longitude')
        if lat and long:
            try:
                location = Point(float(long), float(lat), srid=4326)
                construction_site_instance.location = location
            except (ValueError, TypeError):
                return Response({"message": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle file fields
        file_fields = {
            'demarkationOfPathwaysPhotographs': 'constructionSite/demarkingPathways_photographs',
            'signagesLabelingPhotographs': 'constructionSite/signagesLabeling_Photographs',
            'regularHealthCheckupPhotographs': 'constructionSite/RegularHealthCheckup_Photographs',
            'availabilityOfDoctorPhotographs': 'constructionSite/AvailabilityOfDoctor_photographs',
            'firstAidKitPhotographs': 'constructionSite/FirstAidKit_photographs',
            'drinkingWaterPhotographs': 'constructionSite/drinkingWater_photographs',
            'toiletPhotograph': 'constructionSite/toilet_photographs',
            'documents': 'constructionSite/documents',
            'genralphotographs': 'constructionSite/genral_photograph',
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            files = request.FILES.getlist(field)
            if files:
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path, field)

        updated_construction_site = serializer.save(**file_mapping)
        data = ConstructionSiteDetailsViewSerializer(updated_construction_site).data

        return Response({
            'Message': 'Data updated successfully',
            'status': 'success',
            'data': data
        }, status=status.HTTP_200_OK)


    def get(self, request, id):
        try:
            construction_site = ConstructionSiteDetails.objects.get(id=id)
            data = ConstructionSiteDetailsserializer(construction_site).data
            return Response({'status': 'success',
                             'data': data}, status=200)
        except ConstructionSiteDetails.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Construction camp data not found'}, status=404)


    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the LabourCamp instance.
        """
        construction_site_instance = self.get_object()
        if not construction_site_instance:
            return Response({'status': 'error', 'Message': 'Construction camp data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        construction_site_instance.delete()
        return Response({'status': 'success', 'Message': 'Construction camp deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# The ConstructionSiteListView class is a generic ListAPIView that uses the constructionSiteSerializer
# to serialize the queryset of ConstructionSiteDetails objects.
class ConstructionSiteListView(generics.ListAPIView):
    serializer_class = constructionSiteSerializer
    queryset = ConstructionSiteDetails.objects.all()


