from rest_framework import serializers
from ..models import Events
from ..utils import image_path_to_binary

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"

class EventsSerializer1(serializers.ModelSerializer):
    brochure = serializers.SerializerMethodField()

    def get_brochure(self, instance):
        if instance.brochure:
            return image_path_to_binary(instance.brochure)
        return None

    class Meta:
        model = Events
        fields = '__all__'
