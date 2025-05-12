from rest_framework import serializers
from apps.rooms.models import Room, RoomTaskSubmission


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'name',
            'image',
        ]


class SubmitTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTaskSubmission
        fields = [
            'file',
            'title',
            'description',
        ]