from rest_framework.generics import ListAPIView
from .serializers import *
from SocialMonitoring.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from Training.models import *
from openpyxl import Workbook
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.http import JsonResponse
import calendar
# from django_excel_response import ExcelResponse



''' --------------------------Labour Camp Report View----------------------------'''


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
            # previous = LabourCamp.objects.filter(packages=packages, labourCampName=labourCampName ).order_by('-id')[1:]
            previous = LabourCamp.objects.filter(packages=packages, labourCampName=labourCampName )

            if not previous:
                return JsonResponse({'status':'error','message':'Data Not Found previous'}, status=400)
           
            latest = LabourCamp.objects.filter(packages=packages, labourCampName=labourCampName).latest('id')

            if not latest:
                return JsonResponse({'status':'error','message':'Data Not Found'}, status=400 )           
            # latest_serializer = LabourcampReportSerializer(latest).data
           
            previousData = self.serializer_class(previous, many=True)
            latestData = self.serializer_class(latest)

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            'Previous': previousData.data,
                             'latest': latestData.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'Message': 'There is no data available for this Package or Quarter',
                            'status' : 'Failed'}, status=400)







class labourcampreportpackageExcelDownloadView(generics.ListAPIView):
    serializer_class = LabourcampExcelReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages', 'labourCampName']

    def get_queryset(self):
        queryset = LabourCamp.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values(
            'id','quarter', 'packages','dateOfMonitoring', 'labourCampName', 'labourCampId',
                  'isToilet', 'toiletCondition','toiletPhotograph','toiletRemarks',
                  'isDrinkingWater','drinkingWaterCondition' ,'drinkingWaterPhotographs','drinkingWaterRemarks',
                    'isDemarkationOfPathways','demarkationOfPathwaysCondition','demarkationOfPathwaysPhotographs','demarkationOfPathwaysRemark' ,
                    'isSignagesLabeling','signagesLabelingCondition' ,'signagesLabelingPhotographs','signagesLabelingRemarks',
                    'isKitchenArea','kitchenAreaCondition','kitchenAreaPhotographs','kitchenAreaRemarks',
                    'isFireExtinguish','fireExtinguishCondition','fireExtinguishPhotographs','fireExtinguishRemarks',
                     'isRoomsOrDoms' ,'roomsOrDomsCondition','roomsOrDomsPhotographs' ,'roomsOrDomsRemarks',
                     'isSegregationOfWaste','segregationOfWasteCondition','segregationOfWastePhotographs','segregationOfWasteRemarks',
                    'isRegularHealthCheckup','regularHealthCheckupCondition','regularHealthCheckupPhotographs','regularHealthCheckupRemarks',
                     'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition','availabilityOfDoctorPhotographs','availabilityOfDoctorRemarks',
                      'isFirstAidKit','firstAidKitCondition' ,'firstAidKitPhotographs','firstAidKitRemarks',
                    'transportationFacility', 'modeOfTransportation',
                    'photographs' ,'documents','remarks'
            # Add more fields as needed
        )
        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=labour_camp_report.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response
    
    
        







# The `LabourCampReportQuarterView` class is a Django view that retrieves data from the `LabourCamp`
# model based on the specified quarter, labour camp name, and year, and returns the previous and
# latest data in a response.LabourCampReportQuarterView
class LabourCampReportQuarterView(generics.ListAPIView):

    serializer_class = LabourcampReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, labourCampName, year, *args, **kwarges):
        """
        This function retrieves data from the LabourCamp model based on the specified quarter, labour
        camp name, and year, and returns the previous and latest data in a response.
        
        """
        try:
            previous = LabourCamp.objects.filter(quarter=quarter, labourCampName=labourCampName, dateOfMonitoring__year=year).order_by('-id')[1:]

            latest = LabourCamp.objects.filter( quarter=quarter, labourCampName=labourCampName , dateOfMonitoring__year=year).latest('id')
            previousData = self.serializer_class(previous, many=True).data
            latestData = self.serializer_class(latest).data

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            'Previous': previousData,
                            'latest': latestData},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available',
                            'status' : 'Failed'}, status=400)



import django_filters

class LabourCampFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')

    class Meta:
        model = LabourCamp
        fields = ['quarter', 'year', 'labourCampName']



