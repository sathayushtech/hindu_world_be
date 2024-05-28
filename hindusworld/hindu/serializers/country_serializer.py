from rest_framework import serializers
from ..models import Country,organization


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