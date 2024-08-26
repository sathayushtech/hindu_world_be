from ..models import ArticleCategory
from rest_framework import serializers



class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'