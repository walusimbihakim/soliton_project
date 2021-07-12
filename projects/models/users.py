from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from projects.constants import SUPERVISOR, PROJECT_MANAGER, GENERAL_MANAGER, FIELD_MANAGER, FINANCE_OFFICER, \
    TYPE_CHOICES


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username=username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    role_options = [
        (SUPERVISOR, SUPERVISOR),
        (FIELD_MANAGER, FIELD_MANAGER),
        (FINANCE_OFFICER, FINANCE_OFFICER),
        (PROJECT_MANAGER, PROJECT_MANAGER),
        (GENERAL_MANAGER, GENERAL_MANAGER)
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=50)
    user_role = models.CharField(max_length=50, choices=role_options, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True)
    password = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    class Meta:
        unique_together = ('first_name', 'last_name')
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.name}'

    @property
    def is_finance(self) -> bool:
        return self.user_role == FINANCE_OFFICER

    @property
    def is_project_manager(self) -> bool:
        return self.user_role == PROJECT_MANAGER

    @property
    def is_approver(self) -> bool:
        return self.user_role in (FIELD_MANAGER, PROJECT_MANAGER, GENERAL_MANAGER)

    @property
    def is_supervisor(self) -> bool:
        return self.user_role == SUPERVISOR

    @property
    def notifications(self):
        return self.notification_set.all()

    @property
    def unread_notifications(self):
        return self.notification_set.filter(is_read=False)
