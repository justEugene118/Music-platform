from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

"""
    Full guide for custom user is here: https://django.fun/docs/django/ru/4.0/topics/auth/customizing/
"""


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, username, **extra_fields):
        """
        Create and save a User with the given email, username and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, username and password.
        """
        extra_fields.setdefault('is_creator', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('username', 'admin')

        if extra_fields.get('is_creator') is not True:
            raise ValueError(_('Superuser must have is_creator=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


