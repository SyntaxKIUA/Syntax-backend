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

from .serializers import (
    ForgotPasswordSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer,
)
from .utils import JWTTokenMixin
from accounts.otp_services import send_sms_kavenegar


User = get_user_model()


class RegisterView(JWTTokenMixin, generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if self.is_authenticated(request):
            return Response(
                {"detail": "You are already logged in."}, status=400
            )

        response = super().create(request, *args, **kwargs)

        user = User.objects.get(username=request.data["username"])
        tokens = self.set_jwt_cookie(response, user)

        response.data = {**tokens, "message": "User registered successfully"}

        return response


class LoginView(JWTTokenMixin, generics.GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if self.is_authenticated(request):
            return Response(
                {"detail": "You are already logged in."}, status=400
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = data.get('user')

        if user is None:
            return Response(
                {"detail": "User not found or invalid credentials."},
                status=400,
            )

        response = Response(
            {
                "message": "Login successful",
            }
        )

        tokens = self.set_jwt_cookie(response, user)

        response.data = {**tokens, **response.data}

        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logout successful"})

        response.delete_cookie("access_token")

        return response


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {"detail": "you most first logout"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        field_type = serializer.validated_data['field_type']

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_path = reverse(
            'password_reset_confirm', kwargs={'uidb64': uid, 'token': token}
        )

        reset_url = (
            f"{settings.FRONTEND_URL}{reset_path}"
            if hasattr(settings, 'FRONTEND_URL')
            else reset_path
        )

        if field_type == "email":
            send_mail(
                subject="password change request",
                message=f"for password reset please click the link:\n{reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(
                {"detail": "link sended to your email"},
                status=status.HTTP_200_OK,
            )

        elif field_type == "phone_number":
            message = (
                f"پسورد جدید شما برای ورود به سایت تست واحد فنی:\n{reset_url}"
            )
            try:
                sms_response = send_sms_kavenegar(user.phone_number, message)
            except Exception as e:
                return Response(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "detail": "password sended with sms",
                    "sms_response": sms_response,
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"detail": "user not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                'uidb64': self.kwargs.get('uidb64'),
                'token': self.kwargs.get('token'),
            }
        )
        return context

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "password is changed!"}, status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
