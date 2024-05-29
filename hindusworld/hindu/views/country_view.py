from rest_framework import viewsets,generics
from ..models import Country,organization,continents
from ..serializers import countrySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = countrySerializer





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
#             continent_count = continents.objects.count()
            
#             # Get the total count of countries
#             country_count = Country.objects.count()

#             # Get the organization count for each continent
#             continents_organization_count = []
#             continent = continents.objects.all()
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



class CountsView(APIView):
    def get(self, request):
        continent = continents.objects.all()
        
        organization_count=organization.objects.all().count()
        continents_organization_count = []
        
        for continent in continent:
            count = organization.objects.filter(country__continent=continent).count()
            continents_organization_count.append({
                "continent_name": continent.name,
                "organization_count": count
            })
        
        return Response({
            "Total Organizations Count":organization_count,
            "continents_organization_count": continents_organization_count,
            
        }, status=status.HTTP_200_OK)
    




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
        
        except continents.DoesNotExist:
            return Response({
                'message': 'Continent not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




