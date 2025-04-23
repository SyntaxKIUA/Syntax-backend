from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phone_number = PhoneNumberField(region="IR", unique=True, verbose_name=_("Phone number"))
    email = models.EmailField(unique=True)
    birth_date = models.DateField(
        max_length=10,
        help_text="فرمت: YYYY-MM-DD",
        blank=True,
        null=True,
        verbose_name=_("Birth date")
    )
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10, blank=True, null=True)

    is_active = models.BooleanField(_("is active"), default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    @property
    def fullname(self):
        "Returns the person's full name."
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=False, blank=False)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True, verbose_name="biography")
    professional = models.CharField(max_length=255, blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0, verbose_name=_("followers count"), db_index=True)
    followings_count = models.PositiveIntegerField(default=0,verbose_name=_("followings count"), db_index=True)
    posts_count = models.PositiveIntegerField(default=0, verbose_name=_("posts count"))

    def __str__(self):
        return self.user.username
