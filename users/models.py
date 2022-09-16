from django.contrib import auth
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
# from helper.views import CommonHelper
from django.core.exceptions import PermissionDenied
from django.db import models

import choices
from DigitalAyurved import settings

User = settings.AUTH_USER_MODEL


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError("Email must be set")
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        user = self.create_user(
            mobile=mobile,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(unique=False, max_length=200)
    mobile = models.CharField(unique=True, max_length=10)
    email = models.EmailField(blank=True, verbose_name='email', null=True)

    password = models.CharField(max_length=100, null=True, blank=True)
    # for custom user
    account_type = models.CharField(max_length=20, verbose_name='Account Type',
                                    choices=choices.ACCOUNT_TYPE_CHOICES, null=True, blank=True)
    # for django user
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    # created and modify
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "%s #%s" % (self.name, self.mobile)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        permission = perm.split('.')[1]

        for backend in auth.get_backends():
            if not hasattr(backend, 'has_perm'):
                continue
            try:
                if backend.has_perm(self, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        if not self.is_superuser and self.groups:
            if len(Group.objects.filter()) > 0:
                return True
            else:
                return False
        else:
            return True

    def save(self, *args, **kwargs):
        # self.set_password(self.password)
        # self.save()
        return super().save(*args, **kwargs)
