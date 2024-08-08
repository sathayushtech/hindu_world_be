from rest_framework import serializers
from ..models import TrainingCategory



class TrainingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCategory
        fields = "__all__"