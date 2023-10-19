from rest_framework import serializers
from .models import AnxietyTest
from django.contrib.auth import authenticate

from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'gender')

class AnxietyTestSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(source='user_id', read_only=True)  # Include the user data as a nested serializer

    class Meta:
        model = AnxietyTest
        fields = '__all__'
        
        
class AnxietyTestMultipleTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnxietyTest
        fields = '__all__'