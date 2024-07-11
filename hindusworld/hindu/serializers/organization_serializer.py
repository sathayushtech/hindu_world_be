from rest_framework import serializers
from ..models import Organization
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
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if representation.get('org_images') in [None, 'null']:
    #         representation['org_images'] = "image not found"
    #     if representation.get('org_logo') in [None, 'null']:
    #         representation['org_logo'] = "image not found"
    #         return representation

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['org_images', 'org_logo', 'chairman', 'web_url', 'est_by','reg_id','est_date','location','organization_name','web_url','org_detail','geo_site','organization_members']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation



       
    class Meta:
        model = Organization
        fields = "__all__"


    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # Fields to check for empty or null values
    #     fields_to_check = ['org_images', 'org_logo', 'chairman', 'web_url', 'est_by','reg_id','est_date','location','organization_name','web_url','org_detail','geo_site','organization_members']
    #     for field in fields_to_check:
    #         if representation.get(field) in [None, '', 'null','-']:
    #             representation[field] = "data not found"
  
    #     return representation
    
    
class OrgnisationSerializer1(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = "__all__"



class OrgnisationSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = ['status']        


class OrganizationSerializer3(serializers.ModelSerializer):
 
    image_location = serializers.SerializerMethodField()
    # object_id=serializers.SerializerMethodField()
