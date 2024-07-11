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
        fields=["full_name","father_name","profile_pic","dob","contact_number"]


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



# class ResendOtpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Register
#         fields =["username"]


# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Register
#         fields = "__all__"


# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Register
#         fields =["username","password"]

# class VerifySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Register
#         fields =["username","verification_otp"]




# class ResetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Register
#         fields =["forgot_password_otp","password"]


# class UserSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField(required=True)
    
#     class Meta:
#         model=Register
#         fields=['username','password','first_name',"name","dob"]
    
#     def create(self, validated_data):
#         user = super().create(validated_data=validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user