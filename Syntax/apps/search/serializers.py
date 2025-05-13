from rest_framework import serializers

from apps.rooms.models import Room
from apps.users.models import User


class UserSearchSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='user.profile.avatar', read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'fullname',
            'avatar'

        ]

class RoomSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'name',
            'image'
        ]