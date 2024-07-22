from django.db.models import Count
from rest_framework.generics import GenericAPIView, ListAPIView
from .serializers import *
from EnvMonitoring.models import *
from EnvMonitoring.models import water as Water
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
        packages = self.request.query_params.get("packages")
        quarter = self.request.query_params.get("quarter")

        # Apply filters if parameters are provided
        if packages and quarter:
            category_of_pap = PAP.objects.filter(packages=packages, quarter=quarter).values('categoryOfPap').annotate(count=Count('categoryOfPap'))
        else:
            category_of_pap = PAP.objects.values('categoryOfPap').annotate(count=Count('categoryOfPap'))

        # Check if any data is found
        if not category_of_pap:
            return Response({'message': 'No data found'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract labels and counts, handle None values
        labels = [item['categoryOfPap'] for item in category_of_pap if item['categoryOfPap'] is not None]
        dataset_pap = [item['count'] for item in category_of_pap if item['categoryOfPap'] is not None]


        desired_order = [
            "Residential Land",
            "Commercial Land",
            "Private Land",
            "Government Land",
            "Institutional Land",
            "Other"
        ]

        # Sort labels and dataset_pap together
        # sorted_labels_and_counts = sorted(zip(labels, dataset_pap), reverse=True)
        # sorted_labels = [label for label, _ in sorted_labels_and_counts]
        # sorted_dataset_pap = [count for _, count in sorted_labels_and_counts]

        sorted_labels = []
        sorted_dataset_pap = []
        for category in desired_order:
            for item in category_of_pap:
                if item['categoryOfPap'] == category:
                    sorted_labels.append(category)
                    sorted_dataset_pap.append(item['count'])
                    break  # Stop iterating through category_of_pap once a match is found

        # Handle cases where categories are not present in data
        missing_categories = set(desired_order) - set(sorted_labels)
        for category in missing_categories:
            sorted_labels.append(category)
            sorted_dataset_pap.append(0)  # Add 0 count for missing categories
        
        return Response({
            'status': 'success',
            'Message': 'Data fetched successfully',
            'label': sorted_labels,
            'dataset_PAP': sorted_dataset_pap,
        }, status=status.HTTP_200_OK)


class CategoryWiseCompensationChart(APIView):
    # not working when not passing parameters
    def get(self, request, *args, **kwargs):
        packages = request.query_params.get("packages")
        quarter = request.query_params.get("quarter")

        if packages and quarter:
            Compensation_Status = Rehabilitation.objects.filter(packages=packages, quarter=quarter).values('compensationStatus').annotate(count=Count('compensationStatus'))
        else:
            Compensation_Status = Rehabilitation.objects.values('compensationStatus').annotate(count=Count('compensationStatus'))

        if not Compensation_Status:
            return Response({'message': 'no data found'}, status=status.HTTP_400_BAD_REQUEST)

        label_Compensation_Status = [item['compensationStatus'] for item in Compensation_Status]
        dataset_Compensation_Status = [item['count'] for item in Compensation_Status]

        return Response({
            'status': 'success',
            'Message': 'Data Fetched successfully',
            'label_Compensation_Status': label_Compensation_Status,
            'dataset_Compensation_Status': dataset_Compensation_Status
        }, status=status.HTTP_200_OK)


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
    parser_classes = [MultiPartParser]

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
    def get(self, request, *args, **kwargs):
        quarter = request.query_params.get('quarter')
        packages = request.query_params.get('packages')

        # Base queryset
        pap_queryset = PAP.objects.all()
        rehab_queryset = Rehabilitation.objects.all()

        # Apply filters if parameters are provided
        if quarter:
            pap_queryset = pap_queryset.filter(quarter=quarter)
            rehab_queryset = rehab_queryset.filter(quarter=quarter)
        if packages:
            pap_queryset = pap_queryset.filter(packages=packages)
            rehab_queryset = rehab_queryset.filter(packages=packages)

        # Calculate counts
        PAPCount = pap_queryset.count()
        EligiblePAPCount = pap_queryset.filter(eligibility='Eligible').count()
        NonEligiblePAPCount = pap_queryset.filter(eligibility='Not Eligible').count()
        ReallocateCount = rehab_queryset.count()
        NonReallocateCount = PAPCount - ReallocateCount

        # Print debug information
        print('eligible_count:', EligiblePAPCount, 'none_count:', NonEligiblePAPCount)

        # Return response
        if PAPCount == 0:
            return Response({'Message': 'No data Found', 'status': 'success'})

        return Response({
            'status': 'success',
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
                        'Message': 'No data found for specified package and quarter',
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
        # count = occupationalHealthSafety.objects.filter(packages=packages, quarter=quarter, typeOfIncident="Man Days Lost").count()
        data = occupationalHealthSafety.objects.filter(packages=packages, quarter=quarter)
        man_days_lost_counts = data.values_list('manDaysLostCount', flat=True).exclude(manDaysLostCount__isnull=True)

        total_count = 0
        for count in man_days_lost_counts:
            total_count = total_count + count
            

        print(total_count)
        if total_count == 0:
            return Response({
                        'Message': 'Data not found',
                        }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'success',
                        'Message': 'Data was successfully fetched',
                        'count': total_count,
                        })
    



class WaterWQIChartDashboardView(APIView):
    serializer_class = DashboardWQISerializer
    
    def get(self, request,quarter, packages, *args, **kwargs):

        water = Water.objects.all().filter(packages=packages, quarter=quarter)

        if not water:
            return Response({
            "message":"No data found for specified package/quarter",
        }, status=status.HTTP_404_NOT_FOUND)


        serializer = DashboardWQISerializer(water, many=True)
        serializer_data = serializer.data
     
        wqi_list = []
        for object in serializer_data:
            wqi_list.append(object['WQI'])
            
        avg_wqi = sum(wqi_list) / len(wqi_list)
        
        return Response({
            "message":"AQI generated successfully",
            "status":"success",
            "data":avg_wqi,
            # "quality": quality
        })
    
# Api for Env Monitoring Dashboard GIS Map
class DashboardEnvMonitoringGISMap(APIView):
    def get(self, request, quarter, packages, *args, **kwargs):
        water = Water.objects.all().filter(packages=packages, quarter=quarter)
        air = Air.objects.all().filter(packages=packages, quarter=quarter)
        noise = Noise.objects.all().filter(packages=packages, quarter=quarter)

        if not water:
            return Response({"message":"No data found for specified package/quarter",}
                            , status=status.HTTP_404_NOT_FOUND)
        
        serializer = DashboardEnvMonitoringGISMapWaterSerializer(water, many=True)
        serializer_data_water = serializer.data

        if not air:
            return Response({"message":"No data found for specified package/quarter",}
                            , status=status.HTTP_404_NOT_FOUND)
        
        serializer = DashboardEnvMonitoringGISMapAirSerializer(air, many=True)
        serializer_data_air = serializer.data

        if not noise:
            return Response({"message":"No data found for specified package/quarter",}
                            , status=status.HTTP_404_NOT_FOUND)
        
        serializer = DashboardEnvMonitoringGISMapNoiseSerializer(noise, many=True)
        serializer_data_noise = serializer.data

        return Response({"message": "Data Fetched successfully",
                         "data_water": serializer_data_water,
                         "data_air": serializer_data_air,
                         "data_noise": serializer_data_noise,}
                        , status=status.HTTP_200_OK)
    

class DashboardEnvMonReportsSubmitted(APIView):
    def get(self, request,month, year, *args, **kwargs):
        air = Air.objects.all().filter(month=month, dateOfMonitoring__year=year).count()
        print(air)
        if not air:
            return Response({"message":"No data found for specified package/quarter",}
                            , status=status.HTTP_400_BAD_REQUEST)
        

        if air >= 2:
            return Response({"message": "Data Fetched successfully",
                            "reports_submitted": "yes",}
                            , status=status.HTTP_200_OK)
        else:
            return Response({"message": "Data Fetched successfully",
                            "reports_submitted": "no",}
                            , status=status.HTTP_200_OK)
        


class NoiseChartDashboardView(APIView):
    serializer_class = DashboardNoiseSerializer
    
    def get(self, request,quarter, packages, *args, **kwargs):

        noise = Noise.objects.all().filter(packages=packages, quarter=quarter)

        if not noise:
            return Response({
                        'Message': 'No data found for specified package and quarter',
                        }, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = DashboardNoiseSerializer(noise, many=True)
        serializer_data = serializer.data

        # Initialize count variables
        day_within_limit_count = 0
        day_out_of_limit_count = 0
        night_within_limit_count = 0
        night_out_of_limit_count = 0

        # Iterate through serializer data
        for item in serializer_data:
            # Count occurrences for isWithinLimit_day
            if item['isWithinLimit_day'] == 'Within Limit':
                day_within_limit_count += 1
            elif item['isWithinLimit_day'] == 'Out of Limit':
                day_out_of_limit_count += 1

            # Count occurrences for isWithinLimit_night
            if item['isWithinLimit_night'] == 'Within Limit':
                night_within_limit_count += 1
            elif item['isWithinLimit_night'] == 'Out of Limit':
                night_out_of_limit_count += 1


        if day_within_limit_count > day_out_of_limit_count:
            day_within_limit_value = day_within_limit_count
            isWithinLimit_day = "Within Limit"
        else:
            day_within_limit_value = day_out_of_limit_count
            isWithinLimit_day = "Out of Limit"

        if night_within_limit_count > night_out_of_limit_count:
            night_out_of_limit_value = night_within_limit_count
            isWithinLimit_night = "Within Limit"
        else:
            night_out_of_limit_value = night_out_of_limit_count
            isWithinLimit_night = "Out of Limit"

        # Display the counts
        print("isWithinLimit_day:")
        print("Within Limit:", day_within_limit_count)
        print("Out of Limit:", day_out_of_limit_count)

        print("\nisWithinLimit_night:")
        print("Within Limit:", night_within_limit_count)
        print("Out of Limit:", night_out_of_limit_count)

        
        return Response({
            "message":"Noise chart generated successfully",
            "status":"success",
            "data":{"isWithinLimit_day": isWithinLimit_day,
                "isWithinLimit_night": isWithinLimit_night,
            },
            # "quality": quality
        })