# class labourQuarterExcelDownload(generics.ListAPIView):
class labourQuarterExcelDownload(generics.ListAPIView):
    serializer_class = LabourcampExcelReportSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'labourCampName']
    filterset_class = LabourCampFilter

    def get_queryset(self):
        queryset = LabourCamp.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values(
            'id','quarter', 'packages','dateOfMonitoring', 'labourCampName', 'labourCampId',
                  'isToilet', 'toiletCondition','toiletPhotograph','toiletRemarks',
                  'isDrinkingWater','drinkingWaterCondition' ,'drinkingWaterPhotographs','drinkingWaterRemarks',
                    'isDemarkationOfPathways','demarkationOfPathwaysCondition','demarkationOfPathwaysPhotographs','demarkationOfPathwaysRemark' ,
                    'isSignagesLabeling','signagesLabelingCondition' ,'signagesLabelingPhotographs','signagesLabelingRemarks',
                    'isKitchenArea','kitchenAreaCondition','kitchenAreaPhotographs','kitchenAreaRemarks',
                    'isFireExtinguish','fireExtinguishCondition','fireExtinguishPhotographs','fireExtinguishRemarks',
                     'isRoomsOrDoms' ,'roomsOrDomsCondition','roomsOrDomsPhotographs' ,'roomsOrDomsRemarks',
                     'isSegregationOfWaste','segregationOfWasteCondition','segregationOfWastePhotographs','segregationOfWasteRemarks',
                    'isRegularHealthCheckup','regularHealthCheckupCondition','regularHealthCheckupPhotographs','regularHealthCheckupRemarks',
                     'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition','availabilityOfDoctorPhotographs','availabilityOfDoctorRemarks',
                      'isFirstAidKit','firstAidKitCondition' ,'firstAidKitPhotographs','firstAidKitRemarks',
                    'transportationFacility', 'modeOfTransportation',
                    'photographs' ,'documents','remarks'
            # Add more fields as needed
        )
        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=labour_camp_report.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response
    

# ----------------------------------------------------------------

class ConstructionCampReportPackageView(ListAPIView):
    serializer_class = ConstructionCampReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, constructionSiteName,*args, **kwargs):
        try:
            previous = ConstructionSiteDetails.objects.filter(
                packages=packages, constructionSiteName=constructionSiteName  ).order_by('-id')[1:]
            latest = ConstructionSiteDetails.objects.filter(
                packages=packages, constructionSiteName=constructionSiteName).latest('id')
            previousData = ConstructionCampReportSerializer(previous, many=True)
            latestData = ConstructionCampReportSerializer(latest)

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            'Previous': previousData.data,
                            'latest': latestData.data},
                            status=status.HTTP_200_OK)

        except Exception:
            return Response({'Message': 'There is no data available for the Package or Quarter',
                            'status' : 'Failed'}, status=400)



class ConstructionCampReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = ConstructionCampReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages', 'constructionSiteName']
    # filterset_class = LabourCampFilter

    def get_queryset(self):
        queryset = ConstructionSiteDetails.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values(
'id','quarter', 'packages','dateOfMonitoring' ,'constructionSiteName' , 'constructionSiteId',
                    'isDemarkationOfPathways','demarkationOfPathwaysCondition','demarkationOfPathwaysPhotographs','demarkationOfPathwaysRemark' ,
                    'isSignagesLabelingCheck','signagesLabelingCondition' ,'signagesLabelingPhotographs','signagesLabelingRemarks',
                    'isRegularHealthCheckup','regularHealthCheckupCondition','regularHealthCheckupPhotographs','regularHealthCheckupRemarks',
                    'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition','availabilityOfDoctorPhotographs','availabilityOfDoctorRemarks',
                        'isFirstAidKit','firstAidKitCondition' ,'firstAidKitPhotographs','firstAidKitRemarks',
                    'isDrinkingWaterCheck','drinkingWaterCondition' ,'drinkingWaterPhotographs','drinkingWaterRemarks',
                        'isToilet', 'toiletCondition','toiletPhotograph','toiletRemarks',
                        'genralphotographs','documents','remarks'
            # Add more fields as needed
        )

        if not data:
            return Response({'status':'error','message':'Data Not Found'}, status=400)


        else:
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)


            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=ConstructionCampReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response





class ConstructionCampReportQuarterView(ListAPIView):
    serializer_class = ConstructionCampReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, constructionSiteName, year ,*args, **kwargs):
        try:
            previous = ConstructionSiteDetails.objects.filter(
                quarter=quarter, constructionSiteName=constructionSiteName ,dateOfMonitoring__year=year).order_by('-id')[1:]
            latest = latest = ConstructionSiteDetails.objects.filter(
                quarter=quarter, constructionSiteName=constructionSiteName , dateOfMonitoring__year=year).latest('id')
            previousData = ConstructionCampReportSerializer(
                previous, many=True)
            latestData = ConstructionCampReportSerializer(latest)

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            'Previous': previousData.data,
                            'latest': latestData.data},
                            status=status.HTTP_200_OK)
        except Exception:
            return Response({'Message': 'There is no data available for the Package or Quarter',
                            'status' : 'Failed'}, status=status.HTTP_400_BAD_REQUEST)




class ConstructionCampFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')

    class Meta:
        model = ConstructionSiteDetails
        fields = ['quarter', 'year', 'constructionSiteName']



