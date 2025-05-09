from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.rooms.serializers import RoomListSerializer
from apps.rooms.services.room_service import RoomListService


class RoomList(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rooms = RoomListService.get_rooms_for_user(self.request.user)
        if not rooms:
            return Response({"detail":"You're not in any room. "},status=status.HTTP_404_NOT_FOUND)
        serializer = RoomListSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



