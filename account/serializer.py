from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Account Not Found')
        return data

    def get_jwt_token(self, data):
        user = authenticate(username= data['username'], password=data['password'])
        if not user:
            return {
                'Message': 'Invalid credentials',
                'Data': {},
                'Status': False
            }
        refresh = RefreshToken.for_user(user)
        return {
            'Message': 'Login success',
            'Data': {'token': {'refresh': str(refresh),'access': str(refresh.access_token),}},
            'Status': True
        }
