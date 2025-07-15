from django.core.cache import cache
from django.db import transaction
from rest_framework.response import Response
from apps.users.models import Profile, User
from apps.users.repositories.user_repo import ProfileRepository, UpdateProfileRepository, UserNotFoundError
from apps.users.serializers import PublicProfileSerializer, PrivateProfileSerializer, UpdateUserSerializer
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def register_user(validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            Profile.objects.create(user=user)
            return user

class GetProfileService:
    @staticmethod
    def user_profile(request_user, username):
        cache_key = f"user_profile:{request_user.id}:{username}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data, None

        try:
            user = ProfileRepository.get_by_username(username)

            if request_user.id != user.id:
                profile_serializer = PublicProfileSerializer(user.profile)
            else:
                profile_serializer = PrivateProfileSerializer(user.profile)

            data = profile_serializer.data
            cache.set(cache_key, data, timeout=600)

            return data, None

        except UserNotFoundError as e:
            return {"error": str(e)}, "User not found"


class LogoutService:
    @staticmethod
    def logout():
        response = Response({"message": "Logout successful"})

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")



class UpdateService:
    @staticmethod
    def update_user(request):
        profile = UpdateProfileRepository.get_profile(request)
        if not profile:
            raise ValueError("Profile does not exist")
        serializer = UpdateUserSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cache_key = f"user_profile:{request.user.id}:{request.user.username}"
        cache.delete(cache_key)

        return serializer


