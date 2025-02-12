# # serializers.py
# from accounts.models import User
# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from dj_rest_auth.registration.serializers import (
#     RegisterSerializer as DJRegisterSerializer,
# )
# from phonenumber_field.serializerfields import PhoneNumberField
#
#
# class CustomRegisterSerializer(DJRegisterSerializer):
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)
#     phone_number = PhoneNumberField(region="IR")
#
#     def get_cleaned_data(self):
#         data = super().get_cleaned_data()
#         data['phone_number'] = self.validated_data.get('phone_number', '')
#         return data
#
#     def save(self, request):
#         user = super().save(request)
#         user.phone_number = self.validated_data.get('phone_number')
#         user.save()
#         return user
#
#
# class CustomLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, data):
#         user = authenticate(
#             username=data.get("username"), password=data.get("password")
#         )
#
#         if user is None:
#             raise serializers.ValidationError("username or password incorrect")
#         refresh = RefreshToken.for_user(user)
#         return {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         }
