from rest_framework import serializers
from ..models import SubCategory
from ..serializers import CategorySerializer



class SubCategorySerializer(serializers.ModelSerializer):
    category_id=CategorySerializer()
    class Meta:
        model = SubCategory
        fields = "__all__"