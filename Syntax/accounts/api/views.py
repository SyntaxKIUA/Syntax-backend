from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from .utils import JWTTokenMixin

User = get_user_model()


class RegisterView(JWTTokenMixin, generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if self.is_authenticated(request):
            return Response({"detail": "You are already logged in."}, status=400)

        response = super().create(request, *args, **kwargs)

        user = User.objects.get(username=request.data["username"])
        tokens = self.set_jwt_cookie(response, user)

        response.data = {
            **tokens,
            "message": "User registered successfully"
        }

        return response


class LoginView(JWTTokenMixin, generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if self.is_authenticated(request):
            return Response({"detail": "You are already logged in."}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = data.get('user')

        if user is None:
            return Response({"detail": "User not found or invalid credentials."}, status=400)

        response = Response({
            "message": "Login successful",
        })

        tokens = self.set_jwt_cookie(response, user)

        response.data = {
            **tokens,
            **response.data
        }

        return response


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logout successful"})

        response.delete_cookie("access_token")

        return response