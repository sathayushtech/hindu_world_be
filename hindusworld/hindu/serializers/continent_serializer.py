from rest_framework import serializers
from ..models import continents
from ..serializers.country_serializer import countrySerializer




class continentsSerializer(serializers.ModelSerializer):
    # continent=countrySerializer(many=True,read_only=True)

    class Meta:
        model=continents
        fields="__all__"