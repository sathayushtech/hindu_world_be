from rest_framework import viewsets, generics
from ..models import EventSubCategory
from ..serializers.event_subcategory_serializer import EventSubCategorySerializer


class EventSubCategoryView(viewsets.ModelViewSet):
    queryset = EventSubCategory.objects.all()
    serializer_class = EventSubCategorySerializer