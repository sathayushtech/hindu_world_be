from rest_framework import serializers
from ..models import Register
from ..utils import image_path_to_binary
import base64

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
        fields=["full_name","father_name","profile_pic","dob","contact_number"]


class MemberPicSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    def get_profile_pic(self, instance):
        profile_pic_path = instance.profile_pic
        if profile_pic_path:
            try:
                with open(profile_pic_path, 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return encoded_string
            except FileNotFoundError:
                return None
        return None

    class Meta:
        model = Register
        fields = ["full_name", "father_name", "profile_pic", "dob", "contact_number"]

# class MemberPicSerializer(serializers.ModelSerializer):
#     profile_pic=serializers.SerializerMethodField()
#     def get_profile_pic(self, instance):
#         filename = instance.profile_pic
#         if filename:
#             format = image_path_to_binary(filename)
#             return format
#         return []
    
#     class Meta:
#         model = Register
#         fields = "__all__"



