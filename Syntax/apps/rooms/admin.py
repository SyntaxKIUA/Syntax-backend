from django.contrib import admin

from apps.rooms.apps import RoomConfig
from apps.rooms.models import Room, RoomMembership

admin.site.register(Room)
admin.site.register(RoomMembership)