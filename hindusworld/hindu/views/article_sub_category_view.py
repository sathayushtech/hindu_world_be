from rest_framework import viewsets
from ..models import ArticleSubCategory
from ..serializers import ArticleSubCategorySerializer
from ..pagination import CustomPagination

class ArticleSubCategoryView(viewsets.ModelViewSet):
    queryset = ArticleSubCategory.objects.all()
    serializer_class = ArticleSubCategorySerializer
    pagination_class = CustomPagination