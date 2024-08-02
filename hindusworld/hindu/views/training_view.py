from rest_framework import viewsets, generics, status
from ..models import Training,Register
from ..serializers import TrainingSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..utils import save_image_to_folder,image_path_to_binary
import uuid


# class TrainingView(viewsets.ModelViewSet):
#     queryset = Training.objects.all()
#     serializer_class = TrainingSerializer
#     permission_classes = [IsAuthenticated]

#     def get_permissions(self):
#         if self.request.method in ['POST', 'PUT']:
#             return [IsAuthenticated()]
#         return super().get_permissions()

#     def list(self, request):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)

#         if page is not None:
#             serializer = TrainingSerializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = TrainingSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         try:
#             # Check if user is authenticated and is a member
#             username = request.user.username
#             register_instance = Register.objects.get(username=username)
#             is_member = register_instance.is_member

#             if is_member == "NO":
#                 return Response({
#                     "message": "Cannot add the training session. Membership details are required. Update your profile and become a member."
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Extract image_location from request data
#             image_location = request.data.get('image_location')
#             request.data['image_location'] = "null"

#             # Serialize data and save
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#             if image_location and image_location != "null":
#                 saved_location = save_image_to_folder(image_location, serializer.instance._id, serializer.instance.name, 'training')
#                 if saved_location:
#                     serializer.instance.image_location = saved_location
#                     serializer.instance.save()

#             # Capture the current time
#             created_at = timezone.now()

#             # Send email to EMAIL_HOST_USER
#             send_mail(
#                 'New Training Session Added',
#                 f'User ID: {request.user.id}\n'
#                 f'Full Name: {request.user.get_full_name()}\n'
#                 f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
#                 f'Training ID: {serializer.instance._id}\n'
#                 f'Training Name: {serializer.instance.name}',
#                 settings.EMAIL_HOST_USER,
#                 [settings.EMAIL_HOST_USER],
#                 fail_silently=False,
#             )

#             return Response({
#                 "message": "success",
#                 "result": serializer.data
#             }, status=status.HTTP_201_CREATED)

#         except Register.DoesNotExist:
#             return Response({
#                 "message": "User not found."
#             }, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({
#                 "message": "An error occurred.",
#                 "error": str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def retrieve(self, request, pk=None):
#         try:
#             training_instance = self.get_object()
#         except Training.DoesNotExist:
#             return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = TrainingSerializer(training_instance)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         instance = self.get_object()
#         serializer = TrainingSerializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         updated_instance = serializer.save()
#         return Response({
#             "message": "updated successfully",
#             "data": TrainingSerializer(updated_instance).data
#         })








class TrainingView(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = TrainingSerializer(page, many=True)
            data = serializer.data
            # Convert image paths to base64
            for item in data:
                image_path = item.get('image')
                if image_path:
                    image_binary = image_path_to_binary(image_path)
                    if image_binary:
                        item['image'] = image_binary.decode('utf-8')
            return self.get_paginated_response(data)

        serializer = TrainingSerializer(queryset, many=True)
        data = serializer.data
        # Convert image paths to base64
        for item in data:
            image_path = item.get('image')
            if image_path:
                image_binary = image_path_to_binary(image_path)
                if image_binary:
                    item['image'] = image_binary.decode('utf-8')

        return Response(data)

    def create(self, request, *args, **kwargs):
        try:
            # Check if user is authenticated and is a member
            username = request.user.username
            register_instance = Register.objects.get(username=username)
            is_member = register_instance.is_member

            if is_member == "NO":
                return Response({
                    "message": "Cannot add the training session. Membership details are required. Update your profile and become a member."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Extract image_location from request data
            image_location = request.data.get('image')
            if image_location:
                _id = str(uuid.uuid4())
                name = request.data.get('name', 'default_name')
                entity_type = 'training'
                # Save image to folder and get the relative path
                image_path = save_image_to_folder(image_location, _id, name, entity_type)
                request.data['image'] = image_path
            else:
                request.data['image'] = "null"

            # Serialize data and save
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if image_location and image_location != "null":
                saved_location = save_image_to_folder(image_location, serializer.instance._id, serializer.instance.name, 'training')
                if saved_location:
                    serializer.instance.image_location = saved_location
                    serializer.instance.save()

            # Capture the current time
            created_at = timezone.now()

            # Send email to EMAIL_HOST_USER
            send_mail(
                'New Training Session Added',
                f'User ID: {request.user.id}\n'
                f'Full Name: {request.user.get_full_name()}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Training ID: {serializer.instance._id}\n'
                f'Training Name: {serializer.instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "success",
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

    def retrieve(self, request, pk=None):
        try:
            training_instance = self.get_object()
        except Training.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TrainingSerializer(training_instance)
        data = serializer.data
        image_path = data.get('image')

        if image_path:
            # Convert image to base64
            image_binary = image_path_to_binary(image_path)
            if image_binary:
                data['image'] = image_binary.decode('utf-8')

        return Response(data)

    def update(self, request, pk=None):
        instance = self.get_object()
        data = request.data
        image_data = data.get('image')
        
        if image_data:
            _id = str(uuid.uuid4())
            name = data.get('name', 'default_name')
            entity_type = 'training'
            # Save image to folder and get the relative path
            image_path = save_image_to_folder(image_data, _id, name, entity_type)
            data['image'] = image_path

        serializer = TrainingSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        
        # If image was updated, handle the file saving
        if image_data and image_data != "null":
            saved_location = save_image_to_folder(image_data, updated_instance._id, updated_instance.name, 'training')
            if saved_location:
                updated_instance.image_location = saved_location
                updated_instance.save()

        return Response({
            "message": "updated successfully",
            "data": TrainingSerializer(updated_instance).data
        })





class UpdateTrainingStatus(generics.GenericAPIView):
    serializer_class = TrainingSerializer

    def put(self, request, _id):
        instance = get_object_or_404(Training, _id=_id)
        serializer = TrainingSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(TrainingSerializer(instance).data, status=status.HTTP_200_OK)
