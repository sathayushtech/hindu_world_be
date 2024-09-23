from rest_framework import viewsets, generics
from ..models import TrainingSubCategory
from ..serializers.training_subcategory_serializer import TrainingSubCategorySerializer


class TrainingSubCategoryView(viewsets.ModelViewSet):
    queryset = TrainingSubCategory.objects.all()
    serializer_class = TrainingSubCategorySerializer