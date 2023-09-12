from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser 
from rest_framework.response import Response
from .renderers import ErrorRenderer
from django.contrib.gis.geos import Point
from .models import *
from .permissions import *
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
                                    'status' : 'success'}, status=400)
                else:
                    lat = float(serializer.validated_data['latitude'])
                    long = float(serializer.validated_data['longitude'])
                    location = Point(long, lat, srid=4326)

    
                    file_fields = {
                        'legalDocuments': 'PAP/PAP_legalDocuments',
                        'presentPhotograph': 'PAP/presentphotograph' , }

                    file_mapping = {}
                    for field, file_path in file_fields.items():
                        files = request.FILES.getlist(field)
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path , field)
                    pap = serializer.save(location=location, user=request.user , **file_mapping)

                    data = papviewserialzer(pap).data
                    return Response ({'Message': 'data saved successfully',
                                    'status' : 'success' , 
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
                        'legalDocuments': 'PAP/PAP_legalDocuments',
                        'presentPhotograph': 'PAP/presentphotograph' }

                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path , field)

                pap = serializer.save(location=location , user = request.user , **file_mapping)
                data = papviewserialzer(pap).data 
                return Response ({'Message': 'data saved successfully',
                                    'status' : 'success'}, status=200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                print(error_message)
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)

    
# The `papupdateView` class is a view in a Django REST framework API that handles updating a PAP
# object with partial data.
class papupdateView(generics.UpdateAPIView):
    serializer_class = PapUpdateSerialzier
    renderer_classes = [ErrorRenderer]
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def update(self, request, id,  **kwargs):
        """
        The function updates a PAP object with the given ID and user ID, using the provided request data
        and a serializer.
        
        """
        try:
            instance = PAP.objects.get(PAPID=id, user=request.user.id)
        except Exception:
            return Response({"message": "There is no PAP data for user %s" % (request.user.username)})

        serializer = PapUpdateSerialzier(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"Message": "Please Enter a valid data"})


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
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

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
                        'livelihoodSupportPhotograph': 'rehabitation/livelihoodSupportPhotograph',
                        'trainingPhotograph': 'rehabitation/trainingPhotograph' ,
                        'tenamentsPhotograph' : 'rehabitation/tenamentsPhotograph',
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
                                    'status' : 'success'})
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
                        'livelihoodSupportPhotograph': 'rehabitation/livelihoodSupportPhotograph',
                        'trainingPhotograph': 'rehabitation/trainingPhotograph' ,
                        'tenamentsPhotograph' : 'rehabitation/tenamentsPhotograph',
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
                                    'status' : 'success'})
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)


# ----------------------------- Labour Camp details View --------------------------------

# The `LabourCampDetailsView` class is a view in a Django REST framework API that allows authenticated
# users who are either consultants or contractors to submit data for a labour camp, with different
# validation and response logic based on the user's role.

class LabourCampDetailsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    # parser_classes = [MultiPartParser]
    serializer_class = LabourCampDetailSerializer

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
                                    'status' : 'success'}, status=200)
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
                                    'status' : 'success'}, status=200)
            else:
                key, value =list(serializer.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
        # except Exception:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)


# The `labourCampUpdateView` class is a view in a Django REST framework API that allows authenticated
# consultants to update labour camp data.
class labourCampUpdateView(generics.UpdateAPIView):
    serializer_class = LabourCampUpdateSerialzier
    renderer_classes = [ErrorRenderer]
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsConsultant]

    def update(self, request, id,  **kwargs):
        try:
            instance = LabourCamp.objects.get(id=id, user=request.user.id)
        except Exception:
            return Response({"msg": "There is no labour Camp data for user %s" % (request.user.username)})

        serializer = LabourCampUpdateSerialzier(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'Message': 'data saved successfully',
                                     'status' : 'success'}, status=200)
        else:
            return Response({'Message': "Please enter a valid data",
                            'error': serializer.errors, 'Status': 'failed'} , status= 400)

# ------------------------------------ Construction site View -----------------------------------------------------


# The `constructionSiteView` class is a view in a Django REST framework API that handles the creation
# of construction site data, with different validation and permission checks based on the user's role.

class constructionSiteView(generics.GenericAPIView):
    renderer_classes = [ErrorRenderer]
    #parser_classes = [MultiPartParser]
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
                    data = ConstructionSiteDetailsViewSerializer(
                        construction).data
                    return  Response({'Message': 'data saved successfully',
                                'status' : 'success'}, status=200)
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
                data = ConstructionSiteDetailsViewSerializer(
                    construction).data
                return  Response({'Message': 'data saved successfully',
                                    'status' : 'success'}, status=200)
            else:
                key, value =list(serialzier.errors.items())[0]
                error_message = key+" ,"+value[0]
                return Response({'status': 'error',
                                    'Message' :error_message} , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)


# The ConstructionSiteUpdateView class is a view in a Python Django application that handles updating construction site data.
class ConstructionSiteUpdateView(generics.GenericAPIView):
    serializer_class = constructionSiteSerializer
    renderer_classes = [ErrorRenderer]
    #parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsConsultant]

    def update(self, request, id,  **kwargs):
        """
        The function updates a construction site record with the provided data if it exists, and returns a
        success message if the update is successful, or an error message if the data is invalid.
        
        """
        try:
            instance = ConstructionSiteDetails.objects.get(
                id=id, user=request.user.id)
        except Exception:
            return Response({"Message": "There is no Construction site data for user %s" % (request.user.username),
                            'status': 'success'} , status=200)

        serializer = constructionSiteSerializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'Message': 'data updated successfully',
                            'status' : 'success'}, status=200)
        else:
            return Response({"Message": "Please Enter a valid data" ,
                            'status' : 'failed'}, status= 400)


# The ConstructionSiteListView class is a generic ListAPIView that uses the constructionSiteSerializer
# to serialize the queryset of ConstructionSiteDetails objects.
class ConstructionSiteListView(generics.ListAPIView):
    serializer_class = constructionSiteSerializer
    queryset = ConstructionSiteDetails.objects.all()