class ConstructionCampReportQuaterExcelDownload(generics.ListAPIView):
    serializer_class = ConstructionCampReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = ConstructionSiteDetails.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values(
'id','quarter', 'packages','dateOfMonitoring' ,'constructionSiteName' , 'constructionSiteId',
                    'isDemarkationOfPathways','demarkationOfPathwaysCondition','demarkationOfPathwaysPhotographs','demarkationOfPathwaysRemark' ,
                    'isSignagesLabelingCheck','signagesLabelingCondition' ,'signagesLabelingPhotographs','signagesLabelingRemarks',
                    'isRegularHealthCheckup','regularHealthCheckupCondition','regularHealthCheckupPhotographs','regularHealthCheckupRemarks',
                    'isAvailabilityOfDoctor', 'availabilityOfDoctorCondition','availabilityOfDoctorPhotographs','availabilityOfDoctorRemarks',
                        'isFirstAidKit','firstAidKitCondition' ,'firstAidKitPhotographs','firstAidKitRemarks',
                    'isDrinkingWaterCheck','drinkingWaterCondition' ,'drinkingWaterPhotographs','drinkingWaterRemarks',
                        'isToilet', 'toiletCondition','toiletPhotograph','toiletRemarks',
                        'genralphotographs','documents','remarks'
            # Add more fields as needed
        )
        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=ConstructionCampReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response




# -------------------------------------------------------------------------

class PAPReportPackageView(ListAPIView):
    serializer_class = PAPReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = PAP.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)
            papdata = PAPReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "PAP": papdata},
                            status=status.HTTP_200_OK)
        except Exception:
            return Response({'Message': 'There is no data available for the Package or Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)



class PAPReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = PAPReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = PAP.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values(
            'id','quarter', 'packages','dateOfMonitoring','dateOfIdentification','PAPID','firstName','middleName','lastName', 'cadastralMapID', 'cadastralMapDocuments', 
                  'addressLine1','streetName','pincode','eligibility', 'categoryOfPap','dateOfIdentification',
                  'areaOfAsset','typeOfStructure','legalStatus','legalDocuments', 
                   'actionTaken', 'notAgreedReason','remarks', 'presentPhotograph', 'documents'
            # Add more fields as needed
        )
        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=PAPReportPackage.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response



class PAPReportQuarterView(ListAPIView):
    serializer_class = PAPReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year):
        try:
            data = PAP.objects.filter(
                quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)
            papdata = PAPReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "PAP": papdata},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package or Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)




class PAPReportExcelQuaterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')

    class Meta:
        model = PAP
        fields = ['quarter', 'year']



class PAPReportExcelQuaterExcelDownload(generics.ListAPIView):
    serializer_class = PAPReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = PAPReportExcelQuaterFilter

    def get_queryset(self):
        queryset = PAP.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values(
            'id','quarter', 'packages','dateOfMonitoring','dateOfIdentification','PAPID','firstName','middleName','lastName', 'cadastralMapID', 'cadastralMapDocuments', 
                  'addressLine1','streetName','pincode','eligibility', 'categoryOfPap','dateOfIdentification',
                  'areaOfAsset','typeOfStructure','legalStatus','legalDocuments', 
                   'actionTaken', 'notAgreedReason','remarks', 'presentPhotograph', 'documents'
            # Add more fields as needed
        )


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=PAPReportExcelQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response


# ------------------------------------------------------------
class RehabilitationReportPackageView(ListAPIView):
    serializer_class = RehabilitationReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = Rehabilitation.objects.filter(
                packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)
            Rehabilitationdata = RehabilitationReportSerializer(
                data, many=True).data

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Rehabilated_PAP_Package": Rehabilitationdata},
                            status=status.HTTP_200_OK)
        except Exception:
            return Response({'Message': 'There is no data available for the Package or Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)





class RehabilitationReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = RehabilitationReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = Rehabilitation.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('quarter','longitude', 'latitude','packages','dateOfRehabilitation' ,'PAPID',
                   'firstName', 'middleName', 'lastName', 'compensationStatus', 'agreedUpon', 'processStatus',
                   'cashCompensationAmount',
                   'typeOfCompensation', 'otherCompensationType' ,
                   'addressLine1','streetName','pincode',
                   'rehabLocation', 'allowance', 'area',
                   'landProvidedArea', 'alternateAccomodationArea', 'commercialUnitArea',
                   'isShiftingAllowance','shiftingAllowanceAmount',
                   'isLivelihoodSupport', 'livelihoodSupportAmount',
                   'isTraining','trainingRemarks', 'typeOfStructure',
                   'isRelocationAllowance' ,'RelocationAllowanceAmount' ,'isfinancialSupport',
                   'financialSupportAmount','isCommunityEngagement','isEngagementType',
                   'photographs' , 'documents','remarks')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)

        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=RehabilitationReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response




class RehabilitationReportQuarterView(ListAPIView):
    serializer_class = RehabilitationReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year, *args, **kwargs):
        try:
            data = Rehabilitation.objects.filter(
                quarter=quarter, dateOfRehabilitation__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)
            Rehabilitation_data = RehabilitationReportSerializer(
                data, many=True).data

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Rehabilated_PAP_Quarter_wise": Rehabilitation_data},
                            status=status.HTTP_200_OK)
        except Exception:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)



class RehabilitationReportQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')

    class Meta:
        model = Rehabilitation
        fields = ['quarter', 'year']



class RehabilitationReportQuarterExcelDownload(generics.ListAPIView):
    serializer_class = RehabilitationReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = RehabilitationReportQuarterFilter

    def get_queryset(self):
        queryset = Rehabilitation.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('quarter','longitude', 'latitude','packages','dateOfRehabilitation' ,'PAPID',
                   'firstName', 'middleName', 'lastName', 'compensationStatus', 'agreedUpon', 'processStatus',
                   'cashCompensationAmount',
                   'typeOfCompensation', 'otherCompensationType' ,
                   'addressLine1','streetName','pincode',
                   'rehabLocation', 'allowance', 'area',
                   'isShiftingAllowance','shiftingAllowanceAmount',
                   'isLivelihoodSupport', 'livelihoodSupportAmount',
                   'isTraining','trainingRemarks', 'typeOfStructure',
                   'isRelocationAllowance' ,'RelocationAllowanceAmount' ,'isfinancialSupport',
                   'financialSupportAmount','isCommunityEngagement','isEngagementType',
                   'photographs' , 'documents','remarks')

        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)

        else:
                
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=RehabilitationReportQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response




'''----------------------- Env Monitoring Report View------------------------------'''


class AirReportPackageView(ListAPIView):
    serializer_class = AirReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = Air.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)
            airdata = AirReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Air_data": airdata},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)




class AirReportReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = AirReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = Air.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','packages','month','dateOfMonitoring','PM10','PM2_5',
                 'SO2','NOx','CO','AQI','place_location')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)

        else:
            

            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=AirReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response





class AirReportQuarterView(ListAPIView):
    serializer_class = AirReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, month, year, *args, **kwargs):
        try:
            data = Air.objects.filter(
                month=month, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)

            airdata = AirReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Air_data": airdata},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)



class AirReportQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')
    month = django_filters.CharFilter(method='filter_by_month', label='Month')

    def filter_by_month(self, queryset, name, value):
        # if value.isdigit():
        #     # If the value is a digit, return the queryset as is
        #     return queryset

        try:
            month_number = list(calendar.month_name).index(value.capitalize())
            return queryset.filter(dateOfMonitoring__month=month_number)
        except ValueError:
            # If the value is not a valid month name, return an empty queryset
            return queryset.none()
    class Meta:
        model = Air
        fields = [ 'month','year']





class AirReportQuarterExcelDownload(generics.ListAPIView):
    serializer_class = AirReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = AirReportQuarterFilter

    def get_queryset(self):
        queryset = Air.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','packages','month','dateOfMonitoring','PM10','PM2_5',
                 'SO2','NOx','CO','AQI', 'place_location')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=AirReportQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response


class NoiseReportpackageView(ListAPIView):
    serializer_class = NoiseReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = Noise.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)

            Noise_data = NoiseReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Noise_data": Noise_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)



class NoiseReportReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = NoiseReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = Noise.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id', 'quarter','month','packages','dateOfMonitoringThree' , 'noiseLevel_day', 'noiseLevel_night', 'monitoringPeriod_day', 'monitoringPeriod_night', 'typeOfArea', 'isWithinLimit_day', 'isWithinLimit_night'  )

        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
                
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=NoiseReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response






class NoiseReportQuarterView(ListAPIView):
    serializer_class = NoiseReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, month, year, *args, **kwargs):
        try:
            data = Noise.objects.filter(
                month=month, dateOfMonitoringThree__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)

            Noise_data = NoiseReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Noise_data": Noise_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)





class NoiseReportQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoringThree__year', label='Year')
    month = django_filters.CharFilter(method='filter_by_month', label='Month')

    def filter_by_month(self, queryset, name, value):
        # if value.isdigit():
        #     # If the value is a digit, return the queryset as is
        #     return queryset

        try:
            month_number = list(calendar.month_name).index(value.capitalize())
            return queryset.filter(dateOfMonitoringThree__month=month_number)
        except ValueError:
            # If the value is not a valid month name, return an empty queryset
            return queryset.none()
    class Meta:
        model = Noise
        fields = ['month', 'year']



