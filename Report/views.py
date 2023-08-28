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
# from Report.models import Package54Alignment , Package12Alignment


''' --------------------------Labour Camp Report View----------------------------'''


class LabourcampReportPackageView(ListAPIView):
    serializer_class = LabourcampReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, labourCampName ,*args, **kwargs):
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

class LabourCampReportQuarterView(ListAPIView):

    serializer_class = LabourcampReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, labourCampName, year, *args, **kwarges):
        try:
            previous = LabourCamp.objects.filter(
                quarter=quarter, labourCampName=labourCampName, dateOfMonitoring__year=year).order_by('-id')[1:]

            latest = LabourCamp.objects.filter(
                quarter=quarter, labourCampName=labourCampName , dateOfMonitoring__year=year).latest('id')
            previousData = self.serializer_class(previous, many=True).data
            latestData = self.serializer_class(latest).data

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            'Previous': previousData,
                            'latest': latestData},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for this Package or Quarter',
                            'status' : 'Failed'}, status=400)

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
                            'status' : 'Failed'}, status=status.HTTP_400_BAD_REQUEST)

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


# -------------------------------------------------------------------------

class PAPReportPackageView(ListAPIView):
    serializer_class = PAPReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = PAP.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'Failed'},  status=status.HTTP_200_OK)
            papdata = PAPReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "PAP": papdata},
                            status=status.HTTP_200_OK)
        except Exception:
            return Response({'Message': 'There is no data available for the Package or Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class PAPReportQuarterView(ListAPIView):
    serializer_class = PAPReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year):
        try:
            data = PAP.objects.filter(
                quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)
            papdata = PAPReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "PAP": papdata},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package or Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)


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
                                 'status' : 'success'},  status=status.HTTP_200_OK)
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

class RehabilitationReportQuarterView(ListAPIView):
    serializer_class = RehabilitationReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year, *args, **kwargs):
        try:
            data = Rehabilitation.objects.filter(
                quarter=quarter, dateOfRehabilitation__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)
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


'''----------------------- Env Monitoring Report View------------------------------'''


class AirReportPackageView(ListAPIView):
    serializer_class = AirReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = Air.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)
            airdata = AirReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Air_data": airdata},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class AirReportQuarterView(ListAPIView):
    serializer_class = AirReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, month, year, *args, **kwargs):
        try:
            data = Air.objects.filter(
                month=month, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            airdata = AirReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Air_data": airdata},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class NoiseReportpackageView(ListAPIView):
    serializer_class = NoiseReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = Noise.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Noise_data = NoiseReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Noise_data": Noise_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class NoiseReportQuarterView(ListAPIView):
    serializer_class = NoiseReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, month, year, *args, **kwargs):
        try:
            data = Noise.objects.filter(
                month=month, dateOfMonitoringThree__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Noise_data = NoiseReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Noise_data": Noise_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class waterReportPackageView(ListAPIView):
    serializer_class = waterReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = water.objects.filter(packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            water_data = waterReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "water_data": water_data}, status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class waterReportQuarterView(ListAPIView):
    serializer_class = waterReportSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, month, year, *args, **kwargs):
        # try:
            data = water.objects.filter(month=month, dateOfMonitoringTwo__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            water_data = waterReportSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "water_data": water_data},
                            status=status.HTTP_200_OK)
        # except:
        #     return Response({'Message': 'There is no data available for the Quarter',
        #                     'status' : 'Failed'},
        #                     status=status.HTTP_400_BAD_REQUEST)

class WasteTreatmentsPackageView(ListAPIView):
    serializer_class = wasteTreatmentsSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = WasteTreatments.objects.filter(
                packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)
            Waste_data = wasteTreatmentsSerializer(data, many=True).data

            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "wasteManagementdata": Waste_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class WasteTreatmentsQuarterView(ListAPIView):
    serializer_class = wasteTreatmentsSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year, *args, **kwargs):
        try:
            data = WasteTreatments.objects.filter(quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Waste_data = wasteTreatmentsSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "wasteManagementData": Waste_data}, status=200)

        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'} , status=status.HTTP_400_BAD_REQUEST)

class MaterialManagementReporetpackageView(ListAPIView):
    serializer_class = materialManagementSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = MaterialManegmanet.objects.filter(
                packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Material_data = materialManagementSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "materialManagementData": Material_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class MaterialManagementReporetQuarterView(ListAPIView):
    serializer_class = materialManagementSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year, *args, **kwargs):
        try:
            data = MaterialManegmanet.objects.filter(
                quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Material_data = materialManagementSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "material Management data": Material_data},
                            status=200)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class TreeMangementReportPackage(ListAPIView):
    serializer_class = treeManagementSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, packages, *args, **kwargs):
        try:
            data = ExistingTreeManagment.objects.filter(
                packages=packages).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Material_data = treeManagementSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                            "Tree Management data": Material_data},
                            status=status.HTTP_200_OK)
        except:
            return Response({'Message': 'There is no data available for the Package',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

class TreeManagementReportQuarterView(ListAPIView):
    serializer_class = treeManagementSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, quarter, year, *args, **kwargs):
        try:
            data = ExistingTreeManagment.objects.filter(
                quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
            if not data.exists():
                return Response({'Message': 'No data found',
                                 'status' : 'success'},  status=status.HTTP_200_OK)

            Material_data = treeManagementSerializer(data, many=True).data
            return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "Tree Management data": Material_data},
                            status=200)
        except:
            return Response({'Message': 'There is no data available for the Quarter',
                            'status' : 'Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

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
                                'status' : 'success'},  status=status.HTTP_200_OK)
        
        training_data = TrainnigReportSerializer(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "training_data": training_data},
                            status=200)

class TrainnigReportPackageView(APIView):
    def get(self , request , packages):
   
        data = traning.objects.filter(
            packages=packages ).order_by('-id')
        if not data.exists():
            return Response({'Message': 'No data found',
                                'status' : 'success'},  status=status.HTTP_200_OK)
        
        training_data = TrainnigReportSerializer(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "training_data": training_data},
                            status=200)
    
class OccupationalHealthQuarterView(generics.GenericAPIView):
    serializer_class = OccupationalHealthQuarterSeialzier
    def get(self , request , quarter , year):
        data = occupationalHealthSafety.objects.filter(
            quarter=quarter, dateOfMonitoring__year=year).order_by('-id')
        if not data.exists():
            return Response({'Message': 'No data found',
                                'status' : 'success'},  status=status.HTTP_200_OK)
        
        training_data = OccupationalHealthQuarterSeialzier(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "training_data": training_data},
                            status=200)

class OccupationalHealthPackageView(generics.GenericAPIView):
    serializer_class = OccupationalHealthQuarterSeialzier
    def get(self , request , packages):
        data = occupationalHealthSafety.objects.filter(
            packages=packages ).order_by('-id')
        if not data.exists():
            return Response({'Message': 'No data found',
                                'status' : 'success'},  status=status.HTTP_200_OK)
        
        training_data = OccupationalHealthQuarterSeialzier(data, many=True).data
        return Response({'Message': 'data Fetched Successfully',
                            'status' : 'success' , 
                             "training_data": training_data},
                            status=200)

