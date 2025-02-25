from django.test import Client
import pytest
from accounts.models import User
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="testpassword",
        phone_number="09876543213",
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.check_password("testpassword")
    assert str(user) == "testuser"


# @pytest.mark.django_db
# def test_create_user_without_email_raises_error():
#     with pytest.raises(ValidationError):
#         User.objects.create_user(
#             email="",
#             username="testuser",
#             password="testpassword",
#             phone_number="09876543211",
#         )


@pytest.mark.django_db
def test_create_user_without_username_raises_error():
    with pytest.raises(ValueError):
        User.objects.create_user(
            email="test@example.com",
            username="",
            password="testpassword",
            phone_number="09876543211",
        )


@pytest.mark.django_db
def test_create_user_without_password_raises_error():
    with pytest.raises(ValidationError):
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
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="invalid-email",
            username="testuser",
            password="testpassword",
            phone_number="09876543211",
        )


@pytest.mark.django_db
def test_invalid_phone_number_validation_raises_error():
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword",
            phone_number="invalid-phone",
        )


@pytest.mark.django_db
def test_user_str_method():
    user = User.objects.create_user(
        email="test@example.com",
        username="testuser",
        phone_number="09876543211",
        password="password123"
    )

    assert str(user) == "testuser"


@pytest.mark.django_db
def test_email_normalization():
    mixed_email = "TestUser@Example.COM"
    user = User.objects.create_user(
        email=mixed_email,
        username="testuser2",
        phone_number="09876543211",
        password="password123"
    )
    assert user.email == mixed_email.lower()


@pytest.mark.django_db
def test_unique_email_constraint():
    User.objects.create_user(
        email="unique@example.com",
        username="uniqueuser1",
        phone_number="0987654321",
        password="password123"
    )
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="unique@example.com",
            username="uniqueuser2",
            phone_number="09876543211",
            password="password123"
        )


@pytest.mark.django_db
def test_unique_username_constraint():
    User.objects.create_user(
        email="user1@example.com",
        username="uniqueusername",
        phone_number="09876543211",
        password="password123"
    )
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="user2@example.com",
            username="uniqueusername",
            phone_number="09876543211",
            password="password123"
        )


@pytest.mark.django_db
def test_unique_phone_number_constraint():
    User.objects.create_user(
        email="phone1@example.com",
        username="userphone1",
        phone_number="09876543211",
        password="password123"
    )
    with pytest.raises(ValidationError):

        User.objects.create_user(
            email="phone2@example.com",
            username="userphone2",
            phone_number="09876543211",
            password="password123"
        )


@pytest.mark.django_db
def test_update_user_invalid_phone():
    user = User.objects.create_user(
        email="update@example.com",
        username="updateuser",
        phone_number="09876543211",
        password="password123"
    )

    user.phone_number = "invalid_phone"
    with pytest.raises(ValidationError):
        user.save()


@pytest.mark.django_db
def test_update_user_invalid_email():
    user = User.objects.create_user(
        email="update2@example.com",
        username="updateuser2",
        phone_number="09876543211",
        password="password123"
    )

    user.email = "invalid_email"
    with pytest.raises(ValidationError):
        user.save()


@pytest.mark.django_db
def test_update_user_valid_phone():
    user = User.objects.create_user(
        email="update3@example.com",
        username="updateuser3",
        phone_number="09876543211",
        password="password123"
    )
    new_phone = "09876543210"

    with pytest.raises(ValidationError):
        user.phone_number = new_phone
        user.save()
        user.refresh_from_db()


@pytest.mark.django_db
def test_create_superuser_invalid_flags():
    with pytest.raises(ValidationError):
        User.objects.create_superuser(
            email="super@example.com",
            username="superuser",
            phone_number="09876543211",
            password="password123",
            is_staff=False
        )
    with pytest.raises(ValidationError):
        User.objects.create_superuser(
            email="super2@example.com",
            username="superuser2",
            phone_number="09876543211",
            password="password123",
            is_superuser=False
        )


@pytest.mark.django_db
def test_user_optional_fields():
    user = User.objects.create_user(
        email="optional@example.com",
        username="optionaluser",
        phone_number="09876543211",
        password="password123",
        first_name="John",
        last_name="Doe",
        bio="A test bio.",
        professional="Developer"
    )
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.bio == "A test bio."
    assert user.professional == "Developer"


@pytest.mark.django_db
@pytest.mark.parametrize("gender_input, validity", [
    ('male', True),
    ('female', True),
    ('other', False),
    ('', True),
    (None, True),
])
def test_user_gender_validation(gender_input, validity):
    user = User(
        email="gender@test.com",
        username="gendertest",
        phone_number="09876543211",
        password="password123",
        gender=gender_input
    )
    if validity:
        user.save()
        assert user.gender == gender_input
    else:
        with pytest.raises(ValidationError):
            user.full_clean()


@pytest.mark.django_db
def test_birth_date_in_future_raises_error():
    future_date = timezone.now().date() + timezone.timedelta(days=1)
    user = User(
        email="future@test.com",
        username="futuretest",
        phone_number="09876543211",
        password="password123",
        birth_date=future_date
    )
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_default_counts():
    user = User.objects.create_user(
        email="counts@test.com",
        username="countstest",
        phone_number="09876543211",
        password="password123"
    )
    assert user.followers_count == 0
    assert user.followings_count == 0
    assert user.posts_count == 0


@pytest.mark.django_db
def test_update_email_to_duplicate():
    User.objects.create_user(
        email="original@test.com",
        username="originaluser",
        phone_number="09876543211",
        password="password123"
    )
    user2 = User.objects.create_user(
        email="user2@test.com",
        username="user2",
        phone_number="09876543212",
        password="password123"
    )
    user2.email = "original@test.com"
    with pytest.raises(IntegrityError):
        user2.save()


@pytest.mark.django_db
def test_create_inactive_user():
    user = User.objects.create_user(
        email="inactive@test.com",
        username="inactiveuser",
        phone_number="09876543211",
        password="password123",
        is_active=False
    )
    assert user.is_active is False


@pytest.mark.django_db
def test_username_max_length_validation():
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="longuser@test.com",
            username='a' * 33,
            phone_number="09876543211",
            password="password123"
        )


@pytest.mark.django_db
def test_phone_number_length_validation():
    with pytest.raises(ValidationError):
        User.objects.create_user(
            email="test@example.com",
            username="testuser",
            phone_number='123456789012',
            password="password123"
        )


@pytest.mark.django_db
@pytest.mark.parametrize("email, validity", [
    ("valid@example.com", True),
    ("invalid-email", False),
    ("another.valid@sub.example.com", True),
    ("no@tld", False),
])
def test_email_parameterized(email, validity):
    if validity:
        User.objects.create_user(
            email=email,
            username="userparam",
            phone_number="09876543211",
            password="password123"
        )
    else:
        with pytest.raises(ValidationError):
            User.objects.create_user(
                email=email,
                username="userparam",
                phone_number="09876543211",
                password="password123"
            )


@pytest.mark.django_db
def test_regular_user_permissions():
    user = User.objects.create_user(
        email="regular@test.com",
        username="regularuser",
        phone_number="09876543211",
        password="password123"
    )
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_email_normalization_on_save():
    email = "TestUser@Example.COM"
    user = User.objects.create_user(
        email=email,
        username="normalized",
        phone_number="09876543211",
        password="password123"
    )
    assert user.email == email.lower()


@pytest.mark.django_db
@pytest.mark.parametrize("phone, validity", [
    ("09123456789", True),
    ("+989123456789", False),
    ("0936a547890", False),
    ("21234567890", False),
])
def test_iranian_phone_validation(phone, validity):
    if validity:
        User.objects.create_user(
            email="phone@test.com",
            username="phonetest",
            phone_number=phone,
            password="password123"
        )
    else:
        with pytest.raises(ValidationError):
            user = User(
                email="phone@test.com",
                username="phonetest",
                phone_number=phone,
                password="password123"
            )
            user.full_clean()


@pytest.mark.django_db
def test_username_update_to_duplicate_via_queryset():
    User.objects.create_user(
        email="originaluser@test.com",
        username="originalusername",
        phone_number="09876543211",
        password="password123"
    )
    user2 = User.objects.create_user(
        email="user2@test.com",
        username="uniqueusername",
        phone_number="09876543212",
        password="password123"
    )

    with pytest.raises(IntegrityError):
        User.objects.filter(pk=user2.pk).update(username="originalusername")


@pytest.mark.django_db
def test_date_joined_auto_populate():
    before_creation = timezone.now()
    user = User.objects.create_user(
        email="date@test.com",
        username="dateuser",
        phone_number="09876543211",
        password="password123"
    )
    after_creation = timezone.now()
    assert before_creation <= user.date_joined <= after_creation


@pytest.mark.django_db
@pytest.mark.parametrize("field, default_value", [
    ("is_active", True),
    ("is_staff", False),
    ("is_superuser", False),
])
def test_boolean_fields_defaults(field, default_value):
    user = User.objects.create_user(
        email="boolean@test.com",
        username="booleantest",
        phone_number="09876543211",
        password="password123"
    )
    assert getattr(user, field) == default_value


@pytest.mark.django_db
@pytest.mark.parametrize("field, value, max_length", [
    ("username", "a" * 32, 32),
    ("professional", "b" * 255, 255),
    ("first_name", "c" * 50, 50),
])
def test_max_length_validation(field, value, max_length):
    model_field = User._meta.get_field(field)
    assert model_field.max_length == max_length
    User.objects.create_user(
        email=f"{field}@test.com",
        username="lengthtest",
        phone_number="09876543211",
        password="password123",
        **{field: value}
    )


@pytest.mark.django_db
def test_nullable_fields():
    user = User.objects.create_user(
        email="nullable@test.com",
        username="nullableuser",
        phone_number="09876543211",
        password="password123",
        first_name=None,
        last_name=None,
        bio=None
    )
    assert user.first_name is None
    assert user.last_name is None
    assert user.bio is None


@pytest.mark.django_db
def test_custom_auth_backend():
    User.objects.create_user(
        email="auth@test.com",
        username="authtest",
        phone_number="09876543211",
        password="password123"
    )

    client = Client()
    assert client.login(username="authtest", password="password123")
    assert not client.login(username="authtest", password="wrongpassword")


@pytest.mark.django_db
def test_queryset_operations():
    User.objects.create_user(
        email="q1@test.com",
        username="user1",
        phone_number="09876543211",
        password="pass",
        is_active=True
    )
    User.objects.create_user(
        email="q2@test.com",
        username="user2",
        phone_number="09876543212",
        password="pass",
        is_active=False
    )

    active_users = User.objects.filter(is_active=True)
    assert active_users.count() == 1
    assert active_users.first().username == "user1"


@pytest.mark.django_db
def test_follow_relationships():
    user1 = User.objects.create_user(
        email="f1@test.com",
        username="follower1",
        phone_number="09876543211",
        password="pass"
    )
    user2 = User.objects.create_user(
        email="f2@test.com",
        username="following1",
        phone_number="09876543212",
        password="pass"
    )

    user1.following.add(user2)
    assert user1.following.count() == 1
    assert user2.followers.count() == 1
    assert user1.followings_count == 1
    assert user2.followers_count == 1


@pytest.mark.django_db
def test_bulk_create_validation():
    users = [
        User(
            email=f"bulk{i}@test.com",
            username=f"bulkuser{i}",
            phone_number=f"0987654321{i}",
            password="password123"
        ) for i in range(1, 6)
    ]

    with pytest.raises(ValidationError):
        User.objects.bulk_create(users)


@pytest.mark.django_db
@pytest.mark.parametrize("phone_number, validity", [
    ("09123456789", True),
    ("۰۹۸۷۶۵۴۳۲۱۱", False),
    ("09۱۲3۴56۷8", False),
    ("09876a54321", False),
    ("+98912345678", False),
])
def test_phone_number_english_digits_only(phone_number, validity):
    if validity:
        User.objects.create_user(
            email="phone@test.com",
            username="phonetest",
            phone_number=phone_number,
            password="password123"
        )
    else:
        with pytest.raises(ValidationError):
            User.objects.create_user(
                email="phone@test.com",
                username="phonetest",
                phone_number=phone_number,
                password="password123"
            )


@pytest.mark.django_db
@pytest.mark.parametrize("username, validity", [
    ("john_doe123", True),
    ("j۰hن", False),
    ("ユーザー名", False),
    (" space ", False),
    ("user@name", False),
])
def test_username_english_chars_only(username, validity):
    if validity:
        User.objects.create_user(
            email="user@test.com",
            username=username,
            phone_number="09876543211",
            password="password123"
        )
    else:
        with pytest.raises(ValidationError):
            User.objects.create_user(
                email="user@test.com",
                username=username,
                phone_number="09876543211",
                password="password123"
            )


@pytest.mark.django_db
@pytest.mark.parametrize("bio_text, validity", [
    ("این یک بیوگرافی فارسی است", True),
    ("This is an English bio", True),
    ("こんにちは", False),
    ("🇮🇷", False),        ("مرسی! (Thanks)", True),
])
def test_bio_persian_english_only(bio_text, validity):
    user = User(
        email="bio@test.com",
        username="biotest",
        phone_number="09876543211",
        password="password123",
        bio=bio_text
    )
    if validity:
        user.full_clean()
    else:
        with pytest.raises(ValidationError):
            user.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("name, field, validity", [
    ("علی", "first_name", True),
    ("John", "first_name", True),
    ("Мария", "first_name", False),
    ("نام خانوادگی", "last_name", True),
    ("123_surname", "last_name", False),
    ("O'Conner", "last_name", True),
])
def test_name_persian_english_only(name, field, validity):
    user = User(
        email="name@test.com",
        username="nametest",
        phone_number="09876543211",
        password="password123",
        **{field: name}
    )
    if validity:
        user.full_clean()
    else:
        with pytest.raises(ValidationError):
            user.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("professional_text, validity", [
    ("توسعه‌دهنده پایتون", True),
    ("Python Developer", True),
    ("デベロッパー", False),     # ژاپنی
    ("@#\$%^", False),          # کاراکترهای ویژه
])
def test_professional_field_validation(professional_text, validity):
    user = User(
        email="pro@test.com",
        username="protest",
        phone_number="09876543211",
        password="password123",
        professional=professional_text
    )
    if validity:
        user.full_clean()
    else:
        with pytest.raises(ValidationError):
            user.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("gender_input, validity", [
    ("male", True),
    ("female", True),
    ("other", False),
    ("مرد", False),
    (None, True),
])
def test_gender_choices_validation(gender_input, validity):
    user = User(
        email="gender@test.com",
        username="gendertest",
        phone_number="09876543211",
        password="password123",
        gender=gender_input
    )
    if validity:
        user.full_clean()
    else:
        with pytest.raises(ValidationError):
            user.full_clean()


@pytest.mark.django_db
def test_multiple_field_validation():
    with pytest.raises(ValidationError) as e:
        User.objects.create_user(
            email="invalid@test.com",
            username="ユーザー",
            phone_number="۰۹۸۷۶",
            first_name="123!",
            password="password123"
        )
    errors = e.value.message_dict
    assert 'username' in errors
    assert 'phone_number' in errors
    assert 'first_name' in errors


@pytest.mark.django_db
@pytest.mark.parametrize("char", [
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=",
    "،", "؛", "؟", "«", "»", " ", "\n", "\t"
])
def test_allowed_special_chars_in_bio(char):
    user = User(
        email="special@test.com",
        username="specialtest",
        phone_number="09876543211",
        password="password123",
        bio=f"Test {char} Char"
    )
    user.full_clean()


@pytest.mark.django_db
def test_uppercase_validation():
    user = User(
        email="UPPER@TEST.COM",
        username="USERNAME",
        phone_number="09876543211",
        password="password123",
        first_name="ALI"
    )
    user.full_clean()
    assert user.email == "upper@test.com"


@pytest.mark.django_db
def test_mixed_persian_english_names():
    User.objects.create_user(
        email="mix@test.com",
        username="mixuser",
        phone_number="09876543211",
        password="password123",
        first_name="Aliرضا",
        last_name="Smithخانی"
    )
