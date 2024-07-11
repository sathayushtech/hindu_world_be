# from rest_framework import serializers
# from ..models import Village
# from ..utils import image_path_to_binary
# 

 
  
# class VillageSerializer(serializers.ModelSerializer):
#     image_location = serializers.SerializerMethodField()

#     def get_image_location(self, instance):
#         filename = instance.image_location
#         if filename:
#             format = image_path_to_binary(filename)
#             return format
#         return None

  

#     def get_block(self,instance):
#         block = instance.block
#         if block:
#             return {
#                 "id":block._id,
#                 "name":block.name,
#                 "district":{
#                     "districtid":str(block.district.pk),
#                     "name":block.district.name,
#                     "state":{
#                         "stateid":str(block.district.state.pk),
#                         "name":block.district.state.name,
#                         "country":{
#                             "countryid":str(block.district.state.country.pk),
#                             "name":block.district.state.country.name
#                         }
#                     }
#                 }
#             }

    
#     class Meta:
#         model = Village
#         fields = "__all__"


