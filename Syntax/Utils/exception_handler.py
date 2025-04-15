from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        return Response({"detail": "You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, AuthenticationFailed):
        return Response({"detail": "Authentication credentials were invalid."}, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, PermissionDenied):
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    return response
