from apps.search.repositories.user_search import UserSearchRepository
from apps.search.validations import SearchValidator
from apps.users.models import User


class UserSearchService:
    @staticmethod
    def search_users(search_query):
        SearchValidator.validate_search_query(search_query)

        if not search_query:
            return UserSearchRepository.get_all_users()

        return UserSearchRepository.search_users_by_username(search_query)