from django.urls import path
from accounts.api.views import (
    ForgotPasswordView,
    RegisterView,
    LogoutView,
    PasswordResetConfirmView,
    UserProfileView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
]
