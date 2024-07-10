from rest_framework import viewsets,generics
from ..models import Country,organization,Continent
from ..serializers import countrySerializer,CountrySerializer1
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

  
class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer1
 #this is for cached data##   
    def list(self, request, *args, **kwargs):
        cache_key = 'countries_list'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # Add field indicating data is from cache
            response_data = {'source': 'cache', 'data': cached_data}
            return Response(response_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=None)  # Cache indefinitely

        # Add field indicating data is from database
        response_data = {'source': 'database', 'data': response.data}
        return Response(response_data)




# class CountsView(APIView):
#     def get(self, request, country_id):
#         try:
#             # Get the specific country by ID
#             country = Country.objects.get(pk=country_id)
            
#             # Get the continent for the specific country
#             continent = country.continent
            
#             # Get the organization count for the specific country
#             organization_count = organization.objects.filter(country=country).count()
            
#             # Get the organization count for the specific continent
#             organization_count_by_continent = organization.objects.filter(country__continent=continent).count()
            
#             # Get the total organization count
#             total_org_count = organization.objects.count()
            
#             # Get the total count of continents
#             continent_count = Continent.objects.count()
            
#             # Get the total count of countries
#             country_count = Country.objects.count()

#             # Get the organization count for each continent
#             continents_organization_count = []
#             continent = Continent.objects.all()
#             for continent in continent:
#                 count = organization.objects.filter(country__continent=continent).count()
#                 continents_organization_count.append({
#                     "continent_name": continent.name,
#                     "organization_count": count
#                 })
            
#             return Response({
#                 "organization_count_by_country_id": organization_count,
#                 "organization_count_by_continent": organization_count_by_continent,
#                 "total_organization_count": total_org_count,
#                 "continent_count": continent_count,
#                 "country_count": country_count,
#                 "continents_organization_count": continents_organization_count
#             }, status=status.HTTP_200_OK)
        
#         except Country.DoesNotExist:
#             return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)


# class CountsView(APIView):
#     def get(self, request):
#         continent_list = Continent.objects.all()
        
#         organization_count = organization.objects.all().count()  # Corrected capitalization
#         continents_organization_count = []
        
#         for continent in continent_list:
#             count = organization.objects.filter(country__continent=continent).count()  # Corrected capitalization
#             continents_organization_count.append({
#                 "continent_name": continent.name,
#                 "organization_count": count
#             })
        
#         return Response({
#             "Total Organizations Count": organization_count,
#             "continents_organization_count": continents_organization_count,
            
#         }, status=status.HTTP_200_OK)




class countries_by_Continent(generics.GenericAPIView):
    serializer_class = countrySerializer

    def get(self, request, continent):
        try:
            # Fetch the continent using the provided ID
            continent = Country.objects.filter(continent=continent)

            serialized_data=countrySerializer(continent,many=True)

            country_count = continent.count()

           
            return Response({
                "country_count": country_count,
                "countries": serialized_data.data
            }, status=status.HTTP_200_OK)
        
        except Continent.DoesNotExist:
            return Response({
                'message': 'Continent not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






# from ..serializers import countrySerializer
# from ..models import Country
# from rest_framework import viewsets
# from rest_framework .response import Response



# class CountryVIews(viewsets.ModelViewSet):
#     queryset = Country.objects.all()
#     serializer_class = countrySerializer


#     def list(self, request):
#         filter_kwargs = {}

#         for key, value in request.query_params.items():
#             filter_kwargs[key] = value

#         # if not filter_kwargs:
#         #     return super().list(request)

#         try:
#             queryset = Country.objects.filter(**filter_kwargs)
            
#             if not queryset.exists():
#                 return Response({
#                     'message': 'Data not found',
#                     'status': 404
#                 })

#             serialized_data = countrySerializer(queryset, many=True)
#             return Response(serialized_data.data)

#         except Country.DoesNotExist:
#             return Response({
#                 'message': 'Objects not found',
#                 'status': 404
#             })