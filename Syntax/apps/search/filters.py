from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ['username', 'first_name', 'last_name']

