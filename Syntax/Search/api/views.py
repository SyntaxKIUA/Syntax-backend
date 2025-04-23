from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from Search.api.filters import CustomSearchFilter
from Search.api.schema_docs import search_user
from Search.api.serializers import UserSerializer
from Config.throttles import CustomSearchThrottle
from Search.api.validations import SearchValidator


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
            SearchValidator.validate_search_query(search_query)

            queryset = User.objects.all()
            if not search_query:
                return queryset.none()

            return queryset.filter(username__icontains=search_query)