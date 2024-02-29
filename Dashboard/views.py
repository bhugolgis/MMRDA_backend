from django.db.models import Count
from rest_framework.generics import GenericAPIView, ListAPIView
from .serializers import *
from EnvMonitoring.models import *
from Training.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from MMRDA.utils import error_simplifier
from rest_framework import status



# Create your views here.

class PAPCategoryDashboardView(ListAPIView):
    serializer_class = PAPDashboardSerializer
    queryset = PAP.objects.all()

    def get(self, request, *args, **kwargs):
        land_use_type = [
    "Residential Land",
    "Private Land",
    "Other",
    "Institutional Land",
    "Government Land",
    "Commercial Land"
        ]
        packages = self.request.query_params.get("packages")
        quarter = self.request.query_params.get("quarter")
        if packages and quarter:
            categoryOfPap = PAP.objects.filter(packages = packages , quarter = quarter).values('categoryOfPap').annotate(count=Count('categoryOfPap'))
            print(categoryOfPap)

            lable = [count['categoryOfPap'] for count in categoryOfPap]
            dataset_PAP = [count['count'] for count in categoryOfPap]
            # # if no values when filtered
            # for value in land_use_type:
            #     if value not in lable:
            #         lable.append(value)
            #         dataset_PAP.append(0)
        else:
            categoryOfPap = PAP.objects.values('categoryOfPap').annotate(count=Count('categoryOfPap'))
            print(categoryOfPap)
            lable = [count['categoryOfPap'] for count in categoryOfPap]
            lable.sort(reverse=True)
            dataset_PAP = [count['count'] for count in categoryOfPap]
            dataset_PAP.sort(reverse=True)
            # print(dataset_PAP)
        # lable_PAP = [count['categoryOfPap'] for count in categoryOfPap]

        # dataset_PAP = [22 , 22 , 20 , 25 , 23 , 22]
        # dataset_Rehabilitations = [13 ,13 , 8 , 17, 13 , 17]
        # result = []
        # for i in range(len(dataset_PAP)):
        #     percentage = int((dataset_Rehabilitations[i] / dataset_PAP[i]) * 100)
        #     result.append(percentage)
        # totel_identified = sum(dataset_PAP)
        # total_Rehabilitations = sum(dataset_Rehabilitations)
        # total_percentage = int(total_Rehabilitations / totel_identified * 100)

        return Response({'status': 'success',
                        'Message': 'Data Fetched successfully',
                        'label' : lable ,
                        'dataset_PAP': dataset_PAP,
                        # 'dataset_Rehabilitations' : dataset_Rehabilitations ,
                        # 'percentage' : result ,
                        # 'totel_identified' : totel_identified, 
                        # 'total_Rehabilitations' : total_Rehabilitations , 
                        # 'total_percentage' : total_percentage , 
                         })


class CategoryWiseCompensationChart(APIView):
    # not working when not passing parameters
    def get(self, request, *args , **kwargs,):
        packages = self.request.query_params.get("packages")
        quarter = self.request.query_params.get("quarter")
        print(packages)
        print(quarter)
        # Rehabilitations = Rehabilitation.objects.filter(packages = packages , quarter = quarter).values('categoryOfPap').annotate(count=Count('categoryOfPap'))
        # dataset_Rehabilitations = [count['count'] for count in Rehabilitations]
        # print(Rehabilitations)
        # label = [count['categoryOfPap'] for count in Rehabilitations]
        # print(label)

        if packages and quarter:
            Compensation_Status = Rehabilitation.objects.filter(packages=packages, quarter=quarter).values('compensationStatus').annotate(count=Count('compensationStatus'))
            

            label_Compensation_Status = [count['compensationStatus'] for count in Compensation_Status]
            # print(label_Compensation_Status)
            dataset_Compensation_Status = [count['count'] for count in Compensation_Status]
            # print(dataset_Compensation_Status)

            return Response({'status': 'success',
                            'Message': 'Data Fetched successfully',
                            # 'label' : label ,
                            # 'dataset_Rehabilitations': dataset_Rehabilitations,
                            'label_Compensation_Status' : label_Compensation_Status ,
                            'dataset_Compensation_Status': dataset_Compensation_Status
                            })
        else:
            Compensation_Status = Rehabilitation.objects.values('compensationStatus').annotate(count=Count('compensationStatus'))

            label_Compensation_Status = [count['compensationStatus'] for count in Compensation_Status]
            # print(label_Compensation_Status)
            dataset_Compensation_Status = [count['count'] for count in Compensation_Status]
            # print(dataset_Compensation_Status)

            return Response({'status': 'success',
                            'Message': 'Data Fetched successfully',
                            # 'label' : label ,
                            # 'dataset_Rehabilitations': dataset_Rehabilitations,
                            'label_Compensation_Status' : label_Compensation_Status ,
                            'dataset_Compensation_Status': dataset_Compensation_Status
                            })


