from rest_framework import serializers
from ..models import Category



class TrainingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"