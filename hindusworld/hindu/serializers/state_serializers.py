from rest_framework import serializers
from ..models import State

class StateSeerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"