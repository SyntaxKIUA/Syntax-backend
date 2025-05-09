from rest_framework import serializers
from apps.rooms.models import Room

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'name',
            'image',
        ]

