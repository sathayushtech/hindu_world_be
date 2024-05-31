from rest_framework import serializers
from ..models import Country,organization
from ..utils import image_path_to_binary


class countrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


# class countrySerializer1(serializers.ModelSerializer):
#     continent = serializers.SerializerMethodField()
#     # organization_count = serializers.SerializerMethodField()
#     # continent = ContinentSerializer()

#     def get_continent(self, instance):
#         continent = instance.continent
#         return {
#             "name": continent.name
#         }

#     # def get_organization_count(self, instance):
#     #     return organization.objects.filter(country=instance).count()

#     class Meta:
#         model = Country
#         fields = "__all__"



class CountrySerializer1(serializers.ModelSerializer):
    image_location=serializers.SerializerMethodField()
    def get_image_location(self, instance):
            filename = instance.image_location
            print(filename,"yrtyh")
            if filename:
                format= image_path_to_binary(filename)
                print(format,"******************")
                return format
            return None
    
    class Meta:
        model = Country
        fields = "__all__"