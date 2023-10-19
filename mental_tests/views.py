from http.client import NOT_FOUND
from django.shortcuts import render
from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from accounts.models import CustomUser
from .models import AnxietyTest
from rest_framework.permissions import AllowAny
from .serializers import  AnxietyTestMultipleTestSerializer, AnxietyTestSerializer, CustomUserSerializer

# from django.utils import timezone
# Create your views here.

from rest_framework.generics import CreateAPIView
from .models import AnxietyTest
from .serializers import AnxietyTestSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

class AnxietyTestCreateView(CreateAPIView):
    queryset = AnxietyTest.objects.all()
    serializer_class = AnxietyTestSerializer
    permission_classes = [IsAuthenticated, ~IsAdminUser]
    
    
class AnxietyTestDetailView(ListAPIView):
    queryset = AnxietyTest.objects.all()
    serializer_class = AnxietyTestMultipleTestSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed


    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return AnxietyTest.objects.filter(user_id_id=user_id)

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = CustomUser.objects.filter(id=user_id).first()

        if user:
            tests = self.get_queryset()
            user_serializer = CustomUserSerializer(user)

            response_data = {
                "user": user_serializer.data,
                "tests": self.serializer_class(tests, many=True).data
            }

            return Response(response_data)
        else:
            return Response({"detail": "User not found."}, status=404)
    