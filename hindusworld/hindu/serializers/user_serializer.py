from rest_framework import serializers
from ..models import Register
from ..utils import image_path_to_binary


class Register_LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username"]
      

class Verify_LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username","verification_otp"]


class MemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Register
        fields=["id","full_name","father_name","profile_pic","dob","contact_number", "image", "video", "map_location", "experience", "certificate", "achievements", "user_type", "training_type", "email"]


class MemberPicSerializer(serializers.ModelSerializer):
    profile_pic=serializers.SerializerMethodField()
    def get_profile_pic(self, instance):
        filename = instance.profile_pic
        if filename:
            format = image_path_to_binary(filename)
            return format
        return []
    class Meta:
        model = Register
        fields = "__all__"


