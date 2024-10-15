from rest_framework import serializers
from ..models import Events
from ..utils import image_path_to_binary

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"






class EventsSerializer1(serializers.ModelSerializer):
    brochure = serializers.SerializerMethodField()
    event_images = serializers.SerializerMethodField()  
    relative_time = serializers.SerializerMethodField()


    def get_brochure(self, instance):
        if instance.brochure:
            return image_path_to_binary(instance.brochure)
        return None

    def get_event_images(self, instance):
        # Return only the first image if available
        if instance.event_images:
            first_image = instance.event_images[0] if instance.event_images else None
            return image_path_to_binary(first_image) if first_image else None
        return None
    
    def get_relative_time(self, obj):
        return obj.relative_time

    class Meta:
        model = Events
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['event_details', 'event_status', 'sub_category', 'category', 'live_stream_link','event_images','contact_details','end_date','start_date','location','organizer_name','brochure','name']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation



class EventSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Events
        fields = ['status']        







class EventsSerializer3(serializers.ModelSerializer):
    event_image = serializers.SerializerMethodField()  # Renaming to event_image for single image

    def get_event_image(self, instance):
        # Return only the first image if available
        if instance.event_images:
            first_image = instance.event_images[0] if instance.event_images else None
            return image_path_to_binary(first_image) if first_image else None
        return None

    class Meta:
        model = Events
        fields = ['_id', 'event_image', 'name']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['event_image', 'name']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation


