from rest_framework.throttling import SimpleRateThrottle

class CustomSearchThrottle(SimpleRateThrottle):
    scope = 'search'

    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return None
        return f'throttle_search_{request.user.id}'
