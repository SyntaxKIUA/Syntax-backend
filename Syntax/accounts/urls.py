from django.urls import path
from dj_rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    path(
        'api/auth/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    )
]
