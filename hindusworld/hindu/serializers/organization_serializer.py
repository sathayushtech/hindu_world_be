from rest_framework import serializers
from ..models import Organization
from ..utils import image_path_to_binary



class OrgnisationSerializer(serializers.ModelSerializer):
    org_images = serializers.SerializerMethodField()
    org_logo = serializers.SerializerMethodField()
    govt_id_proof = serializers.SerializerMethodField()  # New field for government-issued ID proof

    def get_org_images(self, instance):
        filename = instance.org_images
        if filename:
            format = image_path_to_binary(filename)
            return format
        return []

    def get_org_logo(self, instance):
        filename = instance.org_logo
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None

    def get_govt_id_proof(self, instance):
        filename = instance.govt_id_proof
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None

    class Meta:
        model = Organization
        fields = '__all__'
    


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['org_images', 'org_logo', 'chairman', 'web_url', 'est_by','country','reg_id','est_date','location','organization_name','web_url','org_detail','geo_site','organization_members','sub_category_id','object_id','govt_id_proof']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation



       
    class Meta:
        model = Organization
        fields = "__all__"



    
    
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
