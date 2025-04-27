from rest_framework.exceptions import ValidationError

class SearchValidator:
    @staticmethod
    def validate_search_query(search_query):
        if not search_query:
            raise ValidationError("The 'search' parameter is required.")

        if len(search_query) < 3:
            raise ValidationError("Search term must be at least 3 characters long.")

        return search_query
