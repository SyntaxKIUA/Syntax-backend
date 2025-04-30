import re
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import serializers

from apps.users.models import Profile
from apps.users.validations.validations import ValidatorForgotPassword

# from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField(label="Email, phone number or username")
    iran_phone_regex = re.compile(r'^09\d{9}$')

    def validate_identifier(self, value):
        return ValidatorForgotPassword.clean_identifier(value)

    def validate(self, data):
        identifier = data.get('identifier')
        field = ValidatorForgotPassword.get_identifier_field(identifier)
        lookup = {field: identifier}
        try:
            user = User.objects.get(**lookup)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        data['user'] = user
        data['field_type'] = field
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):

        uidb64 = self.context.get('uidb64')
        token = self.context.get('token')

        if not uidb64 or not token:
            raise serializers.ValidationError("url not correct")

        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError(
                "The password and its confirmation do not match."
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
        except Exception:
            raise serializers.ValidationError("The user ID is invalid.")

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError("The user does not exist.")

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                "The token is either invalid or has expired."
            )

        validate_password(data['new_password'], user=user)

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PrivateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    class Meta:
        model = Profile
        fields = [
            'username',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'bio',
            'professional',
            'followings_count',
            'followers_count',
            'posts_count',
            'avatar'
        ]


class PublicProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'bio',
            'professional',
            'followings_count',
            'followers_count',
            'posts_count',
            'avatar'
        ]


class UpdateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    birth_date = serializers.CharField(source='user.birth_date', required=False)

    class Meta :
        model = Profile
        fields = [
            'username', 'first_name', 'last_name', 'birth_date', 'avatar', 'bio', 'professional'

        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        user = instance.user


        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