class IdentifiedPAPDashboardView(APIView):
    serializer_class = PAPDashboardSerializer

    def get(self, request, *args, **kwargs):
        IdentifiedPAP = PAP.objects.all().count()
        if IdentifiedPAP == 0:
            return Response({'Message': 'No data Found',
                            'status': 'success'})

        return Response({'status': 'success',
                        'Message': 'Data Fetched successfully',
                         'dataset': IdentifiedPAP}, status=200)


class RehabilitatedPAPDashboardView(GenericAPIView):
    serializer_class = RehabilationDashboardSerializer

    def get(self, request):
        packages = self.request.query_params.get("packages")
        quarter = self.request.query_params.get("quarter")
        print("before if")
        if packages and quarter:
            print("inside if")
            counts = Rehabilitation.objects.filter(packages = packages , quarter = quarter).values('compensationStatus').annotate(count=Count('compensationStatus'))
            label = [count['compensationStatus'] for count in counts]
            print(label)
            totalcount = Rehabilitation.objects.all().count()

            dataset = [count['count'] for count in counts]
        else:
            counts = Rehabilitation.objects.values('compensationStatus').annotate(count=Count('compensationStatus'))
            label = [count['compensationStatus'] for count in counts]
            print(label)
            totalcount = Rehabilitation.objects.all().count()

            dataset = [count['count'] for count in counts]
        return Response({'status': 'success',
                        'Message': 'Data fetched successfully',
                         'dataset': dataset,
                         'label' : label , 
                         'totalcount' : totalcount ,
                        #  'Counts': counts,
                          } , status= 200)


class LabourCampFacilitiesDashboardView(GenericAPIView):
    serializer_class = LabourcampDashboardSerializer

    def get(self, request, labourCampName , quarter ,  *args, **kwargs):

        labour = LabourCamp.objects.filter(
            labourCampName=labourCampName , quarter = quarter)
        if labour:
            data = LabourcampDashboardSerializer(labour.latest('id')).data
            values = list(data.values())
            
            dataset = []
            dataset.append(values.count('Good')), dataset.append(
                values.count('Average'))
            dataset.append(values.count('Bad'))

            return Response({'status': 'success',
                            'Message': 'data Fetched successfully',
                            'dataset': dataset,
                            'data': data}, status=200)
        else:
            return Response({"status" : "error",
                    "message" : "Labour Camp Data Not Present"} , status=200)
        

