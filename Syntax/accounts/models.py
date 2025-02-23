from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from accounts.api.validations import Validator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(
        self, email, username, phone_number, password=None, **extra_fields
    ):
        if not email:
            raise ValidationError(
                {'email': _('Users must have an email address')}
            )
        if not username:
            raise ValidationError(
                {'username': _('Users must have a username')}
            )
        if not password:
            raise ValidationError(
                {'password': _('Users must have a password')}
            )
        if not phone_number:
            raise ValidationError(
                {'phone_number': _('Users must have a phone number')}
            )

        email = self.normalize_email(email).lower()
        user = self.model(
            email=email,
            username=username,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username, phone_number, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValidationError(
                {'is_staff': _('Superuser must have is_staff=True.')}
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError(
                {'is_superuser': _('Superuser must have is_superuser=True.')}
            )

        return self.create_user(
            email, username, phone_number, password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(
        max_length=32, unique=True, blank=False, null=False
    )
    phone_number = models.CharField(
        max_length=11, unique=True, blank=False, null=False
    )
    email = models.EmailField(unique=True, blank=False, null=False)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)
    professional = models.CharField(max_length=255, blank=True, null=True)
    followings_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    def full_clean(self):
        self.email = self.email.lower()
        Validator.validate_email(self.email)
        Validator.phone_number(self.phone_number)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
