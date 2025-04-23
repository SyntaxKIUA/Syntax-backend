from django.db import connection, transaction
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.authentication import JWTAuthentication

from .schema_docs import register_view_schema, logout_view_schema, user_profile_view_schema
from .serializers import (
    ForgotPasswordSerializer,
    RegisterSerializer,
    PasswordResetConfirmSerializer,
    PrivateProfileSerializer,
    PublicProfileSerializer, UpdateUserSerializer
)
from .utils import JWTTokenMixin
from Accounts.otp_services import send_sms_kavenegar
from ..models import Profile

User = get_user_model()

@extend_schema(**register_view_schema)
class RegisterView(JWTTokenMixin, generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        with transaction.atomic():
            self.user = serializer.save()
            Profile.objects.create(user=self.user)

    def create(self, request, *args, **kwargs):
        if self.is_authenticated(request):
            return Response(
                {"detail": "You are already logged in."},
                status=400
            )

        response = super().create(request, *args, **kwargs)

        tokens = self.set_jwt_cookie(response, self.user)
        response.data = {**tokens, "message": "User registered successfully"}
        return response

@extend_schema(**logout_view_schema)
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logout successful"})

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        field_type = serializer.validated_data["field_type"]

        reset_url = self.generate_reset_url(user)

        if field_type == "email":
            return self.send_email(user.email, reset_url)
        elif field_type == "phone_number":
            return self.send_sms(user.phone_number, reset_url)

        return Response(
            {"detail": "Invalid field_type"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def generate_reset_url(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_path = reverse("password_reset_confirm", kwargs={
                             "uidb64": uid, "token": token})

        frontend_url = getattr(settings, "FRONTEND_URL", "").rstrip("/")
        return f"{frontend_url}{reset_path}" if frontend_url else reset_path

    def send_email(self, email, reset_url):
        send_mail(
            subject="Password Reset Request",
            message=f"برای تغییر رمزعبور خود روی لینک زیر کلیک کنید:\n{reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(
            {"detail": "Link sent to your email"},
            status=status.HTTP_200_OK,
        )

    def send_sms(self, phone_number, reset_url):
        message = f"پسورد جدید شما برای ورود به سایت تست واحد فنی:\n{reset_url}"
        try:
            sms_response = send_sms_kavenegar(phone_number, message)
            return Response(
                {"detail": "Password reset link sent via SMS",
                    "sms_response": sms_response},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
                                         "uidb64": uidb64, "token": token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been changed successfully!"},
            status=status.HTTP_200_OK
        )


@extend_schema(**user_profile_view_schema)
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        connection.queries.clear()

        # fix for is_active
        user = User.objects.select_related("profile").get(username=username)

        if not user:
            return Response(f"The user {username} is not active or does not exist.", status=status.HTTP_404_NOT_FOUND)

        print(user)
        print(connection.queries)
        print(len(connection.queries))

        if request.user.id != user.id:
            profile_serializer = PublicProfileSerializer(user.profile)
        else:
            profile_serializer = PrivateProfileSerializer(user.profile)

        return Response(profile_serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        user = self.request.user.profile


    def patch(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = self.serializer_class(profile, data=request.data, partial=True,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