class LabourCampFacilitiesOverallDashboardView(APIView):
    serializer_class = LabourcampDashboardSerializer

    def get(self, request, *args, **kwargs):

        labour = LabourCamp.objects.all()
        datas = LabourcampDashboardSerializer(labour, many=True).data

        fields_to_process = ('toiletCondition', 'drinkingWaterCondition', 'demarkationOfPathwaysCondition',
                            'signagesLabelingCondition', 'kitchenAreaCondition', 'fireExtinguishCondition',
                            'roomsOrDomsCondition', 'segregationOfWasteCondition')

      
        field_counts = {}

        for field in fields_to_process:
            field_counts[field] = {
                'Good': 0,
                'Average': 0,
                'Bad': 0
            }

        for data in datas:
            for field in fields_to_process:
                if data[field] == 'Good':
                    field_counts[field]['Good'] += 1
                elif data[field] == 'Average':
                    field_counts[field]['Average'] += 1
                elif data[field] == 'Bad':
                    field_counts[field]['Bad'] += 1

        dataset = [
            sum(field_counts[field]['Good'] for field in fields_to_process),
            sum(field_counts[field]['Average'] for field in fields_to_process),
            sum(field_counts[field]['Bad'] for field in fields_to_process),
        ]

        return Response({
            'status': 'success',
            'Message': 'data Fetched successfully',
            'dataset': dataset,
            'label' : ['Good' , 'Average' , 'Bad']
        }, status=200)


class ConstructionSiteFacilitiesOverallDashboardView(generics.GenericAPIView):
    serializer_class = ConstructionSiteDashboardSerializer

    def get(self, request, *args, **kwargs):

        labour = ConstructionSiteDetails.objects.all()
        datas = self.get_serializer(labour, many=True).data

        fields_to_process =('toiletCondition' ,'drinkingWaterCondition' ,'demarkationOfPathwaysCondition',
                            'signagesLabelingCondition',)
      
        field_counts = {}

        for field in fields_to_process:
            field_counts[field] = {
                'Good': 0,
                'Average': 0,
                'Bad': 0
            }

        for data in datas:
            for field in fields_to_process:
                if data[field] == 'Good':
                    field_counts[field]['Good'] += 1
                elif data[field] == 'Average':
                    field_counts[field]['Average'] += 1
                elif data[field] == 'Bad':
                    field_counts[field]['Bad'] += 1
        dataset = [
            sum(field_counts[field]['Good'] for field in fields_to_process),
            sum(field_counts[field]['Average'] for field in fields_to_process),
            sum(field_counts[field]['Bad'] for field in fields_to_process),
        ]

        return Response({
            'status': 'success',
            'Message': 'data Fetched successfully',
            'dataset': dataset,
            # 'data': datas
        }, status=200)


class ConstructionChartView(GenericAPIView):
    serializer_class = ConstructionSiteDashboardSerializer

    def get(self, request,constructionSiteName, quarter , *args, **kwargs):
        ConstructionCamp = ConstructionSiteDetails.objects.filter(constructionSiteName = constructionSiteName , quarter = quarter)
        if ConstructionCamp:
            data = ConstructionSiteDashboardSerializer(ConstructionCamp.latest('id')).data
            values = list(data.values())
            dataset = []
            dataset.append(values.count('Good')) , dataset.append(values.count('Average')) , dataset.append(values.count('Bad'))
            return Response({'status': 'success',
                            'Message': 'data Fetched successfully',
                            'dataset': dataset,
                            'data': data}, status=200)
        else:
            return Response({"status" : "error" ,
                             "message" : "Construction Site Data Not Present"} , status= 200)


class CashCompensationTypeCharView(GenericAPIView):
    serializer_class = RehabilationDashboardSerializer

    def get(self, request):
        counts = Rehabilitation.objects.values(
            'typeOfCompensation').annotate(count=Count('typeOfCompensation'))
        label = [count['typeOfCompensation'] for count in counts]  
        print(label)
        dataset = [count['count'] for count in counts]
        print(dataset)

        return Response({'status': 'success',
                         'Message': 'data fetched Successfully',
                         'dataset': dataset,
                         'label' : label})


