from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserManager


ACCOUNT_TYPE_CHOICE = (("moderator", "Moderator"), ("member", "Member"))


class User(AbstractUser):
    username = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        default="",
        error_messages={
            "required": "Username must be provided.",
            "unique": "A user with this username already exists.",
        },
    )

    account_type = models.CharField(
        max_length=14,
        error_messages={"required": "Account Type must be specified"},
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={"unique": "A user with this email already exists"},
    )
    verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email"]
    objects = UserManager()

    def __unicode__(self):
        return self.email
