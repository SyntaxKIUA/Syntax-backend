from apps.search.repositories.user_search import UserSearchRepository, RoomSearchRepository
from apps.search.validations import SearchValidator
from apps.users.models import User


class UserSearchService:
    @staticmethod
    def search_users(search_query):
        SearchValidator.validate_search_query(search_query)
        return UserSearchRepository.search_users_by_username(search_query)

class RoomSearchService:
    @staticmethod
    def search_rooms(search_query):
        SearchValidator.validate_search_query(search_query)
        return RoomSearchRepository.search_rooms_by_name(search_query)