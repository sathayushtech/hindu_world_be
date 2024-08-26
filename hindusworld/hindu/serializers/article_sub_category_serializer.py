from ..models import ArticleCategory, ArticleSubCategory
from rest_framework import serializers
from ..serializers import ArticleCategorySerializer


class ArticleSubCategorySerializer(serializers.ModelSerializer):
    # category_id=CategorySerializer()
    class Meta:
        model = ArticleSubCategory
        fields = '__all__'