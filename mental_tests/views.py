from django.shortcuts import render
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from .models import AnxietyTest
from rest_framework.permissions import AllowAny
from .serializers import  AnxietyTestSerializer

# from django.utils import timezone
# Create your views here.

from rest_framework.generics import CreateAPIView
from .models import AnxietyTest
from .serializers import AnxietyTestSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

class AnxietyTestCreateView(CreateAPIView):
    queryset = AnxietyTest.objects.all()
    serializer_class = AnxietyTestSerializer
    permission_classes = [IsAuthenticated, ~IsAdminUser]
    
    

class AnxietyTestDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AnxietyTest.objects.all()
    serializer_class = AnxietyTestSerializer
    