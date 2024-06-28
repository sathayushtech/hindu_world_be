from ..models import State
from ..serializers import StateSeerializer
from rest_framework import viewsets
from rest_framework .response import Response


class StateViews(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSeerializer


    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = State.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = StateSeerializer(queryset, many=True)
            return Response(serialized_data.data)

        except State.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })
    