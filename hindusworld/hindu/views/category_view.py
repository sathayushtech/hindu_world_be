from rest_framework import viewsets, generics
from ..models import Category,SubCategory

from ..serializers.category_serializer import CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        # Get the Category by ID
        category = self.get_object()

        # Get all SubCategories related to this Category
        subcategories = SubCategory.objects.filter(category_id=category)

        # Retrieve only the SubCategory IDs
        subcategory_ids = subcategories.values_list('_id', 'name')

        # Return the list of SubCategory IDs in the response
        return Response(list(subcategory_ids))