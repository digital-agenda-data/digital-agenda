from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from digital_agenda.common.citext import CIEmailField
from digital_agenda.common.models import TimestampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")

        if not password:
            raise ValueError("Users must have a password.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    email = CIEmailField(unique=True)
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        default=True,
        help_text="Designates whether the user can log into this admin site.",
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email
