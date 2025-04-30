from apps.users.models import User


class UserSearchRepository:
    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def search_users_by_username(search_query: str):
        return User.objects.filter(username__icontains=search_query)