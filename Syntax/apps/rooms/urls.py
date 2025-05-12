from django.urls import path

from apps.rooms.views import RoomList

urlpatterns = [
        path('my-rooms/', RoomList.as_view(), name='my-rooms'),
]