class NoiseReportQuarterExcelDownload(generics.ListAPIView):
    serializer_class = NoiseReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = NoiseReportQuarterFilter

    def get_queryset(self):
        queryset = Noise.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id', 'quarter','month','packages','dateOfMonitoringThree' , 'noiseLevel_day', 'noiseLevel_night', 'monitoringPeriod_day', 'monitoringPeriod_night', 'typeOfArea', 'isWithinLimit_day', 'isWithinLimit_night' )

        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        # Create a Pandas DataFrame
        else:
            
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=NoiseReportQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response



class waterReportPackageView(ListAPIView):
    serializer_class = waterReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = water.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)

            water_data = waterReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "water_data": water_data}, status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)


class waterReportReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = waterExcelReportSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = water.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','packages','month', 'dateOfMonitoringTwo','qualityOfWater' , 'sourceOfWater' , 'trueColor', 'turbidity', 'odour', 'waterDisposal', 'WQI', 'pH', 'totalHardnessAsCaCO3', 'calcium', 'totalAlkalinityAsCaCO3', 'chlorides', 'magnesium', 'totalDissolvedSolids', 'sulphate', 'nitrate', 'fluoride', 'iron', 'zinc', 'copper', 'aluminum', 'nickel', 'manganese', 'phenolicCompounds', 'sulphide', 'cadmium', 'cyanide', 'lead', 'mercury', 'totalArsenic', 'totalChromium' )


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)

        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=WaterReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response









class waterReportQuarterView(ListAPIView):
    serializer_class = waterReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, month, year, *args, **kwargs):
        # try:
            data = water.objects.filter(month=month, dateOfMonitoringTwo__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_400_BAD_REQUEST)

            water_data = waterReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "water_data": water_data},
                            status=status.HTTP_200_OK)
        # except:
        #     return Response({'Message': 'There is no data available for the Quarter',
        #                     'status' : 'Failed'},
        #                     status=status.HTTP_400_BAD_REQUEST)



class WaterReportQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoringTwo__year', label='Year')
    month = django_filters.CharFilter(method='filter_by_month', label='Month')

    def filter_by_month(self, queryset, name, value):
        # if value.isdigit():
        #     # If the value is a digit, return the queryset as is
        #     return queryset

        try:
            month_number = list(calendar.month_name).index(value.capitalize())
            return queryset.filter(dateOfMonitoringTwo__month=month_number)
        except ValueError:
            # If the value is not a valid month name, return an empty queryset
            return queryset.none()
    class Meta:
        model = water
        fields = ['month', 'year']



class WaterReportQuarterExcelDownload(generics.ListAPIView):
    serializer_class = WaterReportQuarterFilter
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = WaterReportQuarterFilter

    def get_queryset(self):
        queryset = water.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','packages','month', 'dateOfMonitoringTwo','qualityOfWater' , 'sourceOfWater' , 'trueColor', 'turbidity', 'odour', 'waterDisposal', 'WQI', 'pH', 'totalHardnessAsCaCO3', 'calcium', 'totalAlkalinityAsCaCO3', 'chlorides', 'magnesium', 'totalDissolvedSolids', 'sulphate', 'nitrate', 'fluoride', 'iron', 'zinc', 'copper', 'aluminum', 'nickel', 'manganese', 'phenolicCompounds', 'sulphide', 'cadmium', 'cyanide', 'lead', 'mercury', 'totalArsenic', 'totalChromium' )

        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
                
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=WaterReportQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response




class WasteTreatmentsPackageView(ListAPIView):
    serializer_class = wasteTreatmentsSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = WasteTreatments.objects.filter(
                packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)
            Waste_data = wasteTreatmentsSerializer(data, many=True).data

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "wasteManagementdata": Waste_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)


class wasteTreatmentReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = wasteTreatmentsExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = WasteTreatments.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','month','packages','dateOfMonitoring', 'GISPermitsTransportationDocuments', 'TransportationVechicalHasPermissionDocuments', 'wasteOilQnt', 'CCPCPaintSludgeQnt', 'filterQnt', 'airFiltersQnt', 'usedCartridgesQnt', 'plasticQnt', 'paperQnt', 'woodQnt', 'bottlesQnt', 'rubberQnt', 'bioDegradableQuantity', 'bioMedicalQuantity', 'metalScrapeQuantity', 'eWasteQuantity', 'constructionWasteQuantity', 'wasteHandlingLocation', 'photographs' , 'documents','remarks')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=wasteTreatmentReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response




class WasteTreatmentsQuarterView(ListAPIView):
    serializer_class = wasteTreatmentsSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year, *args, **kwargs):
        try:
            data = WasteTreatments.objects.filter(quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)

            Waste_data = wasteTreatmentsSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "wasteManagementData": Waste_data}, status=200)

        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'} , status=status.HTTP_400_BAD_REQUEST)




class WasteTreatmentsQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')
    quarter = django_filters.CharFilter(field_name='quarter', label='quarter')
    # month = django_filters.CharFilter(method='filter_by_month', label='Month')

    # def filter_by_month(self, queryset, name, value):
    #     # if value.isdigit():
    #     #     # If the value is a digit, return the queryset as is
    #     #     return queryset

    #     try:
    #         month_number = list(calendar.month_name).index(value.capitalize())
    #         return queryset.filter(dateOfMonitoring__month=month_number)
    #     except ValueError:
    #         # If the value is not a valid month name, return an empty queryset
    #         return queryset.none()
    class Meta:
        model = WasteTreatments
        fields = ['quarter', 'year']



class wasteTreatmentQuarterExcelDownload(generics.ListAPIView):
    serializer_class = wasteTreatmentsExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = WasteTreatmentsQuarterFilter

    def get_queryset(self):
        queryset = WasteTreatments.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','month','packages','dateOfMonitoring', 'GISPermitsTransportationDocuments', 'TransportationVechicalHasPermissionDocuments', 'wasteOilQnt', 'CCPCPaintSludgeQnt', 'filterQnt', 'airFiltersQnt', 'usedCartridgesQnt', 'plasticQnt', 'paperQnt', 'woodQnt', 'bottlesQnt', 'rubberQnt', 'bioDegradableQuantity', 'bioMedicalQuantity', 'metalScrapeQuantity', 'eWasteQuantity', 'constructionWasteQuantity', 'wasteHandlingLocation', 'photographs' , 'documents','remarks')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)

        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=WasteTreatmentQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response



class MaterialManagementReporetpackageView(ListAPIView):
    serializer_class = materialManagementSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = MaterialManegmanet.objects.filter(
                packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_400_BAD_REQUEST)

            Material_data = materialManagementSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "materialManagementData": Material_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)



class MaterialManegmanetReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = materialManagementExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = MaterialManegmanet.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','month','packages','dateOfMonitoring',
         'typeOfMaterial','source','sourceOfQuarry','materialStorageType','storageLocation',
         'materialStorageCondition','materialStoragePhotograph','approvals' ,'photographs',
          'documents','remarks')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
                
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=MaterialManagementReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response



class MaterialManagementReporetQuarterView(ListAPIView):
    serializer_class = materialManagementSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year, *args, **kwargs):
        try:
            data = MaterialManegmanet.objects.filter(
                quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_400_BAD_REQUEST)

            Material_data = materialManagementSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "materialManagementData": Material_data},
                            status=200)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)




class materialManagementQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')
    quarter = django_filters.CharFilter(field_name='quarter', label='quarter')
    # month = django_filters.CharFilter(method='filter_by_month', label='Month')

    # def filter_by_month(self, queryset, name, value):
    #     # if value.isdigit():
    #     #     # If the value is a digit, return the queryset as is
    #     #     return queryset

    #     try:
    #         month_number = list(calendar.month_name).index(value.capitalize())
    #         return queryset.filter(dateOfMonitoring__month=month_number)
    #     except ValueError:
    #         # If the value is not a valid month name, return an empty queryset
    #         return queryset.none()
    class Meta:
        model = MaterialManegmanet
        fields = ['quarter', 'year']



class materialManagementQuarterExcelDownload(generics.ListAPIView):
    serializer_class = materialManagementExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = materialManagementQuarterFilter

    def get_queryset(self):
        queryset = MaterialManegmanet.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','month','packages','dateOfMonitoring',
         'typeOfMaterial','source','sourceOfQuarry','materialStorageType','storageLocation',
         'materialStorageCondition','materialStoragePhotograph','approvals' ,'photographs',
          'documents','remarks')

        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=MaterialManegmanetQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response



class TreeMangementReportPackage(ListAPIView):
    serializer_class = treeManagementSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = ExistingTreeManagment.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)

            Material_data = treeManagementSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Tree Management data": Material_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)



class treeManagementReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = treeManagementExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = ExistingTreeManagment.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        if 'packages' not in request.GET:
            return JsonResponse({'status': 'error', 'message': 'Please provide filters'}, status=400)
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','month','dateOfMonitoring','packages','treeID','commanName' ,'botanicalName',
                    'condition', 'actionTaken', 'photographs', 'documents','remarks')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)

        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=ExistingTreeManagmentReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response


class TreeManagementReportQuarterView(ListAPIView):
    serializer_class = treeManagementSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year, *args, **kwargs):
        try:
            data = ExistingTreeManagment.objects.filter(
                quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)

            Material_data = treeManagementSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "Tree Management data": Material_data},
                            status=200)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)



class ExistingTreeManagmentQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')
    quarter = django_filters.CharFilter(field_name='quarter', label='quarter')
    # month = django_filters.CharFilter(method='filter_by_month', label='Month')

    # def filter_by_month(self, queryset, name, value):
    #     # if value.isdigit():
    #     #     # If the value is a digit, return the queryset as is
    #     #     return queryset

    #     try:
    #         month_number = list(calendar.month_name).index(value.capitalize())
    #         return queryset.filter(dateOfMonitoring__month=month_number)
    #     except ValueError:
    #         # If the value is not a valid month name, return an empty queryset
    #         return queryset.none()
    class Meta:
        model = ExistingTreeManagment
        fields = ['quarter', 'year']



class TreeManagementQuarterExcelDownload(generics.ListAPIView):
    serializer_class = treeManagementExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = ExistingTreeManagmentQuarterFilter

    def get_queryset(self):
        queryset = ExistingTreeManagment.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','month','dateOfMonitoring','packages','treeID','commanName' ,'botanicalName',
                    'condition', 'actionTaken', 'photographs', 'documents','remarks')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=TreeManegmanetQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response





class MetroLine4View(generics.GenericAPIView):
    serializer_class = MetroLine4AlignmentSerializer

    def get(self, request, *args, **kwargs):
        try:
            MetroLine = MmrdaNew.objects.all()
            serializers = self.get_serializer(MetroLine , many = True).data

            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
        except :
            return Response({'status' : 'failed',
                            'message' : 'Something went wrong !! Please try again'}, status = 400)
        

class MetroLine4AlignmentReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = MetroLine4AlignmentExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = MmrdaNew.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('id','quarter','month','dateOfMonitoring','packages','treeID','commanName' ,'botanicalName',
                    'condition', 'noOfTreeCut','actionTaken', 'photographs', 'documents','remarks')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)

        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=ExistingTreeManagmentReport.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response


class Package54AlignmentView(generics.GenericAPIView):
    serializer_class = Package54AlignmentSerializer

    def get(self, request, *args, **kwargs):
        try:
            package54 = Package54Alignment.objects.all()
            serializers = Package54AlignmentSerializer(package54 , many = True).data
            return Response({'status': 'success',
                                'message' : 'data was successfully fetched',
                                'data': serializers},
                                status= 200)
        except :
            return Response({'status' : 'failed',
                            'message' : 'Something went wrong !! Please try again'}, status = 400)
      
class package12AlignmentView(generics.GenericAPIView):
    serializer_class = Package12AlignmentSerializer 

    def get(self, request, *args, **kwargs):
        try:
            package12 = Package12Alignment.objects.all()
            serializers = Package12AlignmentSerializer(package12 , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializers},
                            status= 200)
        except :
            return Response({'status' : 'failed',
                            'message' : 'Something went wrong !! Please try again'}, status = 400)

class package11AlignmentView(generics.GenericAPIView):
    serializer_class = Package11AlignmentSerializer 

    def get(self, request, *args, **kwargs):
        try:
            package11 = Package11Alignment.objects.all()
            serializer = Package11AlignmentSerializer(package11 , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer},
                             status= 200)
        except :
            return Response({'status' : 'failed',
                            'message' : 'Something went wrong !! Please try again'}, status = 400)

class package10AlignmentView(generics.GenericAPIView):
    serializer_class = Package10AlignmentSerializer

    def get(self , request):
        try:
            package10 = Package10Alignment.objects.all()
            serializer = Package10AlignmentSerializer(package10 , many = True).data
    
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer})
        except :
            return Response({'status' : 'failed',
                            'message' : 'Something went wrong !! Please try again'})

class package09AlignmentView(generics.GenericAPIView):
    serializer_class = Package09AlignmentSerializer  

    def get(self , request):
        try:
            package09 = Package09Alignment.objects.all()
            serializer = Package09AlignmentSerializer(package09 , many = True).data
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer},
                             status= 200)
        except :
            return Response({'status' : 'failed',
                            'message' : 'Something went wrong !! Please try again'}, status = 400)

class package08AlignmentView(generics.GenericAPIView):
    serializer_class = Package08AlignmentSerializer  

    def get(self , request):
        
            package08 = Package08Alignment.objects.all()
            serializer = Package08AlignmentSerializer(package08 , many = True)
            return Response({'status': 'success',
                            'message' : 'data was successfully fetched',
                            'data': serializer.data},
                             status= 200)
        # except :
        #     return Response({'status' : 'failed',
        #                     'message' : 'Something went wrong !! Please try again'}, status = 400)

class MetroStationView(generics.GenericAPIView):
    serializer_class = MetroStationSerializer   

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

