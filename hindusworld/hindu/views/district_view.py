from rest_framework import viewsets
from ..models import District,State
from ..serializers import DistrictSerializer
from rest_framework .response import Response
from rest_framework import generics,status


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
        





class districts_By_State(generics.GenericAPIView):
    serializer_class = DistrictSerializer

    def get(self, request, state):
        try:
            # Fetch the districts using the provided state
            districts = District.objects.filter(state=state)

            serialized_data = DistrictSerializer(districts, many=True)
            district_count = districts.count()

            return Response({
                "district_count": district_count,
                "districts": serialized_data.data
            }, status=status.HTTP_200_OK)
        
        except State.DoesNotExist:
            return Response({
                'message': 'State not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)