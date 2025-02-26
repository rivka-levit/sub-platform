from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from account.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    is_writer = models.BooleanField(
        default=False,
        verbose_name='Are you a writer?'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return str(self.email).split('@')[0]
