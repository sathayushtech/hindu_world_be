from rest_framework import serializers
from ..models import District
from ..utils import image_path_to_binary


class DistrictSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    def get_image_location(self, instance):
        filename = instance.image_location
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None





    class Meta:
        model = District
        fields = "__all__"