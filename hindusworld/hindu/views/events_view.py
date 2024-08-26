from rest_framework import viewsets,generics
from ..models import Events
from ..serializers import *
from ..models import Organization, Country,Continent,Register,District,Events
from rest_framework import status
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from ..utils import save_image_to_folder
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from ..enums import EventStatusEnum
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50






class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer1


class AddEventView(generics.GenericAPIView):
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            username = request.user.username
            print(f"Username: {username}")

            register_instance = Register.objects.get(username=username)
            is_member = register_instance.is_member

            # Check if the user is a member
            if is_member == "FALSE":
                return Response({
                    "message": "Cannot create event. Membership details are required. Update your profile and become a member."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Capture the current time
            created_at = timezone.now()

            # Proceed with event creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Handle event brochure if provided
            brochure = request.data.get('brochure')
            if brochure and brochure != "null":
                saved_brochure_location = save_image_to_folder(brochure, serializer.instance._id, serializer.instance.name, 'eventbrochures')
                if saved_brochure_location:
                    serializer.instance.brochure = saved_brochure_location

            # Handle event images if provided
            event_images = request.data.get('event_images', [])
            if event_images:
                saved_event_image_paths = []
                for image_data in event_images:
                    if image_data and image_data != "null":
                        saved_location = save_image_to_folder(image_data, serializer.instance._id, serializer.instance.name, 'eventimages')
                        if saved_location:
                            saved_event_image_paths.append(saved_location)
                serializer.instance.event_images = saved_event_image_paths
                serializer.instance.save()

            # Send email to EMAIL_HOST_USER
            send_mail(
                'New Event Added',
                f'User ID: {request.user.id}\n'
                f'Contact Number: {register_instance.contact_number}\n'
                f'Full Name: {request.user.get_full_name()}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Event ID: {serializer.instance._id}\n'
                f'Event Name: {serializer.instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "Event added successfully.",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Register.DoesNotExist:
            return Response({
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        







class UpdateEventStatus(generics.GenericAPIView):
    serializer_class = EventSerializer2

    def put(self, request, event_id):
        try:
            event = Events.objects.get(pk=event_id, status='PENDING')
        except Events.DoesNotExist:
            return Response({
                'message': 'Event with PENDING status not found for the provided ID'
            }, status=status.HTTP_404_NOT_FOUND)

        # Update the status to 'SUCCESS'
        event.status = 'SUCCESS'
        event.save()

        # Serialize the updated event
        serializer = self.get_serializer(event)

        return Response({
            'message': 'success',
            'result': serializer.data
        }, status=status.HTTP_200_OK)








 



from django.utils import timezone
from datetime import datetime

class UpcomingEventsView(generics.ListAPIView):
    serializer_class = EventsSerializer1
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter events where start_date is in the future or today
        today = datetime.now().date()

        # Assuming your dates are in 'DD-MM-YYYY' format, convert them before filtering
        events = Events.objects.all()
        upcoming_events = []
        for event in events:
            # Parse the start_date correctly
            start_date = datetime.strptime(event.start_date, '%d-%m-%Y').date()
            if start_date >= today:
                upcoming_events.append(event)
        return upcoming_events

class PastEventsView(generics.ListAPIView):
    serializer_class = EventsSerializer1
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter events where end_date is in the past
        today = datetime.now().date()

        # Assuming your dates are in 'DD-MM-YYYY' format, convert them before filtering
        events = Events.objects.all()
        past_events = []
        for event in events:
            # Parse the end_date correctly
            end_date = datetime.strptime(event.end_date, '%d-%m-%Y').date()
            if end_date < today:
                past_events.append(event)
        return past_events
    



class GetEventsByLocation(generics.ListAPIView):
    serializer_class = EventsSerializer1
    pagination_class = CustomPagination


    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')

        # Ensure either input_value or category is provided
        if not input_value and not category:
            raise ValidationError("Input value or category is required")

        queryset = Events.objects.all()

        # Apply filters based on the input values
        if input_value:
            # Define queries for each level
            continent_query = Q(object_id__state__country__continent__pk=input_value)
            country_query = Q(object_id__state__country__pk=input_value)
            state_query = Q(object_id__state__pk=input_value)
            district_query = Q(object_id__pk=input_value)

            # Combine queries with OR operator
            combined_query = continent_query | country_query | state_query | district_query
            queryset = queryset.filter(combined_query)

            # If the queryset is empty, check directly by object_id
            if not queryset.exists():
                queryset = Events.objects.filter(object_id=input_value)

        if category:
            queryset = queryset.filter(category=category)

        # Prefetch related fields for better performance
        queryset = queryset.select_related(
            'object_id__state__country__continent',
            'object_id__state__country',
            'object_id__state',
            'object_id'
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)










from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

class EventListView(generics.ListAPIView):
    serializer_class = EventsSerializer4
    pagination_class = CustomPagination

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        now = timezone.now()

        queryset = Events.objects.all()

        # Update event statuses before returning the queryset
        for event in queryset:
            event.update_event_status()

        if status_param:
            if status_param not in dict(EventStatusEnum.__members__).keys():
                raise ValidationError("Invalid status value")
            queryset = queryset.filter(event_status=status_param)

        # Order events: upcoming events first, then completed events
        return queryset.order_by(
            Case(
                When(event_status=EventStatusEnum.UPCOMING.name, then=Value(0)),
                When(event_status=EventStatusEnum.COMPLETED.name, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'  # Further order by start date within each status group
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)