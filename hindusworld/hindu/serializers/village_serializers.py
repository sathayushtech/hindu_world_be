from rest_framework import serializers
from ..models import Village
from ..utils import image_path_to_binary

# from .member_serializer import MemberSerializer
# from .connect_serializer import ConnectModelSerializer,ConnectModelSerializer1
# from .temple_serializers import TempleSerializer1
# from .goshala_serializer import GoshalaSerializer1
# from .event_serializer import EventSerializer1


# class VillageSerializer(serializers.ModelSerializer):
#     block = serializers.SerializerMethodField()
#     gramdeavatatemples = serializers.SerializerMethodField()
#     othertemples = serializers.SerializerMethodField()
 
  
class VillageSerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    def get_image_location(self, instance):
        filename = instance.image_location
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if representation.get('overall_population') is None:
    #         representation['overall_population'] = '0'
    #     return representation


    def get_block(self,instance):
        block = instance.block
        if block:
            return {
                "id":block._id,
                "name":block.name,
                "district":{
                    "districtid":str(block.district.pk),
                    "name":block.district.name,
                    "state":{
                        "stateid":str(block.district.state.pk),
                        "name":block.district.state.name,
                        "country":{
                            "countryid":str(block.district.state.country.pk),
                            "name":block.district.state.country.name
                        }
                    }
                }
            }

    
    class Meta:
        model = Village
        fields = "__all__"


