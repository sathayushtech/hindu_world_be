from rest_framework.views import APIView, status
from rest_framework.response import Response
from ..serializers import *
from ..models.district import District
from ..models.event import Events
from ..models.event_category import EventCategory
from ..models.organization import Organization 
from ..models.training import Training  





class OrganizationMain(APIView):
    def get(self, request):
        organizations = Organization.objects.all()[:4]  # Retrieve the first 4 organizations globally

        organization_serializer = OrgnisationSerializer1(organizations, many=True)

        return Response({
            'organizations': organization_serializer.data,
        })





class EventsMain(APIView):
    def get(self, request):
        event_category = EventCategory.objects.all()[:4]
        events = Events.objects.all()[:4]  # Retrieve the first 4 events globally

        # eventcategory = EventCategorySerializer(event_category, many=True)
        events_serializer = EventsSerializer(events, many=True)

        return Response({
            # 'categories': eventcategory.data,
            'events': events_serializer.data,
        })




class TrainingMain(APIView):
    def get(self, request):
        trainings = Training.objects.all()[:4]  # Retrieve the first 4 trainings globally

        training_serializer = TrainingSerializer(trainings, many=True)

        return Response({
            'trainings': training_serializer.data,
        })
