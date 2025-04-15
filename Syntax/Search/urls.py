from django.urls import path, include

from Search.api.views import SearchUserView

urlpatterns = [
    path('api/user/', SearchUserView.as_view(), name='user-search'),
]
