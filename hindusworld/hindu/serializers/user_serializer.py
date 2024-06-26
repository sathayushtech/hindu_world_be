from rest_framework import serializers
from ..models import Register


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Register
        fields = "__all__"



class RegisterSerializer1(serializers.ModelSerializer):
 

    # ConnectModel = ConnectModelSerializer1(many=True, read_only=True)
    class Meta:
        model = Register
        fields ="__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username","password"]

class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username","verification_otp"]


class ResendOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username"]

class ResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["forgot_password_otp","password"]


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    
    class Meta:
        model=Register
        fields=['username','password','first_name',"name","dob"]
    
    def create(self, validated_data):
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user