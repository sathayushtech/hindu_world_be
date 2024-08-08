from rest_framework import viewsets, generics, status
from ..models import Training,Register
from ..serializers import TrainingSerializer,TrainingSerializer2
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..utils import save_image_to_folder,image_path_to_binary,video_path_to_binary,save_video_to_folder
import uuid
import os




class TrainingView(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            username = request.user.username
            register_instance = Register.objects.get(username=username)
            is_member = register_instance.is_member

            if is_member == "NO":
                return Response({
                    "message": "Cannot add the training session. Membership details are required. Update your profile and become a member."
                }, status=status.HTTP_400_BAD_REQUEST)

            image_data = request.data.get('image')
            video_data = request.data.get('video')

            _id = str(uuid.uuid4())
            name = request.data.get('name', 'default_name')

            if image_data:
                image_path = save_image_to_folder(image_data, _id, name, 'training')
                request.data['image'] = image_path
            else:
                request.data['image'] = "null"

            if video_data:
                video_path = save_video_to_folder(video_data, _id, name, 'training')
                request.data['video'] = video_path
            else:
                request.data['video'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

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

    def update(self, request, pk=None):
        instance = self.get_object()
        data = request.data
        image_data = data.get('image')
        video_data = data.get('video')

        _id = str(uuid.uuid4())
        name = data.get('name', 'default_name')

        if image_data:
            image_path = save_image_to_folder(image_data, _id, name, 'training')
            data['image'] = image_path

        if video_data:
            video_path = save_video_to_folder(video_data, _id, name, 'training')
            data['video'] = video_path

        serializer = TrainingSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        return Response({
            "message": "updated successfully",
            "data": TrainingSerializer(updated_instance).data
        })




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