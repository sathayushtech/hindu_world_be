from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import EventCategory, EventSubCategory
from ..serializers import EventCategorySerializer,EventSubCategorySerializer
from ..utils import CustomPagination


class EventCategoryView(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        # Get the Category by ID
        category = self.get_object()

        # Get all SubCategories related to this Category
        subcategories = EventSubCategory.objects.filter(category_id=category)

        # Serialize SubCategories
        serialized_data = EventSubCategorySerializer(subcategories, many=True).data

        # Return the list of SubCategory data in the response
        return Response(serialized_data)