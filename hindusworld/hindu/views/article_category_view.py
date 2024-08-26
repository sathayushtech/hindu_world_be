from ..serializers import ArticleCategorySerializer
from ..models import ArticleCategory
from rest_framework import viewsets
from ..pagination import CustomPagination


class ArticleCategoryView(viewsets.ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer
    pagination_class = CustomPagination