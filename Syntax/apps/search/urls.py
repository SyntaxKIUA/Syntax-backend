from django.urls import path, include

from apps.search.views import SearchUserView

urlpatterns = [
    path('api/user/', SearchUserView.as_view(), name='user-search'),
]
