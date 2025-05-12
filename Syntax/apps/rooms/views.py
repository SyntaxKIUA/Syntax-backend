from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from yaml import serialize

from apps.rooms.models import Room
from apps.rooms.serializers import RoomListSerializer, SubmitTasksSerializer
from apps.rooms.services.room_service import RoomListService


class RoomList(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rooms = RoomListService.get_rooms_for_user(self.request.user)
        if not rooms:
            return Response({"detail":"You're not in any room. "},status=status.HTTP_404_NOT_FOUND)
        serializer = RoomListSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubmitRoomTasks(GenericAPIView):
    serializer_class = SubmitTasksSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request,room_id,  *args, **kwargs):
        room = get_object_or_404(Room, id=room_id)
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            task = RoomListService.post_room_tasks(
                user=request.user,
                room=room,
                file=data["file"],
                title=data["title"],
                description=data.get("description", "")
            )
            return Response({"detail": "Submission successful", "id": task.id}, status=status.HTTP_201_CREATED)

        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




