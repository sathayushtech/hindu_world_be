from ..serializers import UserSerializer,LoginSerializer,VerifySerializer,ResetSerializer,ResetSerializer,ResendOtpSerializer
from rest_framework import viewsets,generics
from ..models import Register
from rest_framework .views import APIView,status
from rest_framework .response import Response
from ..enums.user_status_enum import UserStatus
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import generate_otp, validate_email,send_email,send_sms,Resend_sms
from django.contrib.auth import authenticate








# class Registerview(viewsets.ModelViewSet):
#     queryset = Register.objects.all()
#     serializer_class = RegisterSerializer

#     def list(self, request):
#         users = Register.objects.all()
#         serializer = RegisterSerializer1(users, many=True)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         instance = serializer.save()
#         return Response({
#             "status": 200,
#             "result": RegisterSerializer(instance).data,
#             "message": "success"
#         })
    
#     def retrieve(self, request, pk=None):  # Change the method name from GetById to retrieve
#         instance = self.get_object()
#         serializer = RegisterSerializer1(instance)  # Use RegisterSerializer1 for single instance
#         return Response({
#             "message": "retrieved successfully",
#             "data": serializer.data
#         })

#     def update(self, request, pk=None):
#         instance = self.get_object()
#         serializer = RegisterSerializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         updated_instance = serializer.save()
#         return Response({
#             "message": "updated successfully",
#             "data": RegisterSerializer(updated_instance).data
#         })
    
#     def destroy(self, request, pk=None):
#         instance = self.get_object()
#         instance.status = 'inactive'  # Marking as inactive instead of actually deleting
#         instance.save()
#         return Response({"message": "soft deleted successfully"})


    
# class LoginApiView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     def post(self,request):
#         username = request.data["username"]
#         print(username,"11111111")
#         password = request.data["password"]
#         print(password,"222222222")
        
#         try:
#             a = Register.objects.get(username=username)

#         except Register.DoesNotExist:
#             return Response({
#                 "status":400,
#                 "message":"invalid username"
#             })
#         if a.password == password:
#             if a.status != UserStatus.ACTIVE.value:
#                 return Response({
#                     "error": "Verify account before login"
#                 })
            
#             return Response({
#                 "status":200,
#                 "message":"login succesfully",
#                 # "refresh_token":"refresh"
        
#             })
#         else:
#             return Response({
#                 "status":200,
#                 "message":"invalid password"
#         })



 
# class LoginApiView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         username = data.get('username')
#         password = data.get('password')
        
#         user = authenticate(username=username, password=password)
        
#         if user is None:
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





class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        try:
            user = Register.objects.get(username=username)
        except Register.DoesNotExist:
            user = None

        if user is None or not user.check_password(password):
            return Response({
                'message': "Invalid username or password"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is active
        if user.status != UserStatus.ACTIVE.value:
            return Response({
                "error": "Verify account before login"
            }, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.get_username(),
            'user_id': user.id
        }, status=status.HTTP_200_OK)






# class Registerview(generics.GenericAPIView):
#     serializer_class=UserSerializer
#     def post(self, request, *args, **kwargs):
#         print("bgvfdsa")
#         data = request.data
#         serializer = UserSerializer(data=data)
#         print(serializer,"oiuhygt")
#         serializer.is_valid(raise_exception=True)  
#         serializer.save()
#         return Response({
#             'message': "Registration Successful, Please check the account"
#         }, status=status.HTTP_201_CREATED)
            





class Registerview(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        
        if Register.objects.filter(username=data.get('username')).exists():
            return Response({
                'message': "User already exists"
            }, status=status.HTTP_409_CONFLICT)
        
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'message': "Registration Successful, Please check the account"
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': "Invalid data",
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



    
class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifySerializer
    
    def post(self, request):
       
        data = request.data
        username = data['username']
        print(username,"1aaaaaaaaaaaaaaaaa")
        verification_otp = data['verification_otp']
        print(verification_otp,"ooooooooooooooooooooooo")
        try:
            user = Register.objects.using('login_db').get(username=username)
        except Register.DoesNotExist:
            return Response({
                "status":400,
                "message":"invalid username"
            })
        print(user,"a22222222222222222222222")

        if user.verification_otp == verification_otp:
            user.verification_otp = None
            user.is_verified = True
            user.status = UserStatus.ACTIVE.value
            v=user.save()
            print(v,"a333333333333333333333")
            return Response({
                'message': 'Account Verified'
            })
            
        return Response({
            'message':'Something went Wrong',
            'data': 'Invalid OTP'
        })






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





class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetSerializer
    

    def put(self,request):
        otp = request.data["forgot_password_otp"]
        password = request.data["password"]

        if not otp or not password:
            return Response({
                "status":400,
                "message":"required otp and resetpassword"
            })
        try:
            user=Register.objects.using('login_db').get(forgot_password_otp=otp)
        except Register.DoesNotExist:
            return Response({
                "status":400,
                "message":"invalid otp, please enter valid otp"
            })
        if user.password==password:
            return Response({
                "status": 400,
                "message": "New password should not be the same as the old password."
            })
        else:
            user.forgot_password_otp=None
            user.password=password
            user.save()
            return Response({
                "status":200,
                "message":"reset password succesfully"
            })

        