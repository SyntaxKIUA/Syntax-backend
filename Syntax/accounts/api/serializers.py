# serializers.py
from accounts.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DJRegisterSerializer,
)


class CustomRegisterSerializer(DJRegisterSerializer):
    # phone_number = serializers.CharField(required=True)

    class Meta:

        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'phone_number',
            'email',
        ]

        def create(self, validated_data):
            user1 = User.objects.create_user(
                username=validated_data['username'],
                password1=validated_data['password1'],
                password2=validated_data['password2'],
                phone_number=validated_data['phone_number'],
                email=validated_data['email'],
            )

            return user1

    # def get_cleaned_data(self):
    #     data = super().get_cleaned_data()
    #     data['phone_number'] = self.validated_data.get('phone_number', '')
    #     return data
    #
    # def save(self, request):
    #     user = super().save(request)
    #     user.phone_number = self.validated_data.get('phone_number')
    #     user.save()
    #     return user


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )

        if user is None:
            raise serializers.ValidationError("username or password incorrect")
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