class TrainnigReportQuarterView(APIView):
    def get(self , request , quarter , year):
   
        data = traning.objects.filter(
            quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
        if not data.exists():
            return Response({'Message': 'No data found',
                                },  status=status.HTTP_400_BAD_REQUEST)
        
        training_data = TrainnigReportSerializer(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "training_data": training_data},
                            status=200)


class TrainingQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')
    month = django_filters.CharFilter(method='filter_by_month', label='Month')

    def filter_by_month(self, queryset, name, value):
        if value.isdigit():
            # If the value is a digit, return the queryset as is
            return queryset

        try:
            month_number = list(calendar.month_name).index(value.capitalize())
            return queryset.filter(dateOfMonitoring__month=month_number)
        except ValueError:
            # If the value is not a valid month name, return an empty queryset
            return queryset.none()
    class Meta:
        model = traning
        fields = ['month', 'year']



class TrainningManagementQuarterExcelDownload(generics.ListAPIView):
    serializer_class = TrainnigReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = TrainingQuarterFilter

    def get_queryset(self):
        queryset = traning.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('quarter' , 'packages' , 'dateOfMonitoring',
                  'category' , 'traningTitle' , 'noOfAttends' , 'noOfTimesTrainingConducted',
                  'male','female' , 'inchargePerson', 'traninigInitiatedBy' , 'conductDate' ,
                  'traningDate' , 'photographs' , 'documents')

        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)

        else:
                
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=TrainningQuater.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response



class TrainnigReportPackageView(APIView):
    def get(self , request , packages):
   
        data = traning.objects.filter(
            packages=packages ).order_by('-id')
        if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)
        
        training_data = TrainnigReportSerializer(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "training_data": training_data},
                            status=200)



class TrainnigReportPackageExcelDownload(generics.ListAPIView):
    serializer_class = TrainnigReportExcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = traning.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values('quarter' , 'packages' , 'dateOfMonitoring',
                  'category' , 'traningTitle' , 'noOfAttends' , 'noOfTimesTrainingConducted',
                  'male','female' , 'inchargePerson', 'traninigInitiatedBy' , 'conductDate' ,
                  'traningDate' , 'photographs' , 'documents')


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=training.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response





    
class OccupationalHealthQuarterView(generics.GenericAPIView):
    serializer_class = OccupationalHealthQuarterSeialzier
    def get(self , request , quarter , year):
        data = occupationalHealthSafety.objects.filter(
            quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
        if not data.exists():
            return Response({'Message': 'No data found',
                                },  status=status.HTTP_400_BAD_REQUEST)
        
        training_data = OccupationalHealthQuarterSeialzier(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "training_data": training_data},
                            status=200)






class OccupationalHealthQuarterExcelDownload(generics.ListAPIView):
    serializer_class = ExcelOccupationalHealthQuarterSeialzier
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['packages']
    # filterset_class = ConstructionCampFilter

    def get_queryset(self):
        queryset = occupationalHealthSafety.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values()


        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=OccupationalHealthQuarter.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response


class OccupationalHealthPackageView(generics.GenericAPIView):
    serializer_class = OccupationalHealthQuarterSeialzier
    def get(self , request , packages):
        data = occupationalHealthSafety.objects.filter(
            packages=packages ).order_by('-id')
        if not data.exists():
                return Response({'Message': 'No data found',
                                 },  status=status.HTTP_400_BAD_REQUEST)
        
        training_data = OccupationalHealthQuarterSeialzier(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "training_data": training_data},
                            status=200)




class ExcelOccupationalHealthQuarterFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='dateOfMonitoring__year', label='Year')
    # month = django_filters.NumberFilter(field_name='dateOfMonitoring__month', label='month')

    class Meta:
        model = occupationalHealthSafety
        fields = ['quarter', 'year']



class ExcelOccupationalHealthQuarterExcelDownload(generics.ListAPIView):
    serializer_class = ExcelOccupationalHealthQuarterSeialzier
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['packages', 'constructionSiteName']
    filterset_class = ExcelOccupationalHealthQuarterFilter

    def get_queryset(self):
        queryset = occupationalHealthSafety.objects.all()
        # Customize the queryset based on your specific requirements
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Use values to convert the queryset to a list of dictionaries
        data = queryset.values()
        if not data:
            return JsonResponse({'status':'error','message':'Data Not Found'}, status=400)
        else:
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data)

            # Create a response with the appropriate content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=OccupationalHealthQuarter.xlsx'

            # Write the DataFrame to the Excel response
            df.to_excel(response, index=False, sheet_name='Sheet1')

            return response


class ExcelWorkbook(generics.GenericAPIView):
    serializer_class = LabourcampReportSerializer

    def get(self, request):
        wb = Workbook()
        ws = wb.active

        ws['A1'] = "Pranav"
        wb.save("sample1")
        

