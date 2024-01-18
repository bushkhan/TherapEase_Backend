from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView,RetrieveUpdateDestroyAPIView
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import CreateUserSerializer, UpdateUserSerializer, LoginSerializer, VerifyAccountSerializer
from knox import views as KnoxViews
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import status
from .emails import send_otp_via_email
from rest_framework.views import APIView
from rest_framework import serializers
# from django.utils import timezone

# Create your views here.
from rest_framework.response import Response
from rest_framework import status

class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({"status":500,"message": "User with this email already exists."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # if CustomUser.objects.filter(email=request.data['email'].lower()).exists():
        #     return Response({"status":400,"message":"User already Exists."},status=status.HTTP_400_BAD_REQUEST)
        try:
            # Try to create the user and send OTP via email
            self.perform_create(serializer)
            
            
            user = serializer.instance  # Get the created user instance
            user_data = CreateUserSerializer(user).data 
            # User creation was successful
            return Response(
                {"status":201,"message": "User created successfully","data":user_data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # User creation failed
            return Response(
                {"message": "User creation failed", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        instance = serializer.save()
        send_otp_via_email(instance.email)

        
        
class VerifyOTP(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email'].lower()
                otp = serializer.data['otp']  
                
                user = CustomUser.objects.filter(email = email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Invalid Email id.'
                    },status=status.HTTP_400_BAD_REQUEST)
                    
                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Wrong otp.'
                    },status=status.HTTP_400_BAD_REQUEST)
                    
                user = user.first()
                user.is_verified = True
                user.save()
                
                return Response({
                        'status': 200,
                        'message': 'Account Verified Successfully.',
                        'data': {}
                    },status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            print(e)
        
class UpdateUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer

class LoginAPI(KnoxViews.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    
    
    def post(self, request, format=None):
        print(request.data)
        if len(request.data["email"]) < 12:
            return Response("error")
        
        if CustomUser.objects.filter(email=request.data['email'].lower()).exists():

            
            serializer = self.serializer_class(data=request.data)
            if  serializer.is_valid(raise_exception=True):

                user = serializer.validated_data['user']

                login(request,user)
                response = super().post(request, format=None)
            else:
                return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response(response.data,status= status.HTTP_200_OK)
        else:
            return Response({"status":400, "message":"Invalid Credentials."},status=status.HTTP_400_BAD_REQUEST)

        
    
    
# class DeleteUnverifiedUserView(APIView):
#     def delete(self, request, user_id):
#         try:
#             user = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response("User not found", status=status.HTTP_404_NOT_FOUND)

#         # Check if the user is unverified and the registration is older than 10 minutes
#         time_difference = timezone.now() - user.registration_timestamp
#         if time_difference.total_seconds() > 600 and not user.is_verified and user.is_superuser != True and user.is_staff != True:
#             user.delete()
#             return Response({
#                 "message": "User Deleted."
#                 }, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({
#                 "userid": user_id,
#                 "message": "Account is still within the 5-minute window or is verified"
#                 }, status=status.HTTP_400_BAD_REQUEST)
