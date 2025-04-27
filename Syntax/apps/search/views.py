from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from apps.search.filters import CustomSearchFilter
from apps.search.serializers import UserSerializer
from apps.search.services.user_search import UserSearchService
from apps.users.models import User
from schema.search.schema_docs import search_user


class SearchUserPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100

@extend_schema(**search_user)
class SearchUserView(ListAPIView):
    """
    Search users by username using the 'search' query parameter.
    """
    serializer_class = UserSerializer
    filter_backends = [CustomSearchFilter]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = SearchUserPagination

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        return UserSearchService.search_users(search_query)