class ExistingTreeCount(GenericAPIView):
    serializer_class = ExistingTreeSerializer

    def get(self, request):
        try:
            ExistingTreeCount = []
            NewtreeCount = []
            treecount = ExistingTreeManagment.objects.all().count()
            NewTreeCount = NewTreeManagement.objects.all().count()
            ExistingTreeCount.append(
                treecount), NewtreeCount.append(NewTreeCount)
            return Response({'status': 'success',
                            'Message': 'Data was successfully fetched',
                             'ExistingTreeCount': ExistingTreeCount,
                             'NewtreeCount': NewtreeCount,
                             }, status=200)
        except:
            return Response({'status': 'error',
                            'Message': 'Something went wrong'}, status=400)


class WasteTypeCount(APIView):

    def get(self, request):
        counts = WasteTreatments.objects.values('wastetype').annotate(count = Count('wastetype'))
        dataset = [count['count'] for count in counts]
        label = [count['wastetype'] for count in counts]

        return Response({'status': 'success',
                            'Message': 'Data was successfully fetched',
                            'dataset': dataset,
                            'label' : label })
        


class WasteHandelingChart(APIView):
    def get(self, request):
        counts = WasteTreatments.objects.values('wastehandling').annotate(count = Count('wastehandling'))
        dataset = [count['count'] for count in counts]
        label = [count['wastehandling'] for count in counts]
        return Response({'status': 'success',
                            'Message': 'Data was successfully fetched',
                            'dataset': dataset,
                            'label' : label , 
                            'counts' : counts})
    

class MaterialSourceTypeCountChart(APIView):

    def get(self, request):
        counts = MaterialManegmanet.objects.values('source').annotate(count = Count('source'))
        label  = [count['source'] for count in counts]
        dataset = [count['count'] for count in counts]
        return Response({'status': 'success',
                         'Message': 'Data was successfully fetched',
                         'dataset': dataset,
                         'label' : label , 
                         'counts' : counts}, status=200)
       


class MaterialConditionChart(APIView):
    def get(self, request):

        counts = MaterialManegmanet.objects.values('materialStorageCondition').annotate(count = Count('materialStorageCondition'))
        dataset = [count['count'] for count in counts]
        label = [count['materialStorageCondition'] for count in counts]
        return Response({'status': 'success',
                            'Message': 'Data was successfully fetched',
                            'dataset': dataset,
                            'label' : label , 
                            'counts' : counts}, status=200)
    


class IncidenttypeCountchart(APIView):
# need proper response for no data available like only CA-08 and July September data is available
    def get(self, request, packages, quarter):
        counts = occupationalHealthSafety.objects.values('typeOfIncident').filter(packages=packages, quarter=quarter).exclude(typeOfIncident="Man Days Lost").annotate(count = Count('typeOfIncident'))
        label = [count['typeOfIncident'] for count in counts]
        dataset = [count['count'] for count in counts]
        

        if not label:
            return Response({ 'Message': 'No data found', 
                         }, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'success',
                        'Message': 'Data was successfully fetched',
                        'dataset': dataset,
                        'label' : label , 
                         })
        


class WaterConditionChart(APIView):

    def get(self, request):
        counts = water.objects.values('qualityOfWater').annotate(count = Count('qualityOfWater'))
        label = [count['qualityOfWater'] for count in counts]
        dataset = [count['count'] for count in counts]
        return Response({'status': 'success',
                            'Message': 'Data was successfully fetched',
                            'dataset': dataset,
                            'label' : label , 
                            'counts': counts }, status=200)
        

class AirChartView(generics.GenericAPIView):
    serializer_class = AirChartSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, month, year, **kwargs):
        try:
            airdata = Air.objects.filter(month=month, dateOfMonitoring__year=year).latest('id')
            label =  ['PM10' , 'SO2' ,'O3' , 'NOx' , 'AQI' ]
        except:
            return Response({'Message': 'No data Avaialable for this Month or Year',
                            'status': 'error'},)
        dataset = []
        serializers = AirChartSerializer(airdata  ).data
        print(serializers)
       
        dataset.append(serializers.get('PM10')), dataset.append(
        serializers.get('SO2')), dataset.append(serializers.get('O3')),
        dataset.append(serializers.get('NOx')), dataset.append(serializers.get('AQI'))
        return Response({'status': 'success',
                         'Message': 'Data was successfully fetched',
                         'label' : label , 
                         'dataset': dataset    })                
                        # 'PM10': serializers.get('PM10'), 'SO2': serializers.get('SO2'),
                        #  'O3':  serializers.get('O3'), 'Nox': serializers.get('NOx'),
                        #  'AQI': serializers.get('AQI')})


