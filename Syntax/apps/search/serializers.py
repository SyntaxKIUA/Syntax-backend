from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(source='user.profile.avatar', read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'fullname',
            'avatar'

        ]