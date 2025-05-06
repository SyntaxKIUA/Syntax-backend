from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from apps.users.models import User

class UserNotFoundError(Exception):
    """Exception For Not Founding User"""
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

class ProfileRepository:
    @staticmethod
    def get_by_username(username):
        try:
            user = User.objects.select_related("profile").get(username=username)
            return user
        except User.DoesNotExist:
            raise UserNotFoundError(f"User with username '{username}' does not exist.")
        except (DatabaseError, ValueError, TypeError) as e:
            raise Exception(f"Unexpected error occurred: {str(e)}")


class UpdateProfileRepository:
    @staticmethod
    def get_profile(request):
        try:
            return request.user.profile
        except AttributeError:
            raise ValueError("User does not have a profile")


