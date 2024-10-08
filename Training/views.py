from rest_framework import generics
from .serialzers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.response import Response
from django.contrib.gis.geos import Point 
from .models import *
from .models import traning, photographs
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
    parser_classes = [MultiPartParser]

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
                        'documents': 'training/documents',
                        'photographs': 'training/photographs' ,}

            file_mapping = {}
            for field, file_path in file_fields.items():
                files = request.FILES.getlist(field)
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path , field)

            training_instance = serializer.save(location = location , user = request.user , **file_mapping)
            data = TrainingViewSerializer(training_instance).data
            
            return Response({'status': 'success',
                                        'message' : 'data saved successfully',
                                        'data' : data
                                        }, status= status.HTTP_200_OK)
        else:
            key, value =list(serializer.errors.items())[0]
            error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : error_message} , status = status.HTTP_400_BAD_REQUEST)


# GET UPDATE DELETE (PATCH) API
class TrainingGetUpdateDeleteView(generics.UpdateAPIView):
    serializer_class = TrainingUpdateSerializer
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]
    parser_classes = [MultiPartParser]

    def get_object(self):
        try:
            return traning.objects.get(id=self.kwargs['id'])
        except traning.DoesNotExist:
            return None

    def get(self, request, id):
        try:
            training_instance = traning.objects.get(id=id)
            data = TrainingViewSerializer(training_instance).data
            return Response({'status': 'success',
                             'data': data}, status=200)
        except traning.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Training data not found'}, status=404)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({'status': 'error', 'message': 'Instance not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Handle coordinates if provided
        if 'latitude' in request.data and 'longitude' in request.data:
            lat = float(request.data['latitude'])
            long = float(request.data['longitude'])
            instance.location = Point(long, lat, srid=4326)

        # Handle file fields - only update fields provided in the request
        file_fields = {
            'photographs': 'training/photographs',
            'documents': 'training/documents'
        }

        file_mapping = {}
        for field, file_path in file_fields.items():
            if field in request.FILES:
                # Clear previous value of the field (i.e., replace with new files)
                files = request.FILES.getlist(field)
                file_mapping[field] = []  # Clear existing files
                save_multiple_files(files, file_mapping, file_path, field)
            else:
                # Keep the existing files unchanged if not provided in the request
                file_mapping[field] = getattr(instance, field)

        # Save updated instance with new files or existing files
        updated_instance = serializer.save(**file_mapping)
        data = TrainingUpdateSerializer(updated_instance).data

        return Response({'status': 'success', 'message': 'Data updated successfully', 'data': data}, status=status.HTTP_200_OK)




    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the Rehab instance.
        """
        training_instance = self.get_object()
        if not training_instance:
            return Response({'status': 'error', 'Message': 'training data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        training_instance.delete()
        return Response({'status': 'success', 'Message': 'Air deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

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

# No authorization or contractor or consultant?
class occupationalHealthSafetyView(generics.GenericAPIView):
    serializer_class = occupationalHealthSafetySerialziers
    parser_classes = [MultiPartParser]
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
                        'documents': 'OHS/Occupational_Wellness/Documents',
                        'photographs': 'OHS/Occupational_Wellness/Photographs' ,}

            file_mapping = {}
            for field, file_path in file_fields.items():
                files = request.FILES.getlist(field)
                file_mapping[field] = []
                save_multiple_files(files, file_mapping, file_path , field)

            data = serializer.save(location=location, user = request.user , **file_mapping)
            data = occupationalHealthSafetyViewSerializer(data).data
            return Response({'status' : 'success',
                             'Message' : 'Data Saved Successfully',
                             'data': data}, status=200)
        else:
            key, value =list(serializer.errors.items())[0]
            # error_message = key+" ,"+ value[0]
            return Response({'status': 'error',
                            'Message' : value[0],
                            'data': data} , status = status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        try:
            ohs = occupationalHealthSafety.objects.get(id=id)
            data = occupationalHealthSafetyViewSerializer(ohs).data
            return Response({'status': 'success',
                             'data': data}, status=200)
        except occupationalHealthSafety.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Occupation Health and Safety data not found'}, status=404)


# GET PATCH DELTE API
class OccupationalWellnessGetUpdateDeleteView(generics.UpdateAPIView):
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
            'documents': 'OHS/Occupational_Wellness/Documents',
            'photographs': 'OHS/Occupational_Wellness/Photographs',
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


    def get(self, request, id):
        try:
            occupational_wellness = occupationalHealthSafety.objects.get(id=id)
            data = occupationalHealthSafetyViewSerializer(occupational_wellness).data
            data['properties']['id'] = id
            return Response({'status': 'success',
                             'data': data}, status=200)
        except occupationalHealthSafety.DoesNotExist:
            return Response({'status': 'error',
                             'message': 'Occupational Wellness data not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the Rehab instance.
        """
        occupational_wellness_instance = self.get_object()
        if not occupational_wellness_instance:
            return Response({'status': 'error', 'Message': 'Occupational Wellness data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        occupational_wellness_instance.delete()
        return Response({'status': 'success', 'Message': 'Air deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


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
    serializer_class = PreConstructionStageComplianceSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    # check or reconfirm weather we want to capture date of monitoring field for compliance(pre const and const)
    def post(self, request):
        if "contractor" in request.user.groups.values_list("name", flat=True):
            serializer = PreConstructionStageComplianceSerializer(data=request.data)
            if serializer.is_valid():
                # packages = serializer.validated_data['packages']
                # data = PreConstructionStage.objects.filter(  packages = packages ).exists()
                
                file_fields = {
                    'ShiftingofUtilitiesDocuments': 'env_monitoring/compliance/pre_construction',
                    'PermissionForFellingOfTreesDocuments': 'env_monitoring/compliance/pre_construction',
                    'CRZClearanceDocuments': 'env_monitoring/compliance/pre_construction',
                    'ForestClearanceDocuments': 'env_monitoring/compliance/pre_construction',
                }

                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path, field)

                compliance_details = serializer.save(user=request.user, **file_mapping)
                data = PreConstructionStageComplianceViewSerializer(compliance_details).data

                return Response({'Message': 'Data saved successfully', 'status': 'success', 'data': data}, status=200)
            else:
                key, value = list(serializer.errors.items())[0]
                error_message = key + " ," + value[0]
                return Response({'status': 'error', 'Message': error_message}, status=status.HTTP_400_BAD_REQUEST)

        elif "consultant" in request.user.groups.values_list("name", flat=True):
            serializer = PreConstructionStageComplianceSerializer(data=request.data)
            if serializer.is_valid():
                file_fields = {
                    'ShiftingofUtilitiesDocuments': 'env_monitoring/compliance/pre_construction/shifting_of_utilities_documents',
                    'PermissionForFellingOfTreesDocuments': 'env_monitoring/compliance/pre_construction/permission_for_felling_of_trees_documents',
                    'CRZClearanceDocuments': 'env_monitoring/compliance/pre_construction/CRZ_clearance_documents',
                    'ForestClearanceDocuments': 'env_monitoring/compliance/pre_construction/forest_clearance_documents',
                }

                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path, field)

                compliance_details = serializer.save(user=request.user, **file_mapping)
                data = PreConstructionStageComplianceViewSerializer(compliance_details).data
                
                return Response({'Message': 'Data saved successfully', 'status': 'success', 'data': data}, status=200)
            else:
                key, value = list(serializer.errors.items())[0]
                error_message = key + " ," + value[0]
                return Response({'status': 'error', 'Message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)


# Get Update Delete(PATCH)
class PreConstructionStageComplianceGetUpdateDeleteView(generics.GenericAPIView):
    serializer_class = PreConstructionStageComplianceSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    def get_object(self):
        """
        Retrieve the PreConstructionStage object based on the ID.
        """
        try:
            return PreConstructionStage.objects.get(id=self.kwargs['id'])
        except PreConstructionStage.DoesNotExist:
            return None


    def get(self, request, id):
        try:
            pre_construction_stage = PreConstructionStage.objects.get(id=id)
            data = PreConstructionStageComplianceViewSerializer(pre_construction_stage).data
            return Response({'status': 'success',
                             'data': data}, status=200)
        except PreConstructionStage.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Pre construction stage data not found'}, status=404)


    def patch(self, request, *args, **kwargs):
        pre_construction_stage = self.get_object()
        if not pre_construction_stage:
            return Response({'status': 'error', 'Message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(pre_construction_stage, data=request.data, partial=True)
        if serializer.is_valid():
            file_fields = {
                'ShiftingofUtilitiesDocuments': 'env_monitoring/compliance/pre_construction/shifting_of_utilities_documents',
                'PermissionForFellingOfTreesDocuments': 'env_monitoring/compliance/pre_construction/permission_for_felling_of_trees_documents',
                'CRZClearanceDocuments': 'env_monitoring/compliance/pre_construction/CRZ_clearance_documents',
                'ForestClearanceDocuments': 'env_monitoring/compliance/pre_construction/forest_clearance_documents',
            }

            file_mapping = {}
            for field, file_path in file_fields.items():
                #if field in request.FILES:
                    files = request.FILES.getlist(field)
                    if files:
                        file_mapping[field] = []
                        save_multiple_files(files, file_mapping, file_path, field)

            compliance_details = serializer.save(**file_mapping)
            data = PreConstructionStageComplianceSerializer(compliance_details).data

            return Response({'Message': 'Data updated successfully', 'status': 'success', 'data': data}, status=200)
        else:
            key, value = list(serializer.errors.items())[0]
            error_message = key + " ," + value[0]
            return Response({'status': 'error',
                             'Message': error_message,
                             'data': data}
                            , status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the LabourCamp instance.
        """
        pre_construction_stage= self.get_object()
        if not pre_construction_stage:
             return Response({'status': 'error', 'Message': 'Pre Construction Stage data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        pre_construction_stage.delete()
        return Response({'status': 'success', 'Message': 'Pre Construction Stage data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    

# The serializer_class attribute of the ConstructionStageComplainceView class is set to the ConstructionStageComplainceSerializer class. This class is used to serialize and deserialize the data submitted by the user.
# The permission_classes attribute of the ConstructionStageComplainceView class is set to the IsAuthenticated class. This class ensures that only authenticated users can use the view.
# The post() method of the ConstructionStageComplainceView class first validates the data submitted by the user.
# If the data is valid, the method then saves the record to the database and returns a success message. Otherwise, the view returns an error message.
class ConstructionStageComplainceView(generics.GenericAPIView):
    serializer_class = ConstructionStageComplianceSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    # check or reconfirm weather we want to capture date of monitoring field for compliance(pre const and const)
    def post(self, request):
        if "contractor" in request.user.groups.values_list("name", flat=True) or "consultant" in request.user.groups.values_list("name", flat=True):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # if 'packages' not in serializer.validated_data:
                #     return Response({'status': 'error', 'Message': 'Packages field is missing'}, status=status.HTTP_400_BAD_REQUEST)

                file_fields = {
                    'ConsenttToEstablishOoperateDocuments': 'env_monitoring/compliance/construction/consent_to_establish_operate_documents',
                    'PermissionForSandMiningFromRiverbedDocuments': 'env_monitoring/compliance/construction/permission_for_sand_mining_from_riverbed_documents',
                    'PermissionForGroundWaterWithdrawalDocuments': 'env_monitoring/compliance/construction/permission_for_ground_water_withdrawal_documents',
                    'AuthorizationForCollectionDisposalManagementDocuments': 'env_monitoring/compliance/construction/authorization_for_collection_disposal_management_documents',
                    'AuthorizationForSolidWasteDocuments': 'env_monitoring/compliance/construction/authorization_for_solid_waste_documents',
                    'DisposalOfBituminousAndOtherWasteDocuments': 'env_monitoring/compliance/construction/disposal_of_bituminous_and_other_waste_documents',
                    'ConsentToDisposalOfsewagefromLabourCampsDocuments': 'env_monitoring/compliance/construction/consent_to_disposal_of_sewage_from_labour_camps_documents',
                    'PollutionUnderControlCertificateDocuments': 'env_monitoring/compliance/construction/pollution_under_control_certificate_documents',
                    'RoofTopRainWaterHarvestingDocuments': 'env_monitoring/compliance/construction/roof_top_rain_water_harvesting_documents',
                }

                file_mapping = {}
                for field, file_path in file_fields.items():
                    files = request.FILES.getlist(field)
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path, field)

                compliance_details = serializer.save(user=request.user, **file_mapping)
                data = ConstructionStageComplianceViewSerializer(compliance_details).data

                return Response({'Message': 'Data saved successfully', 'status': 'success', 'data': data}, status=200)
            else:
                key, value = list(serializer.errors.items())[0]
                error_message = key + " ," + value[0]
                return Response({'status': 'error', 'Message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"msg": "Only consultant and contractor can fill this form"}, status=401)


# Update (PATCH)
class ConstructionStageComplianceGetUpdateDeleteView(generics.GenericAPIView):
    serializer_class = ConstructionStageComplianceSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated & (IsConsultant | IsContractor)]

    def get_object(self):
        """
        Retrieve the ConstructionStage object based on the ID.
        """
        try:
            return ConstructionStage.objects.get(id=self.kwargs['id'])
        except ConstructionStage.DoesNotExist:
            return None

    def get(self, request, id):
        try:
            construction_stage = ConstructionStage.objects.get(id=id)
            data = ConstructionStageComplianceViewSerializer(construction_stage).data
            return Response({'status': 'success',
                             'data': data}, status=200)
        except ConstructionStage.DoesNotExist:
            return Response({'status': 'error',
                             'Message': 'Construction Stage data not found'}, status=404)

    def patch(self, request, *args, **kwargs):
        construction_stage_instance = self.get_object()
        if not construction_stage_instance:
            return Response({'status': 'error', 'Message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(construction_stage_instance, data=request.data, partial=True)
        if serializer.is_valid():
            file_fields = {
                'ConsenttToEstablishOoperateDocuments': 'env_monitoring/compliance/construction/consent_to_establish_operate_documents',
                'PermissionForSandMiningFromRiverbedDocuments': 'env_monitoring/compliance/construction/permission_for_sand_mining_from_riverbed_documents',
                'PermissionForGroundWaterWithdrawalDocuments': 'env_monitoring/compliance/construction/permission_for_ground_water_withdrawal_documents',
                'AuthorizationForCollectionDisposalManagementDocuments': 'env_monitoring/compliance/construction/authorization_for_collection_disposal_management_documents',
                'AuthorizationForSolidWasteDocuments': 'env_monitoring/compliance/construction/authorization_for_solid_waste_documents',
                'DisposalOfBituminousAndOtherWasteDocuments': 'env_monitoring/compliance/construction/disposal_of_bituminous_and_other_waste_documents',
                'ConsentToDisposalOfsewagefromLabourCampsDocuments': 'env_monitoring/compliance/construction/consent_to_disposal_of_sewage_from_labour_camps_documents',
                'PollutionUnderControlCertificateDocuments': 'env_monitoring/compliance/construction/pollution_under_control_certificate_documents',
                'RoofTopRainWaterHarvestingDocuments': 'env_monitoring/compliance/construction/roof_top_rain_water_harvesting_documents',
            }

            file_mapping = {}
            for field, file_path in file_fields.items():
                files = request.FILES.getlist(field)
                if files:
                    file_mapping[field] = []
                    save_multiple_files(files, file_mapping, file_path, field)

            serializer.save(**file_mapping)
            return Response({'Message': 'Data updated successfully', 'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            key, value = list(serializer.errors.items())[0]
            error_message = key + " ," + value[0]
            return Response({'status': 'error', 'Message': error_message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests for deleting the LabourCamp instance.
        """
        construction_stage= self.get_object()
        if not construction_stage:
             return Response({'status': 'error', 'Message': 'Construction Stage data not found'}, status=status.HTTP_404_NOT_FOUND)
        
        construction_stage.delete()
        return Response({'status': 'success', 'Message': 'Construction Stage data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)