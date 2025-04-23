from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken


class JWTTokenMixin:

    def get_token_from_request(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None
        try:
            return AccessToken(token)
        except Exception:
            return None

    def is_authenticated(self, request):
        token = self.get_token_from_request(request)
        return token is not None

    def set_jwt_cookie(self, response, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            secure=True,  # in production env must be (True)
        )

        return {"refresh": str(refresh), "access": access_token}
