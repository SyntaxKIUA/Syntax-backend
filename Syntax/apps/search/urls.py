from django.urls import path, include

from apps.search.views import SearchUserView, RoomSearchView

urlpatterns = [
    path('api/user/', SearchUserView.as_view(), name='user-search'),
    path('api/room/', RoomSearchView.as_view(), name='room-search'),
]
