from django.contrib import admin

from apps.rooms.apps import RoomConfig
from apps.rooms.models import Room, RoomMembership, RoomTaskSubmission

admin.site.register(Room)
admin.site.register(RoomMembership)
admin.site.register(RoomTaskSubmission)