from rest_framework import viewsets, generics
from ..models import continents,organization,Country
from ..serializers.continent_serializer import continentsSerializer
from ..serializers.country_serializer import countrySerializer
from rest_framework.response import Response
from rest_framework import status


class continentsView(viewsets.ModelViewSet):
    queryset = continents.objects.all()
    serializer_class = continentsSerializer

    
    # def get_serializer_class(self):
    #     if self.action == 'list' or self.action == 'create':
    #         return continentsSerializer
    #     return continentsSerializer1





