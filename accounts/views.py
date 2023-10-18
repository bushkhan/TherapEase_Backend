from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import CreateUserSerializer, UpdateUserSerializer, LoginSerializer, VerifyAccountSerializer
from knox import views as KnoxViews
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import status
from .emails import send_otp_via_email
from rest_framework.views import APIView
# Create your views here.
class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)    
    
    
    def perform_create(self, serializer):
        instance = serializer.save()
        send_otp_via_email(instance.email)
        
        
class VerifyOTP(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']  
                otp = serializer.data['otp']  
                
                user = CustomUser.objects.filter(email = email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Invalid Email id.'
                    })
                    
                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Something went wrong',
                        'data': 'Wrong otp.'
                    })
                user = user.first()
                user.is_verified = True
                user.save()
                
                return Response({
                        'status': 200,
                        'message': 'Account Verified Successfully.',
                        'data': {}
                    })
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
        serializer = self.serializer_class(data=request.data)
        
        if  serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request,user)
            response = super().post(request, format=None)
        else:
            return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response.data,status= status.HTTP_200_OK)