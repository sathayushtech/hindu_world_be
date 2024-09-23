from rest_framework import serializers
from ..models import EventSubCategory
from ..serializers import EventCategorySerializer
from ..utils import image_path_to_binary



class EventSubCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, instance):

            filename = instance.image
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None
    class Meta:
        model = EventSubCategory
        fields = "__all__"