from rest_framework.pagination import PageNumberPagination


class SearchPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100