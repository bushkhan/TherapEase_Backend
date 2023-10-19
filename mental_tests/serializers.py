from rest_framework import serializers
from .models import AnxietyTest
from django.contrib.auth import authenticate


class AnxietyTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnxietyTest
        fields = '__all__'