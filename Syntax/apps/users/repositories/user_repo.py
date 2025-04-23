from apps.users.models import User


class ProfileRepository:
    @staticmethod
    def get_by_username(username):
        return User.objects.select_related("profile").filter(username=username).first()


class UpdateProfileRepository:
    @staticmethod
    def get_profile(request):
        try:
            return request.user.profile
        except AttributeError:
            raise ValueError("User does not have a profile")


