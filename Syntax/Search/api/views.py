from rest_framework.generics import ListAPIView
from Accounts.models import User, Profile
from Search.api.filters import CustomSearchFilter
from Search.api.serializers import UserSerializer


class SearchUserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [CustomSearchFilter]
