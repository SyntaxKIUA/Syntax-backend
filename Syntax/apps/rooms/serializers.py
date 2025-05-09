from rest_framework import serializers

from apps.rooms.models import Room


class GetRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room

        fields = [
            'user',
            'name',
            'image',
            'is_teacher',
            'is_student',
        ]

