from rest_framework import permissions

from apps.rooms.models import RoomMembership


class IsRoomAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        room_id = view.kwargs.get('room')
        return RoomMembership.objects.filter(room_id=room_id, user=request.user, is_admin= True).exists()