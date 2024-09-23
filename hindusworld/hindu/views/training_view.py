from rest_framework import viewsets, generics, status
from ..models import Training,Register
from ..serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..utils import save_image_to_folder,image_path_to_binary,video_path_to_binary,save_video_to_folder
import uuid
import os
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework import viewsets, pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100




class TrainingView(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            username = request.user.username
            register_instance = Register.objects.get(username=username)
            user_type = register_instance.user_type

            # Check if the user type is ADMIN
            if user_type != "ADMIN":
                return Response({
                    "message": "Only ADMIN users can create training records."
                }, status=status.HTTP_403_FORBIDDEN)

            data = request.data

            image_data = data.get('image')
            video_data = data.get('video')

            _id = str(uuid.uuid4())
            name = data.get('name', 'default_name')

            if image_data:
                image_path = save_image_to_folder(image_data, _id, name, 'training')
                if image_path:
                    data['image'] = image_path
                else:
                    return Response({
                        "message": "Failed to save image."
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['image'] = "null"

            if video_data:
                video_path = save_video_to_folder(video_data, _id, name, 'training')
                if video_path:
                    data['video'] = video_path
                else:
                    return Response({
                        "message": "Failed to save video."
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['video'] = "null"

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Send email notification to EMAIL_HOST_USER
            send_mail(
                'New Training Session Added',
                f'User ID: {request.user.id}\n'
                f'Contact Number: {register_instance.contact_number}\n'
                f'Full Name: {request.user.get_full_name()}\n'
                f'Training ID: {serializer.instance._id}\n'
                f'Training Name: {serializer.instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "Training session added successfully.",
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
            serializer = TrainingSerializer(training_instance)
            data = serializer.data

            image_path = data.get('image')
            video_path = data.get('video')

            if image_path and image_path != "null":
                img_url = os.path.join(settings.FILE_URL, image_path)
                image_binary = image_path_to_binary(img_url)
                if image_binary:
                    data['image'] = image_binary.decode('utf-8')

            if video_path and video_path != "null":
                vid_url = os.path.join(settings.FILE_URL, video_path)
                video_binary = video_path_to_binary(vid_url)
                if video_binary:
                    data['video'] = video_binary.decode('utf-8')

            return Response(data)

        except Training.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)



    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            for item in data:
                image_path = item.get('image')
                video_path = item.get('video')

                if image_path and image_path != "null":
                    img_url = os.path.join(settings.FILE_URL, image_path)
                    image_binary = image_path_to_binary(img_url)
                    if image_binary:
                        item['image'] = image_binary.decode('utf-8')
                    else:
                        item['image'] = "null"

                if video_path and video_path != "null":
                    vid_url = os.path.join(settings.FILE_URL, video_path)
                    video_binary = video_path_to_binary(vid_url)
                    if video_binary:
                        item['video'] = video_binary.decode('utf-8')
                    else:
                        item['video'] = "null"

            return Response(data)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            username = request.user.username
            register_instance = Register.objects.get(username=username)
            is_admin = register_instance.user_type == "ADMIN"

            if not is_admin:
                return Response({
                    "message": "Only admin users can update training sessions."
                }, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            image_data = data.get('image')
            video_data = data.get('video')

            _id = str(uuid.uuid4())
            name = data.get('name', 'default_name')

            if image_data:
                image_path = save_image_to_folder(image_data, _id, name, 'training')
                if image_path:
                    data['image'] = image_path

            if video_data:
                video_path = save_video_to_folder(video_data, _id, name, 'training')
                if video_path:
                    data['video'] = video_path

            serializer = TrainingSerializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()

            return Response({
                "message": "Training session updated successfully.",
                "data": TrainingSerializer(updated_instance).data
            })

        except Training.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

        except Register.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        










class UpdateTrainingStatus(generics.GenericAPIView):
    serializer_class = TrainingSerializer2

    def put(self, request, training_id):
        try:
            training = Training.objects.get(pk=training_id, status='PENDING')
        except Training.DoesNotExist:
            return Response({
                'message': 'Training with PENDING status not found for the provided ID'
            }, status=status.HTTP_404_NOT_FOUND)

        # Update the status to 'SUCCESS'
        training.status = 'SUCCESS'
        training.save()

        # Serialize the updated training
        serializer = self.get_serializer(training)

        return Response({
            'message': 'success',
            'result': serializer.data
        }, status=status.HTTP_200_OK)




class GetTrainingsByLocation(generics.ListAPIView):
    serializer_class = TrainingSerializer5  # Replace with your actual serializer
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        sub_category = self.request.query_params.get('sub_category')

        # Validate that at least one of the filters is provided
        if not input_value and not category and not sub_category:
            raise ValidationError("At least one of 'input_value', 'category', or 'sub_category' is required.")

        queryset = Training.objects.all()  # Replace with your actual model

        # Check input_value against continent, country, state, and district
        if input_value:
            # Try matching continent
            continent_match = Training.objects.filter(object_id__state__country__continent__pk=input_value)
            if continent_match.exists():
                queryset = continent_match
            else:
                # Try matching country
                country_match = Training.objects.filter(object_id__state__country__pk=input_value)
                if country_match.exists():
                    queryset = country_match
                else:
                    # Try matching state
                    state_match = Training.objects.filter(object_id__state__pk=input_value)
                    if state_match.exists():
                        queryset = state_match
                    else:
                        # Try matching district
                        district_match = Training.objects.filter(object_id__pk=input_value)
                        if district_match.exists():
                            queryset = district_match
                        else:
                            # No match found, return an empty queryset
                            queryset = Training.objects.none()

        # Apply category and subcategory filtering
        if category:
            queryset = queryset.filter(Q(category_id=category) | Q(sub_category_id=category))

        if sub_category:
            queryset = queryset.filter(sub_category_id=sub_category)

        # Order by '_id' to ensure compatibility with pagination
        queryset = queryset.order_by('_id')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)