from rest_framework import viewsets, generics
from ..models import EventSubCategory
from ..serializers.event_subcategory_serializer import EventSubCategorySerializer
from ..utils import CustomPagination



class EventSubCategoryView(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = EventSubCategory.objects.all()
    serializer_class = EventSubCategorySerializer