from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserDataSerializer(serializers.ModelSerializer):
    follower_cnt = serializers.IntegerField()
    following_cnt = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'is_superuser', 'joined_date', 'nickname', 'username', 'phone', 'follower_cnt',
            'following_cnt'
        ]


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD