import pytest
from django.core.exceptions import ValidationError
from accounts.models import User


@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="testpassword",
        phone_number="09876543211",
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.check_password("testpassword")
    assert str(user) == "testuser"


@pytest.mark.django_db
def test_create_user_without_email_raises_error():
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="",
            username="testuser",
            password="testpassword",
            phone_number="09876543211",
        )


@pytest.mark.django_db
def test_create_user_without_username_raises_error():
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="test@example.com",
            username="",
            password="testpassword",
            phone_number="09876543211",
        )


@pytest.mark.django_db
def test_create_user_without_password_raises_error():
    with pytest.raises(ValueError, match='Phone number is required'):
        User.objects.create_user(
            email="test@example.com",
            username="usertest",
            password="",
            phone_number="09876543211",
        )


@pytest.mark.django_db
def test_create_superuser_success():
    user = User.objects.create_superuser(
        email="admin@example.com",
        username="adminuser",
        password="adminpassword",
        phone_number="09876543211",
    )
    assert user.is_superuser is True
    assert user.is_staff is True


@pytest.mark.django_db
def test_invalid_email_validation_raises_error():
    with pytest.raises(ValueError, match="invalid email address"):
        User.objects.create_user(
            email="invalid-email",
            username="testuser",
            password="testpassword",
            phone_number="09876543211",
        )


@pytest.mark.django_db
def test_invalid_phone_number_validation_raises_error():
    with pytest.raises(ValueError, match="Invalid mobile number"):
        User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            phone_number="invalid-phone",
        )
