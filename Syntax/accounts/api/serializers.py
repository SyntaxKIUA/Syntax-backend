from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")

        return {'user': user}


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        provided_fields = [
            field for field in ['email', 'phone_number'] if data.get(field)
        ]
        if len(provided_fields) != 1:
            raise serializers.ValidationError(
                "pleas enter ones of phone number or email or username"
            )

        field = provided_fields[0]
        identifier = data.get(field)

        lookup = {field: identifier}
        try:
            user = User.objects.get(**lookup)
        except User.DoesNotExist:
            raise serializers.ValidationError("user not found!")

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
