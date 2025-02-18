from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.api.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", LogoutView.as_view(), name="logout"),

]
