from ..serializers import VillageSerializer
from ..models import Village
from rest_framework import viewsets
from rest_framework .response import Response
from ..utils import CustomPagination
from rest_framework.pagination import PageNumberPagination



class VillageView(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    print("sssssss")
    serializer_class = VillageSerializer
    pagination_class = CustomPagination


    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = Village.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = VillageSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except Village.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })
        
class GetVillages(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = VillageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = VillageSerializer(queryset, many=True)
        return Response(serializer.data)


