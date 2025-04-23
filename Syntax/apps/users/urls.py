from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import RegisterView, LogoutView, ForgotPasswordView, PasswordResetConfirmView, UserProfileView, \
    UpdateProfileView

urlpatterns = [
    path("api/register/", RegisterView.as_view(), name="register"),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path(
        "api/forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('api/profile/<str:username>', UserProfileView.as_view(), name='user_profile'),

    path('api/update-user-profile', UpdateProfileView.as_view(), name='update_user_profile'),
]
