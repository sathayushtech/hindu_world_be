from rest_framework import viewsets, generics
from ..models import TrainingCategory
from ..serializers.training_category_serializers import TrainingCategorySerializer


class TrainingCategoryView(viewsets.ModelViewSet):
    queryset = TrainingCategory.objects.all()
    serializer_class = TrainingCategorySerializer
