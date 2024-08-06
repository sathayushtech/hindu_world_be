from rest_framework import viewsets, generics
from ..models import Category
from ..serializers.category_serializer import CategorySerializer


class TrainingCategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer