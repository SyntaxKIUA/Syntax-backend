from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from apps.Utils.search.searchutils import SearchPagination
from apps.schema.search.schema_docs import search_user
from apps.search.filters import CustomSearchFilter
from apps.search.serializers import UserSearchSerializer, RoomSearchSerializer
from apps.search.services.user_search import UserSearchService, RoomSearchService


@extend_schema(**search_user)
class SearchUserView(ListAPIView):
    serializer_class = UserSearchSerializer
    filter_backends = [CustomSearchFilter]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = SearchPagination

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        return UserSearchService.search_users(search_query)

class RoomSearchView(ListAPIView):
    serializer_class = RoomSearchSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SearchPagination

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        return RoomSearchService.search_rooms(search_query)