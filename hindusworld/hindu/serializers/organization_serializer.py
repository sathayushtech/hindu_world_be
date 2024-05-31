from rest_framework import serializers
from ..models import organization
from ..utils import image_path_to_binary

class OrgnisationSerializer(serializers.ModelSerializer):
    org_images=serializers.SerializerMethodField()
    org_logo=serializers.SerializerMethodField()
    def get_org_images(self, instance):
            filename = instance.org_images
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return[]
    def get_org_logo(self, instance):
            filename = instance.org_logo
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None
    class Meta:
        model = organization
        fields = "__all__"

class OrgnisationSerializer1(serializers.ModelSerializer):
    
    class Meta:
        model = organization
        fields = "__all__"



class OrgnisationSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = organization
        fields = ['status']        