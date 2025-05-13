from django.urls import path

from apps.rooms.views import RoomList, SubmitRoomTasks

urlpatterns = [
        path('api/my-rooms/', RoomList.as_view(), name='my-rooms'),
        path('api/<int:room_id>/submit-tasks/', SubmitRoomTasks.as_view(), name='submit-tasks'),
]
