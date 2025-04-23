from rest_framework import serializers

from Accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='user.profile.avatar', read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'fullname',
            'avatar'

        ]