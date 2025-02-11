from rest_framework import generics
from rest_framework.response import Response
from .serializers import CustomRegisterSerializer, CustomLoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
