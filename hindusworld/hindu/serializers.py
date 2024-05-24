from rest_framework import serializers
from .models import organization,Country


class OrgnisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = organization
        fields = "__all__"


class countrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"