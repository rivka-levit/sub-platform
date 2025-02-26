from django.contrib.auth.base_user import BaseUserManager

from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier"""

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError(_('The email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with appropriate extra fields."""

        add_fields = {'is_staff': True,
                      'is_superuser': True,
                      'is_active': True}
        extra_fields.update(add_fields)

        for field in add_fields:
            if extra_fields.get(field) is not True:
                raise ValueError(_('The superuser must have %s=True' % field))

        return self.create_user(email, password, **extra_fields)
