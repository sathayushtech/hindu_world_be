from rest_framework import viewsets
from ..models import District
from ..serializers import DistrictSerializer
from rest_framework .response import Response


class DistrictVIew(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = District.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = DistrictSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except District.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })