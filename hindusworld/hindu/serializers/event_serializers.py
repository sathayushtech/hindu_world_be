from rest_framework import serializers
from ..models import Events
from ..utils import image_path_to_binary

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"




# class EventsSerializer1(serializers.ModelSerializer):
#     brochure = serializers.SerializerMethodField()
#     event_images = serializers.SerializerMethodField()

#     def get_brochure(self, instance):
#         if instance.brochure:
#             return image_path_to_binary(instance.brochure)
#         return None

#     def get_event_images(self, instance):
#         return [image_path_to_binary(img) for img in instance.event_images]

#     class Meta:
#         model = Events
#         fields = '__all__'




class EventsSerializer1(serializers.ModelSerializer):
    # brochure = serializers.SerializerMethodField()
    event_images = serializers.SerializerMethodField()  # Changed to event_image for a single image

    # def get_brochure(self, instance):
    #     if instance.brochure:
    #         return image_path_to_binary(instance.brochure)
    #     return None

    def get_event_images(self, instance):
        # Return only the first image if available
        if instance.event_images:
            first_image = instance.event_images[0] if instance.event_images else None
            return image_path_to_binary(first_image) if first_image else None
        return None

    class Meta:
        model = Events
        fields = ['_id','event_images','name','start_date','end_date','end_time','end_time','location','organizer_name','live_stream_link','category','organization','contact_details']






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
