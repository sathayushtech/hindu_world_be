from rest_framework import serializers
from .models import organization,Country
from .utils import image_path_to_binary


class OrgnisationSerializer(serializers.ModelSerializer):
    org_images=serializers.SerializerMethodField()
    def get_image_location(self, instance):
            filename = instance.org_images
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return[]
    class Meta:
        model = organization
        fields = "__all__"


class countrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"