# API for PAP count
class SocialMonitoringCountDashboardView(APIView):
    serializer_class = SocialMonitoringCountDashboardViewSerializer
    #Need to be optimized
    def get(self, request,quarter, packages, *args, **kwargs):

        PAPCount = PAP.objects.all().filter(packages=packages, quarter=quarter).count()
        EligiblePAPCount = PAP.objects.filter(eligibility='Eligible', packages=packages, quarter=quarter).count()
        NonEligiblePAPCount = PAP.objects.filter(eligibility='Not Eligible', packages=packages, quarter=quarter).count()
        ReallocateCount = Rehabilitation.objects.all().filter(packages=packages, quarter=quarter).count()
        NonReallocateCount = PAPCount - ReallocateCount


        print('eligible_count:', EligiblePAPCount, 'none_count:', NonEligiblePAPCount)

        # for obj in queryset:
        #   print(obj.__dict__)

        # # Serialize the queryset using your custom serializer
        # serializer = SocialMonitoringCountDashboardViewSerializer(queryset, many=True)
        # serialized_data = serializer.data

        # for obj in serialized_data:
        #   print(obj)

        if PAPCount == 0:
            return Response({'Message': 'No data Found',
                            'status': 'success'})

        return Response({'status': 'success',
                        'Message': 'Data Fetched successfully',
                         'PAPcount': PAPCount,
                         'EligiblePAPCount': EligiblePAPCount,
                         'NonEligiblePAPCount': NonEligiblePAPCount,
                         'ReallocateCount': ReallocateCount,
                         'NonReallocateCount': NonReallocateCount,
                         }, status=200)
    


class AirAQIChartDashboardView(APIView):
    serializer_class = DashboardAQISerializer
    
    def get(self, request,quarter, packages, *args, **kwargs):

        air = Air.objects.all().filter(packages=packages, quarter=quarter)

        if not air:
            return Response({
                        'Message': 'Use package CA-08 and quarter July-September',
                        }, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = DashboardAQISerializer(air, many=True)
        serializer_data = serializer.data
     
        aqi_list = []
        for object in serializer_data:
            aqi_list.append(object['AQI'])
            
        avg_aqi = sum(aqi_list) / len(aqi_list)
        
        return Response({
            "message":"AQI generated successfully",
            "status":"success",
            "data":avg_aqi,
            # "quality": quality
        })
    



class ManDaysLostCountchart(APIView):
# how to improve it more    
    def get(self, request, packages, quarter):
        count = occupationalHealthSafety.objects.filter(packages=packages, quarter=quarter, typeOfIncident="Man Days Lost").count()
        

        if count == 0:
            return Response({
                        'Message': 'Data not found',
                        }, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'success',
                        'Message': 'Data was successfully fetched',
                        'count': count,
                        })
    



# class WaterWQIChartDashboardView(APIView):
#     serializer_class = DashboardAQISerializer
    
#     def get(self, request,quarter, packages, *args, **kwargs):

#         water = water.objects.all().filter(packages=packages, quarter=quarter)
#         serializer = DashboardAQISerializer(air, many=True)
#         serializer_data = serializer.data
     
#         aqi_list = []
#         for object in serializer_data:
#             aqi_list.append(object['AQI'])
            
#         avg_aqi = sum(aqi_list) / len(aqi_list)
        
#         return Response({
#             "message":"AQI generated successfully",
#             "status":"success",
#             "data":avg_aqi,
#             # "quality": quality
#         })