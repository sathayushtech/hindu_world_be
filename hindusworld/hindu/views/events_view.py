from rest_framework import viewsets,generics
from ..models import Events
from ..serializers import EventsSerializer,EventsSerializer1,EventSerializer2
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












