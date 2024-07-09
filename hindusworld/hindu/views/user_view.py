# from ..serializers import UserSerializer,LoginSerializer,VerifySerializer,ResetSerializer,ResetSerializer,ResendOtpSerializer,RegisterSerializerl,VerifyOtpSerializer
from ..serializers import Register_LoginSerializer,Verify_LoginSerializer,MemberSerializer,MemberPicSerializer,ResendOtpSerializer
from rest_framework import viewsets,generics
from ..models import Register
from rest_framework .views import APIView,status
from rest_framework .response import Response
from ..enums.user_status_enum import UserStatus
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import validate_email,send_email,send_sms,generate_otp,Resend_sms
from django.contrib.auth import authenticate
from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..utils import save_profile_image_to_folder
from datetime import datetime

     
     

class Register_LoginView(generics.GenericAPIView):
    serializer_class = Register_LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        
        if not username:
            return Response({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Register.objects.using('login_db').get(username=username)
            print(user)
            # Username already exists, update OTP
            otp = generate_otp()
            print(otp,"1111111111")

            user.verification_otp = otp
            user.verification_otp_created_time = timezone.now()
            user.save(using='login_db')
            send_sms(username, otp)
            print(otp,'000000000000000000')
            message = "Login successful and OTP sent successfully"
        except Register.DoesNotExist:
            # Username does not exist, create new user and set OTP
            otp = generate_otp()
            print(otp,"222222222222222222222222")
            
            user = Register.objects.using('login_db').create(username=username, verification_otp=otp, verification_otp_created_time=timezone.now())
            user.save(using='login_db')
          
            print(otp,'3333333333333333333')
            send_sms(username, otp)
            # user.save()
            print(otp,'44444444444444')
            message = "OTP sent successfully"
        
        
        
        return Response({"otp": message}, status=status.HTTP_200_OK)

    
# class Validate_LoginOTPView(generics.GenericAPIView):
#     serializer_class = Verify_LoginSerializer
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         verification_otp = request.data.get('verification_otp')
#         try:
#             user = Register.objects.using('login_db').get(username=username, verification_otp=verification_otp)
#             if user:
#                 if user.verification_otp_created_time < timezone.now() - timezone.timedelta(hours=24):
#                     return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
#                 # Update user status to ACTIVE
#                 user.status = 'ACTIVE'
#                 user.save(using='login_db')
#                 refresh = RefreshToken.for_user(user)
#                 access_token = refresh.access_token
#                 return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'username': user.get_username(),
#             'user_id': user.id
#         }, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid credentials', 'status': '401'}, status=status.HTTP_401_UNAUTHORIZED)
#         except Register.DoesNotExist:
#             return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        


class Validate_LoginOTPView(generics.GenericAPIView):
    serializer_class = Verify_LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        verification_otp = request.data.get('verification_otp')
        
        try:
            user = Register.objects.using('login_db').get(username=username)
        except Register.DoesNotExist:
            return Response({"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.verification_otp != verification_otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_otp_created_time < timezone.now() - timezone.timedelta(hours=24):
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update user status to ACTIVE
        user.status = 'ACTIVE'
        user.save(using='login_db')
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
            'username': user.get_username(),
            'user_id': user.id
        }, status=status.HTTP_200_OK)


class ResendOTPView(generics.GenericAPIView):
    serializer_class = ResendOtpSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = Register.objects.using('login_db').get(username=username)
            otp = generate_otp()
            user.verification_otp = otp
            user.verification_otp_resend_count += 1  # Increment resend count
            user.verification_otp_created_time = timezone.now()  
            user.save(using='login_db')  # Save the new OTP to the database
            
            Register_LoginView().send_sms(username, otp)
            return Response({"otp": "otp sent successfully"}, status=status.HTTP_200_OK)
        except Register.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class MemberDetailsViews(viewsets.ModelViewSet):
    queryset=Register.objects.all()
    serializer_class=MemberPicSerializer

class UpdateMemberDetails(generics.GenericAPIView):
    serializer_class = MemberSerializer
    def put(self, request, id):
        # Retrieve the instance
        instance = get_object_or_404(Register, id=id)
        # Retrieve image_location from request data
        profile_pic = request.data.get('profile_pic')
        print(profile_pic, "vfvfv")
        # Make a mutable copy of request.data and set image_location to "null"
        mutable_data = request.data.copy()
        mutable_data['profile_pic'] = "profile_pic"
        # Instantiate the serializer with the mutable copy of data
        serializer = self.get_serializer(instance, data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_member'] = True
        serializer.save()
        # If image_location is provided and not "null", save the image
        if profile_pic and profile_pic != "null":
            saved_location = save_profile_image_to_folder(profile_pic, serializer.instance.id, serializer.instance.full_name)
            if saved_location:
                serializer.instance.profile_pic = saved_location
                print(serializer.instance.profile_pic, "referg")
                serializer.instance.save()
        # Return the response with the updated data
        return Response(MemberSerializer(serializer.instance).data, status=status.HTTP_200_OK)





# class Registerview(generics.GenericAPIView):
#     serializer_class=UserSerializer
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = UserSerializer(data=data)
#         print(serializer,"oiuhygt")
#         serializer.is_valid(raise_exception=True)  
#         serializer.save()
#         return Response({
#             'message': "Registration Successful, Please check the account"
#         }, status=status.HTTP_201_CREATED)
            

# class LoginApiView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         username = data.get('username')
#         password = data.get('password')

#         try:
#             user = Register.objects.get(username=username)
#         except Register.DoesNotExist:
#             user = None

#         if user is None or not user.check_password(password):
#             return Response({
#                 'message': "Invalid username or password"
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Check if the user is active
#         if user.status != UserStatus.ACTIVE.value:
#             return Response({
#                 "error": "Verify account before login"
#             }, status=status.HTTP_400_BAD_REQUEST)

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'username': user.get_username(),
#             'user_id': user.id
#         }, status=status.HTTP_200_OK)
      

    
# class VerifyOtpView(generics.GenericAPIView):
#     serializer_class = VerifySerializer
    
#     def post(self, request):
       
#         data = request.data
#         username = data['username']
#         print(username,"1aaaaaaaaaaaaaaaaa")
#         verification_otp = data['verification_otp']
#         print(verification_otp,"ooooooooooooooooooooooo")
#         try:
#             user = Register.objects.using('login_db').get(username=username)
#         except Register.DoesNotExist:
#             return Response({
#                 "status":400,
#                 "message":"invalid username"
#             })
#         print(user,"a22222222222222222222222")

#         if user.verification_otp == verification_otp:
#             user.verification_otp = None
#             user.is_verified = True
#             user.status = UserStatus.ACTIVE.value
#             v=user.save()
#             print(v,"a333333333333333333333")
#             return Response({
#                 'message': 'Account Verified'
#             })
            
#         return Response({
#             'message':'Something went Wrong',
#             'data': 'Invalid OTP'
#         })
    
class ResendOtp(generics.GenericAPIView):
    serializer_class = ResendOtpSerializer

    def post(self,request):
        username = request.data["username"]
        try:
            user = Register.objects.using('login_db').get(username=username)
        except Register.DoesNotExist:
            return Response({
                "status": 400,
                "message": "Invalid username, please enter valid username"
            })
        try:

            if validate_email(username):
                otp = generate_otp()
                user.verification_otp=otp
                user.save()
                send_email(username,otp)
                return Response({
                    "status":200,
                    "message":"resent otp succesfull, please check your Email"
                })
            
            else:
                otp = generate_otp()
                user.verification_otp=otp
                user.save()
                Resend_sms(username,otp)
                return Response({
                    "status":200,
                    "message":"resent otp succesfull, please check your mobile number"
                })
        except:
            return Response({
                "status":200,
                "message":"invalid otp"
            })
        
class ForgotOtp(generics.GenericAPIView):
    serializer_class = ResendOtpSerializer

    def post(self,request):
        username = request.data["username"]
        try:
            user = Register.objects.using('login_db').get(username=username)
        except Register.DoesNotExist:
            return Response({
                "status": 400,
                "message": "Invalid username, please enter valid username"
            })
        if validate_email(username):
            otp = generate_otp()
            send_email(username,otp)
            user.forgot_password_otp=otp
            user.save()
            return Response({
                "status":200,
                "message":"otp succesfully, please check your Email"
            })
        
        else:
            otp = generate_otp()
            user.forgot_password_otp=otp
            user.save()
            send_sms(username,otp)
            return Response({
                "status":200,
                "message":"otp sent succesfully, please check your mobile number"
            })
        


        