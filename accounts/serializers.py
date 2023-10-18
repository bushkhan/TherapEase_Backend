from datetime import timezone
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'gender')
        
        
        
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'required': True
            }
        }
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        # Save the registration timestamp when the user is created.
        user.registration_timestamp = timezone.now()
        user.save()
        return user
    
    
    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email id already exists!')
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'gender')
        
        
        def update(self, instance, validated_data):
            password = validated_data.pop('password')
            if password:
                instance.set_password(password)
            instance = super().update(instance, validated_data)
            return instance
        
        
    
class LoginSerializer(serializers.Serializer):

        
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    
    def validate(self, attrs):
        email = attrs.get('email').lower()
        print(email)
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("Please give both email and password.")
        
        user_exists = CustomUser.objects.filter(email=email).exists()
        print(user_exists)
        
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exists.')
        

        
        user = authenticate(request=self.context.get('request'), email=email, password=password,)
            
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")
        
        attrs['user'] = user
        return attrs
    
class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    