from rest_framework import serializers
from ..models import TrainingSubCategory
from ..serializers import TrainingCategorySerializer



class TrainingSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSubCategory
        fields = "__all__"